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

def imapLabelEmail(connection, emailId, label):
    # Gmail labels work via IMAP folders
    # Gmail shows IMAP folders as labels in the UI
    
    try:
        # create label folder if it doesn't exist
        connection.create(label)
    except:
        # folder already exists
        pass
    
    try:
        # copy email to label folder (Gmail displays this as a label)
        connection.copy(emailId, label)
        print(f"  ✓ Applied Gmail label: {label}")
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to apply label '{label}': {e}")
        return False
