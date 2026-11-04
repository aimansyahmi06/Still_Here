# StillHere

A simple desktop check-in app for people who live alone. It shows two big buttons, and it emails a family member when something happens, so they don't have to wonder whether everything is okay.

> **StillHere is not an emergency service.** It only sends emails, and it only works while the computer is on and the app is running. In an emergency, call your local emergency number. A phone's Emergency SOS feature or a medical alert device is the right tool for that.

## What it does

- Shows a window with two large buttons: **I'm OK!!** and **Call me!**
- **I'm OK!!** records a check-in and emails the family: "Grandma checked in".
- **Call me!** emails the family right away: "Grandma asked you to call her".
- Every morning at a set time, the window pops up again.
- If there's no check-in by a set deadline, the app emails the family: "Grandma hasn't checked in today".
- If an email can't be sent (no internet, rejected login), the window says so, and the reason is printed in the console. It never fails silently.
- Closing the window only hides it, so the app keeps running in the background.

## How it works

| Part | What it does |
|---|---|
| `tkinter` | Draws the window and buttons |
| `schedule` | Runs the morning popup and the deadline check at set times |
| `smtplib` | Sends email through Gmail's SMTP server |
| `root.after(...)` | Runs a timer inside the window so the schedule is checked once a second without freezing it |

Everything is in one file, `still_here.py`.

## Requirements

- Python 3 (with `tkinter`, which comes with the installer from python.org; with Homebrew Python, run `brew install python-tk`)
- The `schedule` library
- A Gmail account with 2-Step Verification turned on, and an **app password**

## Setup

1. **Install the library**

   ```bash
   python3 -m pip install schedule
   ```

2. **Create a Gmail app password** at <https://myaccount.google.com/apppasswords>. It's different from your normal password. Treat it like a password, and never paste it into your code, chats or screenshots.

3. **Store the password in an environment variable.** Don't put it in the source code. In Terminal:

   ```bash
   export STILLHERE_APP_PASSWORD="your-16-character-app-password"
   ```

   In PyCharm, set it under **Run → Edit Configurations → Environment variables**.

4. **Run the app**

   ```bash
   python3 still_here.py
   ```

## Settings

At the top of `still_here.py`:

```python
POPUP_TIME = "07:00"     # the window pops up (24-hour clock, two-digit hour)
DEADLINE_TIME = "08:00"  # no check-in by this time -> email the family
```

The sender and recipient addresses are in `send_email`. Change the recipient to a family member's address.

To test quickly, set both times to a minute or two from now, close the window with its close button, and wait.

## Known limitations

- The app must be running. If the computer is off or the app is closed, nothing happens.
- The check-in is remembered only while the app is running. If it restarts, it forgets.
- It sends email only, with no text messages or calls.
- Only one recipient and one person are supported, and both are set in the code.
- It has only been tested on macOS.

## Roadmap

- [ ] Save the last check-in to a file so it survives restarts
- [ ] Move names, times and email addresses into a settings file
- [ ] Start automatically when the computer logs in
- [ ] Larger text and higher-contrast colors, tested with a real user

## What I learned

- Designing for failure: an app that tells people something must not fail silently.
- Keeping secrets (like passwords) out of source code.
- Debugging by isolating one variable at a time.