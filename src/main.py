import os
import sys

# Auto-activate venv if not already active to fix 'ModuleNotFoundError'
def activate_venv():
    # Only try to activate if we are not already in a venv
    if sys.prefix == sys.base_prefix:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        venv_python = os.path.join(base_dir, 'venv', 'bin', 'python3')
        
        if os.path.exists(venv_python):
            # Re-execute the script with the venv interpreter
            os.execv(venv_python, [venv_python] + sys.argv)
        else:
            print("Warning: Virtual environment 'venv' not found. Please run './run.sh' first to create it.")

activate_venv()

# add current directory to path to find modules if running from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config_loader
import imap_handler
import ai_handler
import utils
import state_manager

def main():
    # load configuration
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configPath = os.path.join(baseDir, 'config', 'config.yml')
    stateFile = os.path.join(baseDir, 'config', 'state.yml')
    
    try:
        config = config_loader.configLoad(configPath)
    
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    # validate config essentials
    if not config['email']['imap_server']:
        print("Error: 'imap_server' not configured in config.yml")
        return

    # CRITICAL: Load last processed timestamp
    lastProcessedTimestamp = state_manager.stateLoad(stateFile)
    
    if lastProcessedTimestamp:
        print(f"Last processed timestamp: {lastProcessedTimestamp}")
        print("Only processing emails newer than this timestamp...")
    else:
        print("No previous state found. Processing all emails from today.")

    # connect to imap
    try:
        print("Connecting to IMAP server...")
        connection = imap_handler.imapConnect(config)
        print("Connected.")
        
    except Exception as e:
        print(f"Error connecting to IMAP: {e}")
        return

    # CRITICAL: Get only NEW emails (after last processed timestamp)
    try:
        emails = imap_handler.imapGetEmails(connection, lastProcessedTimestamp)
        print(f"Retrieved {len(emails)} NEW emails from today.")
    
    except Exception as e:
        print(f"Error fetching emails: {e}")
        emails = []

    if not emails:
        print("No new emails to process.")
        return

    # process in batches
    emailBatches = utils.utilsBatchList(emails, 20)
    
    totalLabeled = 0
    totalFailed = 0
    
    for batchNum, batch in enumerate(emailBatches, 1):
        print(f"\n[Batch {batchNum}] Processing {len(batch)} emails...")
        
        try:
            # aiGetLabels now receives full email objects with 'from' field
            labels = ai_handler.aiGetLabels(batch, config)
            
            # check if labels is None (no API key or error)
            if labels is None:
                print("Skipping labeling for this batch (no API key or error)")
                continue
            
            # check if labels dict is empty
            if not labels:
                print("Warning: AI returned no labels for this batch")
                continue
            
            # apply labels
            for emailItem in batch:
                title = emailItem['title']
                sender = emailItem['from']
                
                if title in labels:
                    label = labels[title]
                    
                    # show sender info in log for context
                    senderShort = sender[:30] + "..." if len(sender) > 30 else sender
                    titleShort = title[:40] + "..." if len(title) > 40 else title
                    
                    print(f"From: {senderShort}")
                    print(f"  Subject: '{titleShort}'")
                    print(f"  → Label: '{label}'")
                    
                    try:
                        success = imap_handler.imapLabelEmail(connection, emailItem['id'], label)
                        if success:
                            totalLabeled += 1
                        else:
                            totalFailed += 1
                            
                    except Exception as e:
                        print(f"  ✗ Error labeling email: {e}")
                        totalFailed += 1
                else:
                    titleShort = title[:40] + "..." if len(title) > 40 else title
                    print(f"Warning: No label returned for '{titleShort}'")
                    totalFailed += 1
        
        except Exception as e:
            print(f"Error processing AI batch: {e}")
            totalFailed += len(batch)

    # CRITICAL: Save the latest timestamp after successful processing
    if emails:
        latestTimestamp = state_manager.stateGetLatestTimestamp(emails)
        
        if latestTimestamp:
            if state_manager.stateSave(stateFile, latestTimestamp):
                print(f"\n✓ Saved latest timestamp: {latestTimestamp}")
            else:
                print(f"\n✗ Failed to save state!")

    try:
        connection.logout()
    except:
        pass

    print("\n" + "="*50)
    print("Summary:")
    print(f"  Total NEW emails processed: {len(emails)}")
    print(f"  Successfully labeled: {totalLabeled}")
    print(f"  Failed: {totalFailed}")
    print("="*50)
    print("Done.")

if __name__ == "__main__":
    main()
