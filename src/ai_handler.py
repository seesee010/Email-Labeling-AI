import yaml
import json
from openai import OpenAI

def aiGetLabels(emails, config, existingLabels):
    # check if list is empty
    if not emails:
        return None

    apiKey = config['ai']['api_key']
    model = config['ai']['model']
    
    # BUG FIX: Return None instead of mock data when no API key
    # This prevents labeling when user just wants to see email titles
    if apiKey == "your-api-key-here" or not apiKey:
        print("\n" + "="*50)
        print("WARNING: No API key configured!")
        print("="*50)
        print("\nEmail titles found today:")
        for i, emailData in enumerate(emails, 1):
            print(f"  {i}. From: {emailData['from']}")
            print(f"     Subject: {emailData['title']}")
        print("\n" + "="*50)
        print("Skipping labeling. Configure API key in config/config.yml to enable AI labeling.")
        print("="*50 + "\n")
        return None
    
    # FEATURE: Build enhanced prompt with sender information
    emailListStr = ""
    for emailData in emails:
        title = emailData['title']
        sender = emailData['from']
        emailListStr += f'- Title: "{title}"\n  From: {sender}\n'
    
    # CRITICAL: Include existing labels in prompt
    existingLabelsStr = ', '.join(existingLabels) if existingLabels else 'No labels exist yet'
    
    # get prompt from config
    systemPrompt = config['ai'].get('prompt', "Classify these emails.")
    
    # enhance system prompt to use sender info AND existing labels
    enhancedPrompt = f"""{systemPrompt}

CRITICAL: You MUST use ONLY these existing Gmail labels:
{existingLabelsStr}

If none of the existing labels fit an email well, you can suggest a new label, but prefer using existing ones when possible.

IMPORTANT: You will receive emails with both their subject line AND sender information.
Use BOTH to make better classification decisions. For example:
- "Re: PR #123" from "github.com" → likely "development" or "code-review"
- "Re: Meeting" from "boss@company.com" → likely "work" or "meetings"
- "Sale Alert" from "amazon.com" → likely "shopping"

Return ONLY a YAML object where the key is the EXACT subject line (in quotes if it contains spaces or special characters) and the value is the label.

Example output format:
"Re: PR #123": "development"
"Weekly Newsletter": "news"
"""

    # OpenAI API
    try:
        client = OpenAI(api_key=apiKey)
        
        messages = [
            {"role": "system", "content": enhancedPrompt},
            {"role": "user", "content": f"Emails to classify:\n{emailListStr}"}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=config['ai']['temperature']
        )
        
        content = response.choices[0].message.content
        
        # parse the content as YAML
        # sometimes models output markdown blocks, we strip them if present
        cleanContent = content.replace("```yaml", "").replace("```", "").strip()
        
        # extract only titles for validation
        titles = [e['title'] for e in emails]
        return aiParseResponse(cleanContent, titles)
            
    except Exception as e:
        print(f"Error in AI request: {e}")
        return None

def aiParseResponse(responseString, originalTitles):
    # parse the yaml response
    try:
        data = yaml.safe_load(responseString)
        
        # BUG FIX: Validate that response is actually a dict
        if not isinstance(data, dict):
            print(f"Warning: AI response is not a valid YAML dict: {type(data)}")
            return None
        
        # BUG FIX: Log parsing results
        print(f"  → AI returned {len(data)} labels")
        
        # Check if any titles are missing
        missingTitles = set(originalTitles) - set(data.keys())
        if missingTitles:
            print(f"  ⚠ Warning: AI didn't label {len(missingTitles)} emails")
        
        return data
        
    except yaml.YAMLError as e:
        print(f"Error parsing YAML response: {e}")
        print(f"Raw response was: {responseString[:200]}...")
        return None
