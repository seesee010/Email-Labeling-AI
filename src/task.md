# AI this is your task

Write a program in python that will connect to an IMAP server and will get all of today (only them from today),
then you send an AI request (batch them into 20s), the AI should strictly only output a yml object with this format:

(For example here there was the email called: "new from here", and another called "hey new day")
```yml
new-from-here: "math"
hey-new-day: "science"
```

In this example there was the label `math` and `science`.

## How the logic works in detail
1. Get all emails from today
2. use an extra variable to store the time of the lastest email (this will be used to check if there are new emails)
3. list all emails you got into an list (with title AND sender information)
4. read the first 20 index of the list and send them as batched to the AI.
5. AI will answer with the yml.
6. You will read the full yml and use the data of the names as labels and set that specific email with that label.
7. Repeat until all emails are processed.

### Example email

Title: "new from here"
From: "GitHub <[email protected]>"
To: "[EMAIL_ADDRESS]"
Date: "2022-01-01 12:00:00"
Body: "this is the body of the email"

> You will read the **title** AND **from** field to provide better context to the AI for labeling.

So in this example:
- Title: "new from here"
- From: "GitHub <[email protected]>"

This gives the AI much better context. For example:
- "Re: PR #123" from "github.com" → AI knows it's likely "development" or "code-review"
- "Re: Meeting" from "boss@company.com" → AI knows it's likely "work" or "meetings"  
- "Sale Alert" from "amazon.com" → AI knows it's likely "shopping"

The list structure will look like this:

```py
allTodaysEmails = [
    {
        "id": b'1',
        "title": "new from here",
        "from": "GitHub",
        "from_email": "[email protected]"
    },
    {
        "id": b'2', 
        "title": "Re: PR #123",
        "from": "GitHub Notifications",
        "from_email": "[email protected]"
    }
]
```

## Important

There is actually a config.yml in config/, so the user can customize some stuff!

### When no API key is configured

If the user hasn't configured an API key (it's still "your-api-key-here"), the program should:
1. **NOT** attempt to label any emails
2. **ONLY** display the emails found today with their sender info
3. Print a clear message that API key configuration is needed

Example output:
```
WARNING: No API key configured!
==================================================

Email titles found today:
  1. From: GitHub
     Subject: Re: PR #123
  2. From: Amazon
     Subject: Your order has shipped
  
==================================================
Skipping labeling. Configure API key in config/config.yml to enable AI labeling.
==================================================
```

## Program
Write the code modular.
And I want to see really clean and nice code.
I will **NOT** accept any code that is not clean and nice.
As well as that I want you to use the best practices of programming.

> If you have any further questions just read the AGENT.md file, and if that doesn't help you, then you can ask me.
