import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
import datetime

def imapConnect(config):
    # connect to IMAP server
    server = config['email']['imap_server']
    port = config['email']['port']
    username = config['email']['username']
    password = config['email']['password']

    connection = imaplib.IMAP4_SSL(server, port)
    connection.login(username, password)
    
    return connection

def imapGetExistingLabels(connection):
    # get all existing Gmail labels/folders
    # this is called once at startup to know which labels exist
    
    try:
        status, folders = connection.list()
        
        if status != "OK":
            return []
        
        labelList = []
        
        for folder in folders:
            # decode folder name
            folderStr = folder.decode() if isinstance(folder, bytes) else folder
            
            # extract folder name from IMAP list response
            # format: (\HasNoChildren) "/" "LabelName"
            parts = folderStr.split('"')
            
            if len(parts) >= 3:
                folderName = parts[-2]
                
                # skip system folders
                if folderName not in ['INBOX', '[Gmail]', '[Gmail]/All Mail', 
                                      '[Gmail]/Drafts', '[Gmail]/Sent Mail', 
                                      '[Gmail]/Spam', '[Gmail]/Starred', 
                                      '[Gmail]/Trash', '[Gmail]/Important']:
                    # remove [Gmail]/ prefix if present
                    if folderName.startswith('[Gmail]/'):
                        folderName = folderName.replace('[Gmail]/', '')
                    
                    labelList.append(folderName)
        
        return labelList
        
    except Exception as e:
        print(f"Error getting existing labels: {e}")
        return []

def imapGetEmails(connection, lastProcessedTimestamp=None):
    # select inbox
    connection.select("INBOX")
    
    # get today's date
    date = datetime.datetime.now().strftime("%d-%b-%Y")
    
    # search for emails from today
    status, messages = connection.search(None, f'(ON "{date}")')
    
    if status != "OK":
        return []

    emailIds = messages[0].split()
    
    # if no emails found, return early
    if not emailIds:
        return []
    
    emailList = []

    for eId in emailIds:
        # fetch email headers
        res, msgData = connection.fetch(eId, "(RFC822)")
        
        for responsePart in msgData:
            if isinstance(responsePart, tuple):
                msg = email.message_from_bytes(responsePart[1])
                
                # CRITICAL: Extract timestamp from email
                dateHeader = msg.get("Date")
                emailTimestamp = None
                
                if dateHeader:
                    try:
                        emailTimestamp = parsedate_to_datetime(dateHeader)
                        # convert to unix timestamp for easy comparison
                        emailTimestampUnix = emailTimestamp.timestamp()
                    except:
                        # if parsing fails, use current time
                        emailTimestampUnix = datetime.datetime.now().timestamp()
                else:
                    emailTimestampUnix = datetime.datetime.now().timestamp()
                
                # OPTIMIZATION: Skip emails older than last processed timestamp
                if lastProcessedTimestamp and emailTimestampUnix <= lastProcessedTimestamp:
                    continue
                
                # handle missing/empty subjects
                subject = msg.get("Subject", "(No Subject)")
                
                if subject and subject != "(No Subject)":
                    subjectDecoded, encoding = decode_header(subject)[0]
                    
                    if isinstance(subjectDecoded, bytes):
                        # decode subject if needed
                        subject = subjectDecoded.decode(encoding if encoding else "utf-8")
                    else:
                        subject = subjectDecoded
                else:
                    subject = "(No Subject)"
                
                # extract sender information
                fromHeader = msg.get("From", "Unknown Sender")
                fromName, fromEmail = parseaddr(fromHeader)
                
                # decode name if needed
                if fromName:
                    try:
                        nameDecoded, encoding = decode_header(fromName)[0]
                        if isinstance(nameDecoded, bytes):
                            fromName = nameDecoded.decode(encoding if encoding else "utf-8")
                    except:
                        pass
                
                # use name if available, otherwise use email
                sender = fromName if fromName else fromEmail
                
                emailList.append({
                    "id": eId,
                    "title": subject,
                    "from": sender,
                    "from_email": fromEmail,
                    "timestamp": emailTimestampUnix
                })

    return emailList

def imapLabelEmail(connection, emailId, label, existingLabels):
    # CRITICAL: Gmail labels work differently than standard IMAP
    # We need to COPY the email to the label folder WITHOUT removing it from inbox
    
    # check if label exists in our known labels
    if label not in existingLabels:
        print(f"  ⚠ Label '{label}' doesn't exist. Creating it...")
        
        try:
            # create new label folder
            connection.create(label)
            existingLabels.append(label)
        except Exception as e:
            print(f"  ✗ Failed to create label '{label}': {e}")
            return False
    
    try:
        # CRITICAL FIX: Use COPY to add label without moving email
        # This keeps the email in INBOX and adds the label
        connection.copy(emailId, label)
        
        print(f"  ✓ Applied Gmail label: {label}")
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to apply label '{label}': {e}")
        return False
