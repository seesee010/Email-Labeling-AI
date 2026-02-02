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

def main():
    # load configuration
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    configPath = os.path.join(baseDir, 'config', 'config.yml')
    
    try:
        config = config_loader.configLoad(configPath)
    
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    # validate config essentials
    if not config['email']['imap_server']:
        print("Error: 'imap_server' not configured in config.yml")
        return

    # connect to imap
    try:
        print("Connecting to IMAP server...")
        connection = imap_handler.imapConnect(config)
        print("Connected.")
        
    except Exception as e:
        print(f"Error connecting to IMAP: {e}")
        return

    # get emails
    try:
        emails = imap_handler.imapGetEmails(connection)
        print(f"Retrieved {len(emails)} emails from today.")
    
    except Exception as e:
        print(f"Error fetching emails: {e}")
        emails = []

    if not emails:
        print("No emails found to process.")
        return

    # process in batches
    emailBatches = utils.utilsBatchList(emails, 20)
    
    for batch in emailBatches:
        titles = [e['title'] for e in batch]
        
        # get labels from AI
        print(f"Sending batch of {len(titles)} to AI...")
        
        try:
            labels = ai_handler.aiGetLabels(titles, config)
            
            # apply labels
            for emailItem in batch:
                title = emailItem['title']
                
                if title in labels:
                    label = labels[title]
                    print(f"Labeling email '{title}' as '{label}'")
                    try:
                        imap_handler.imapLabelEmail(connection, emailItem['id'], label)
                    except Exception as e:
                        print(f"Error labeling email {emailItem['id']}: {e}")
        
        except Exception as e:
            print(f"Error processing AI batch: {e}")

    try:
        connection.logout()
    except:
        pass

    print("Done.")

if __name__ == "__main__":
    main()