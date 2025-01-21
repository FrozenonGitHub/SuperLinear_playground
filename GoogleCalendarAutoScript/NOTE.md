# GoogleCalendarAutoScript Builder Note
## Local Dev Environment

``` bash
[Python virtual environment on Mac]
$ python3 -m venv calendar-env
$ source calendar-env/bin/activate
$ deactivate

[Basic Usage]
(calendar-env) $ python main.py
# follow prompt to:
# Exit | Create an Event | List Events 

- Color of Events:
  - banana: work
  - graphite: wasted
  - lavender: learning
  - sage: exercise
  - flamingo: personal growth

```

## Q&A
### OAuth credential
- which user type to choose when creating OAuth client credentials?
  - Internal: when builiding for users within your organization only
  - External: default choice
- where is `token.pickle`? why should I use it?
  - automatically downloaded when permission is granted
  - when expired, remove it manually
  - user doesn't need to re-authorize every time



## ChatGPT Guide

- Prompt:
```
I want to write Python Script for automatically create, edit, delete events on my Google Calendar.
Show me how this can be done step by step.
```
- Answer:
```
To interact with Google Calendar using Python, you need to use the Google Calendar API. Here's a step-by-step guide:

Step 1: Set Up Google Cloud Project and Enable Calendar API
1. Go to the Google Cloud Console.
2. Create a new project or select an existing one.
3. Go to APIs & Services > Library.
4. Search for "Google Calendar API" and enable it.
5. Go to APIs & Services > Credentials and create a credential:
6. Type: OAuth 2.0 Client ID
7. Application Type: Desktop Application
8. Download the credentials.json file and save it in your project directory.

Step 2: Install Required Libraries
Install the required Python libraries using pip:

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


Step 3: Authenticate and Authorize
Authenticate your script to access the Google Calendar API.
```

