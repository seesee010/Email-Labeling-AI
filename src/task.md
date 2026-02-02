# Ai this is your task

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
3. list all emails you got into an list
4. read the first 20 index of the list and send them as batched to the AI.
5. AI will answer with the yml.
6. You will read the full yml and use the data of the names as labels and set that specific email with that label.
7. Repeat until all emails are processed.

### Example email

Title: "new from here"
From: "[EMAIL_ADDRESS]"
To: "[EMAIL_ADDRESS]"
Date: "2022-01-01 12:00:00"
Body: "this is the body of the email"

> BUT you will only read the **title** in order to label the email. (So in details: in order to put the title into an list)

So in this example the title is "new from here" will get stored as in list as `new from here`.

So after a few times the list will look like this (the structure):

```py
allTodaysEmails = ["new from here", "next time", "hey here is your new encyrption"] # and so own...
```

## Important

There is actually a config.yml in config/, so the user can customize some stuff!


## Program
Write the code modular.
And I want to see really clean and nice code.
I will **NOT** accept any code that is not clean and nice.
As well as that I want you to use the best practices of programming.

> If you have any further questions just read the AGENT.md file, and if that doesn't help you, then you can ask me.