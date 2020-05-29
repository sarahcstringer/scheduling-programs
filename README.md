# Scheduling programs different ways

You have a python script that you want to run periodically.
For this example, let's pretend that we want to run a program
that sends a text with the weather in your zipcode every morning.

After we've written the script, how do we set it up so that it runs
periodically without us needing to manually run it?

## Getting started

- Create a virtual environment `python3 -m venv venv`
- Pip install the requirements: `pip3 install -r requirements.txt`

## Setting up the weather texting script

For this service, we'll need two APIs: Twilio and OpenWeather. Both
APIs require authenticating, but have free versions of their APIs.

### Signing up for OpenWeather

Go to the [OpenWeather signup page](https://home.openweathermap.org/users/sign_up).
Create a username and password.

Once you've created your account and are logged in, find your [API key](https://home.openweathermap.org/api_keys).
There should be one already created, your default API key. Copy that key and store it in a file
in this repository called `secrets.sh`. This file is going to contain our API tokens.

```
touch secrets.sh
```

Open the file and inside it, create an environment variable for the OpenWeather API key.

```
export OPENWEATHER_API_KEY=<your key goes here>
```

**Note:** You explicitly do not want to check your secrets file into Github.
You don't want any of your credentials stored in Git, because they are your personal
access tokens for the API.

### Signing up for Twilio

Go to the [Twilio sign up page](https://www.twilio.com/try-twilio) and create an account.
You'll be asked to enter your phone number and verify it.

Once you've verified your account, you'll land on your [dashboard](https://www.twilio.com/console).
Here, you can create a new project to test the Twilio functionality. Your new project
will be in trial mode and will have a small amount of preloaded credit on it to
play around with.

[Create a new project](https://www.twilio.com/console/projects/create). Once you've
created it, you should be sent back to your dashboard and see the new project.
This dashboard will also list a few credentials. You want to copy the `account sid`
and `auth token`. Paste those into `secrets.sh` as well, underneath your OpenWeather
API key.

```
export OPENWEATHER_API_KEY=<your key goes here>
export TWILIO_ACCOUNT_SID=<your account sid goes here>
export TWILIO_AUTH_TOKEN=<your auth token goes here>
```

You'll also need to create a Twilio number for this project. On the main
dashboard page for the Twilio project, click the "Get a Trial Number" button.
It should pop up a number that you can use for the project. This is the number
that all your text messages will be sent from.

Copy this number, and put it in secrets.sh.

```
export TWILIO_SENDER_NUMBER=<your twilio number here>
# example format: 15551234567
```

Finally, add the phone number that you used when signing up for your Twilio
account. This will be the number that we send SMS messages to for this
project, while it's still in a trial phase.

```
export TWILIO_RECEIVER_NUMBER=<your personal hone number, verified with Twilio>
```

## Scheduling

Now that we have the script working, let's talk about different ways to
automate this.

### Version 1: Using Cron

`cron` is a job scheduler for Unix-like computer operating systems.
It can be used to schedule programs to run automatically at specified
times or intervals.

Oftentimes cron is used for important periodic tasks like generating
backups, periodically deleting unnecessary files, and doing other
system maintenance tasks.

#### Vocab
`cron` is the software
A `cron job` is a task that's been scheduled to run at a specific interval
A `crontab` is a file that lists the existing `cron jobs`


### Version 2: Using Python Schedule library

There are several python libraries to allow scheduling programs.
[`schedule`](https://pypi.org/project/schedule/) is one of those.


### Version 3: Using Celery

Celery is a distributed task queue for python. This is the most involved
of the different options listed.

https://github.com/celery/celery
