import imaplib
import email
from email.header import decode_header
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

def imapGetEmails(connection):
    # select inbox
    connection.select("INBOX")
    
    # get today's date
    date = datetime.datetime.now().strftime("%d-%b-%Y")
    
    # search for emails from today
    status, messages = connection.search(None, f'(SINCE "{date}")')
    
    if status != "OK":
        return []

    emailIds = messages[0].split()
    emailList = []

    for eId in emailIds:
        # fetch email headers
        res, msgData = connection.fetch(eId, "(RFC822)")
        
        for responsePart in msgData:
            if isinstance(responsePart, tuple):
                msg = email.message_from_bytes(responsePart[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                
                if isinstance(subject, bytes):
                    # decode subject if needed
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                emailList.append({
                    "id": eId,
                    "title": subject
                })

    return emailList

def imapLabelEmail(connection, emailId, label):
    # handle "Gmail-style" labels (X-GM-LABELS) if supported
    # this maps correctly to Gmail labels which the user requested
    try:
        # quote label if needed
        safeLabel = f'"{label}"' if " " in label else label
        
        # try Gmail specific extension
        typ, data = connection.store(emailId, '+X-GM-LABELS', safeLabel)
        
        if typ == 'OK':
            return
    except Exception:
        # ignore error and fall back to standard flags
        pass

    # fallback: apply as standard IMAP keyword/flag
    connection.store(emailId, '+FLAGS', f'({label})')
