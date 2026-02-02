# Agent Instructions

Folge STRIKT den Regeln aus CONTRIBUTING.md!

## Critical Rules

### Code Style
- **Funktionsnamen**: `camelCase` with namespace prefix (e.g., `imapConnect()`, `aiSortEmail()`)
- **Klassennamen**: `PascalCase` (e.g., `EmailSorter`, `AIClient`)
- **Variablen**: `camelCase` (e.g., `emailData`, `apiResponse`)
- **Konstanten**: `UPPER_CASE` (e.g., `MAX_RETRIES`)

### Indentation & Spacing
- 4 spaces indentation (NO tabs!)
- Always 1 space before and after `=`
- Always 1 space after comment chars: `# comment`
- Always 1 empty line between code blocks
- NO empty lines at end of file
- NO inline if statements

### Function Structure
Example:
```python
def imapConnect(server, port, username, password):
    # connect to IMAP server
    connection = imaplib.IMAP4_SSL(server, port)
    connection.login(username, password)
    
    return connection
```

### Git Workflow
- **Branch names**: `feature/<name>`, `fix/<name>`, `chores/<name>`, `refactor/<name>`, `hotfix/<name>`
- **Commit format**: Use `.gitmessage` template

### Project Structure
- `/src` - all source code
- `/config` - YAML configuration files
- `/tests` - test files
- Clean separation of concerns

### Dependencies
- Only add necessary dependencies
- Keep `requirements.txt` updated
- Prefer standard library when possible

### Testing
- Write tests for critical functions
- Use `pytest` framework
- Test files in `/tests` directory

## Important Notes
- Always follow namespace/prefix pattern for functions
- Keep code clean and readable
- Avoid deep nesting (max ~4 levels)