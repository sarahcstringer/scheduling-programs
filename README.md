# Scheduling python programs different ways

Let's pretend that we want to run a program that sends a text with the
weather in your zipcode every morning.

After we've written the script, how do we set it up so that it runs
periodically without us needing to manually run it?

## Setting up the weather texting script

We'll first set up the example script that we want to run periodically.
The script is already written, but needs some setup to use the
two APIs that power the program.

### Getting started

- Create a virtual environment `python3 -m venv venv`
- Pip install the requirements: `pip3 install -r requirements.txt`

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

> **Note about secrets.sh:** You **do not want to check your secrets into Github.**
> You don't want any of your credentials stored in Git, because they'll remain in
> git history and you don't want other people to have your personal access tokens.
> In this repo, `secrets.sh` is already included in our `.gitignore` file, so it won't
> be checked in.

Open the `secrets.sh` file and inside it, create an environment variable for the OpenWeather API key.

```
export OPENWEATHER_API_KEY=<your key goes here>
```

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
project, while it's still in a trial phase. When your project is in trial mode, you can
only send Twilio messages to your own phone number.

```
export TWILIO_RECEIVER_NUMBER=<your personal hone number, verified with Twilio>
```

## Scheduling

Now that we have the script working, let's go through two different ways to
automate this script.

### Version 1: Using Cron

`cron` is a job scheduler for Unix-like computer operating systems.
It can be used to schedule programs to run automatically at specified
times or intervals.

Oftentimes cron is used for important periodic tasks like generating
backups, periodically deleting unnecessary files, and doing other
system maintenance tasks.

> **Note: Vocab**  
> `cron` is the software.
> A `cron job` is a task that's been scheduled to run at a specific interval.
> A `crontab` is a file that lists the existing `cron jobs`.

We can create a cron job that runs our python script every day at a specific
time.

Cron has a specific format for understanding schedules.
[Crontab guru](https://crontab.guru/) is a very helpful site that demonstrates
how to express different increments/times in the cron format.

The basic format is this:

```
* * * * *
```

There are five options. From left to right, the options represent:
minute, hour, day (of the month), month, day (of the week).

A cron job with the schedule `* * * * *` would mean it would run
"every minute of every hour of every day of every month, every day of the week."
Essentially, every minute.

Here are a few other examples:

```
0 3 * * 5  # runs at 3:00 every Friday
0 10 * * 1-5  # runs at 10:00 every day of the week Monday-Friday
*/5 * * * *  # runs every five minutes
30 */4 * * *  # runs at minute 30 every 4 hours
```

The operators `*`, `,`, `-`, and `/` allow more options in your cron expression.

- `*` means any value/always
- `,` specifies repetition. For example: `0 10 * * 1,3,5` means that this will
run at 10:00 on Monday, Wednesday, and Friday
- `-` specifies a range of values (as in the 1-5 example in the block above,
that signaled Monday-Friday)
- `/` specifies repetition over a certain interval. For example: `*/5 */4 * * *`
means to run every 5 minutes of every 4th hour.

For our purposes, we want our Python script to run every morning. So, the
schedule will look like this `0 9 * * *` (run at 9:00 every day).

Now that we have the schedule determined, we just have to tell cron what we
want it to do on that cadence.

The `crontab` command is how we'll edit the list of cron jobs our system has.
`crontab -e` allows you to edit your existing crontab or create a new one if
one doesn't already exist.

To open the crontab, run `crontab -e`. It will open in your system's default
text editor, such as `vim` or `nano`, or it will give you a choice of
which editor to open in if your system doesn't have a default set.

Now we'll put in the schedule that we want this to run on, followed
by the command we want it to run. We want it to go into our project
directory, activate the virtual environment, source the secrets file,
and run the `main.py` file.

```
0 10 * * * cd /path/to/this/directory/ && source venv/bin/activate && source secrets.sh && python3 main.py
```

Once you've added that to the file, it should be set to run. You can view
the tasks in your crontab with `crontab -l`.

If you want to remove the full file (note: this will get rid of the whole file),
you can use `crontab -r`.

To verify that this is actually working, let's edit the existing cron job
to run every 2 minutes, and validate that we start getting regular text messages.
To edit the file, run `crontab -e`.

```
*/2 * * * * cd /path/to/this/directory/ && source venv/bin/activate && source secrets.sh && python3 main.py
```

Once you save the file, you should start getting texts every two minutes.

After you've successfully verified, you can edit the cron job so that it goes back to a once-a-day
schedule.


### Version 2: Using Python Schedule library

There are several python libraries to allow scheduling programs.
[`schedule`](https://pypi.org/project/schedule/) is one of those.

The basic concept of `schedule` is that you give it a python function
to run and a schedule that you want it to run on, and then create a while True
loop and let `schedule` handle calling the function at the right time.

We have an example file already written. Open
[`schedule_example.py`](https://github.com/sarahcstringer/scheduling-programs/blob/master/schedule_example.py)
to view the sample.

The file needs three things:
1) A task to run.
2) A line or lines indicating when or how often to run that task.
3) A while True loop, where schedule handles running tasks when scheduled.

In our example, we import the task to run (the `main` function from main.py)
and give it the schedule to run every day at 10. There's also a commented out
line that sets the task to run every minute, which you can uncomment to see
the schedule working.

All we need to do is source our secrets into our environment, activate our virtual
environment, and run this file. As long as it's running, it will continue to call
the function at the appropriate time.

```
source secrets.sh
source venv/bin/activate
python3 schedule_example.py
```
