import yaml
import json
from openai import OpenAI

def aiGetLabels(titles, config):
    # check if list is empty
    if not titles:
        return {}

    apiKey = config['ai']['api_key']
    model = config['ai']['model']
    
    # helper to construct the prompt
    emailListStr = "\n".join([f'- "{t}"' for t in titles])
    
    # get prompt from config
    systemPrompt = config['ai'].get('prompt', "Classify these emails.")
    
    # If using a placeholder key, we return a mock response for safety
    if apiKey == "your-api-key-here" or not apiKey:
        print("DEBUG: Using mock AI response (API key not configured)")
        mockResponse = {}
        for title in titles:
            mockResponse[title] = "Unsorted"
        return mockResponse

    # OpenAI API
    try:
        client = OpenAI(api_key=apiKey)
        
        messages = [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": f"Emails to classify:\n{emailListStr}"}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            # Explicitly use temperature from config
            temperature=config['ai']['temperature']
        )
        
        content = response.choices[0].message.content
        
        # parse the content as YAML
        # sometimes models output markdown blocks, we strip them if present
        cleanContent = content.replace("```yaml", "").replace("```", "").strip()
        return aiParseResponse(cleanContent)
            
    except Exception as e:
        print(f"Error in AI request: {e}")
        return {}

def aiParseResponse(responseString):
    # parse the yaml response
    try:
        data = yaml.safe_load(responseString)
        return data
    except yaml.YAMLError:
        return {}
