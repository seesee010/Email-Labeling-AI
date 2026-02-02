import yaml
import os
from datetime import datetime

def stateLoad(stateFile):
    # load last processed timestamp from state file
    if not os.path.exists(stateFile):
        return None
    
    try:
        with open(stateFile, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('latest-email')
    except:
        return None

def stateSave(stateFile, timestamp):
    # save last processed timestamp to state file
    data = {
        'latest-email': timestamp
    }
    
    try:
        with open(stateFile, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False

def stateGetLatestTimestamp(emails):
    # get the most recent timestamp from a list of emails
    if not emails:
        return None
    
    latestTimestamp = None
    
    for emailData in emails:
        timestamp = emailData.get('timestamp')
        if timestamp:
            if latestTimestamp is None or timestamp > latestTimestamp:
                latestTimestamp = timestamp
    
    return latestTimestamp
