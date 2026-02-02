# Email-Labeling-AI
Order emails into labels with ai

## Project Struct
project/
├── src/                    # Source Code
│   ├── main.py            # Hauptprogramm
│   ├── emailSorter.py     # IMAP & Email-Sortierung
│   ├── aiClient.py        # AI API Integration
│   ├── configLoader.py    # YAML Config Loader
│   ├── logger.py          # Logging Setup
│   ├── webConfig.py       # Flask Web-Interface
│   └── templates/
│       └── config.html    # HTML Config-Seite
├── config/
│   └── config.example.yaml # Beispiel-Konfiguration
├── tests/
│   └── test_configLoader.py # Tests
├── .github/               # GitHub Templates
├── CONTRIBUTING.md        # Deine Style-Guidelines
├── AGENT.md              # Claude Code Instructions
├── README.md             # Dokumentation
├── QUICKSTART.md         # Quick-Start Guide
└── setup.sh              # Setup-Script