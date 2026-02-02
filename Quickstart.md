# Quick Start Guide

Get your Email AI Sorter up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Email account with IMAP access
- AI API key (Anthropic Claude, OpenAI, or custom)

## Step 1: Installation

```bash
# clone or download the project
cd email-ai-sorter

# run setup script
./setup.sh

# or manually:
pip install -r requirements.txt
git config commit.template .gitmessage
```

## Step 2: Configuration

### Option A: Web Interface (Recommended)

```bash
python src/webConfig.py
```

Then open http://localhost:5000 in your browser and fill in:
- Email settings (IMAP server, username, password)
- AI API settings (endpoint, API key, model)
- Labels you want to use
- Sorting preferences

### Option B: Manual Configuration

```bash
cp config/config.example.yaml config/config.yaml
nano config/config.yaml  # edit with your settings
```

## Step 3: Run

```bash
python src/main.py
```

The app will:
1. Connect to your email server
2. Check for new emails every 60 seconds (configurable)
3. Use AI to classify each email
4. Move emails to appropriate label folders

## Gmail Setup

For Gmail:
1. Enable IMAP: Settings → Forwarding and POP/IMAP → Enable IMAP
2. Create App Password: Google Account → Security → 2-Step Verification → App Passwords
3. Use app password in config (not your regular password)

Example config:
```yaml
email:
  imap_server: "imap.gmail.com"
  imap_port: 993
  username: "youremail@gmail.com"
  password: "your-app-password"
```

## AI Provider Setup

### Anthropic Claude

```yaml
ai:
  api_endpoint: "https://api.anthropic.com/v1/messages"
  api_key: "sk-ant-..."
  model: "claude-sonnet-4-20250514"
```

### OpenAI

```yaml
ai:
  api_endpoint: "https://api.openai.com/v1/chat/completions"
  api_key: "sk-..."
  model: "gpt-4"
```

### Custom API

```yaml
ai:
  api_endpoint: "https://your-api.com/endpoint"
  api_key: "your-key"
  model: "your-model"
```

## Common Issues

### "Authentication failed"
- Check your email credentials
- For Gmail, use app password not regular password
- Enable IMAP access

### "AI API error"
- Verify your API key is correct
- Check your API endpoint URL
- Ensure you have API credits/quota

### "Failed to create folder"
- Some email providers require folders to be created manually first
- Try creating the label folders in your email client first

## Tips

- Start with a few labels (3-5) for best results
- Use descriptive label names (e.g., "Work", "Personal", "Newsletter")
- Monitor the logs in `logs/email-sorter.log` for debugging
- Test with a small number of emails first

## Next Steps

- Customize labels in web interface or config file
- Adjust check interval for your needs
- Set up as a system service for automatic running
- Check logs regularly to ensure proper classification

## Getting Help

- Open an issue on GitHub
- Check logs in `logs/email-sorter.log`
- Review `README.md` for detailed documentation