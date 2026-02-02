# Email Labeling AI

A Python tool to automatically label today's emails using AI.

## Setup

1. **Install Dependencies**
   ```bash
   pip install PyYAML openai
   ```

2. **Configuration**
   Edit `config/config.yml` with your settings:
   - `email`: IMAP connection details.
   - `ai`: API key, model, and the **prompt** to control classification.

3. **Usage**
   ```bash
   python src/main.py
   ```

## License
License is under GPL-2.0,
you can view the License file for more details.