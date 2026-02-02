# Agent Instructions

Follow STRICTLY the rules from CONTRIBUTING.md!

## Critical Rules

### Code Style
- **Function names**: `camelCase` with namespace prefix (e.g., `imapConnect()`, `aiSortEmail()`)
- **Class names**: `PascalCase` (e.g., `EmailSorter`, `AIClient`)
- **Variables**: `camelCase` (e.g., `emailData`, `apiResponse`)
- **Constants**: `UPPER_CASE` (e.g., `MAX_RETRIES`)

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

### Namespace/Prefix Pattern
EVERY function MUST use a namespace prefix to indicate its context!

Examples:
- `imapConnect()` - clearly for IMAP
- `aiClassifyEmail()` - clearly for AI operations
- `configLoad()` - clearly for configuration
- `emailGetBody()` - clearly for email operations

BAD: `connect()`, `classify()`, `load()` - unclear what these are for!

This principle removes the need for many comments by making code self-documenting.

### Git Workflow
- **Branch names**: `feature/<n>`, `fix/<n>`, `chores/<n>`, `refactor/<n>`, `hotfix/<n>`
- **Commit format**: Use `.gitmessage` template
- **Commits**: Atomic - one feature/fix per commit

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

## Formatting Rules (STRICT!)

### Spacing
```python
# CORRECT
myVar = 10

# WRONG
myVar=10
myVar =10
myVar= 10
```

### If Statements
```python
# CORRECT
if condition:
    # code here
    myVar = 10

else:
    # other code
    pass

# WRONG - inline if
if condition: myVar = 10

# WRONG - no space before else
if condition:
    pass
else:
    pass
```

### Comments
```python
# CORRECT - space after #
# this is a comment

# WRONG - no space
#this is wrong
```

### Function Definitions
```python
# CORRECT - no space between name and parentheses
def myFunction():
    pass

# WRONG - space before parentheses
def myFunction ():
    pass
```

### End of File
```python
# CORRECT
def lastFunction():
    pass
# NO empty line after this!

# WRONG
def lastFunction():
    pass

# ← this empty line is forbidden!
```

## Important Notes
- Always follow namespace/prefix pattern for functions
- Keep code clean and readable
- Avoid deep nesting (max ~4 levels)
- Do NOT use nonsense variable/function names
- Keep names short but focused and meaningful
- Write all code and text in **English**!