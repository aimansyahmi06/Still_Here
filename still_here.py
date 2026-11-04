import logging
import os
import schedule
import datetime
import smtplib
from email.message import EmailMessage
import customtkinter as ctk

POPUP_TIME = "07:00"     # time in which the GUI will pop up every day as scheduled
DEADLINE_TIME = "08:00"  # no check-in by this time -> email the family
checked_in_today = False


def send_email(subject, body):
    email = EmailMessage()
    email["From"] = "asyahmi670@gmail.com"
    email["To"] = "asyahmi670@gmail.com"
    email["Subject"] = subject
    email.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15) as s:
            s.login(os.environ.get ("STILLHERE_EMAILADDRESS"), os.environ.get("STILLHERE_PASSWORD"))
            s.send_message(email)
    except (smtplib.SMTPException, OSError, KeyError) as error:
        print(f"Email failed: {error}")
        return False  # it did not work
    return True

def check_in():
    global checked_in_today
    first_time_today = not checked_in_today  # is this her first check-in today?
    checked_in_today = True
    now = datetime.datetime.now().strftime("%I:%M %p")
    message.configure(text=f"Thanks! Checked in at {now}")
    root.update()  # redraw the window now, before the slow email part
    if first_time_today:
        sent = send_email("StillHere: Grandma checked in",
                          f"Good news! Grandma checked in today at {now}.")
        if not sent:
            message.configure(text="Checked in, but couldn't tell your family. Please call them.")


def call_me():
    message.configure(text="Sending...")
    root.update()  # redraw the window now, before the slow email part
    now = datetime.datetime.now().strftime("%I:%M %p")
    sent = send_email("StillHere: Grandma asked you to call her",
                      f"Grandma asked you to call her at {now}.")
    if sent:
        message.configure(text="Done! Your family will call you.")
    else:
        message.configure(text="Couldn't send. Please phone your family.")


def show_window():
    global checked_in_today
    checked_in_today = False  # new day, nobody has checked in yet
    message.configure(text="Not checked in yet")
    root.deiconify()  # show the window again
    root.lift()  # bring it in front of other windows
    root.attributes("-topmost", True)  # keep it on top for a moment...
    root.after(3000, lambda: root.attributes("-topmost", False))


def check_missed():
    if not checked_in_today:
        sent = send_email("StillHere: Grandma hasn't checked in today",
                          f"Grandma hasn't checked in yet today. The deadline was {DEADLINE_TIME}.\n\n"
                          "Please try calling her.")
        if not sent:
            print("WARNING: the missed check-in email did NOT send!")


def check_schedule():
    schedule.run_pending()
    root.after(1000, check_schedule)

###############BUTTON SETTINGS####################################################################################
ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("StillHere")
root.geometry("460x600")
root.resizable(False, False)

title = ctk.CTkLabel(root, text="StillHere",
                     font=("Helvetica", 34, "bold"), text_color="#2e9e4f")
title.pack(pady=(30, 0))

subtitle = ctk.CTkLabel(root, text="Tap the green button every morning",
                        font=("Helvetica", 16), text_color="gray40")
subtitle.pack(pady=(0, 10))

message = ctk.CTkLabel(root, text="Not checked in yet",
                       font=("Helvetica", 22), wraplength=380, height=70)
message.pack(pady=10)

ok_button = ctk.CTkButton(root, text="I'm OK!",
                          font=("Helvetica", 40, "bold"),
                          width=380, height=150, corner_radius=28,
                          fg_color="#2e9e4f", hover_color="#237a3c",
                          command=check_in)
ok_button.pack(pady=10)

call_button = ctk.CTkButton(root, text="Call me",
                            font=("Helvetica", 24, "bold"),
                            width=380, height=70, corner_radius=20,
                            fg_color="transparent", border_width=3,
                            border_color="#2e6fd0", text_color="#2e6fd0",
                            hover_color="#e6eefb",
                            command=call_me)
call_button.pack(pady=(10, 20))
root.protocol("WM_DELETE_WINDOW", root.withdraw)  # close button = hide, not quit
schedule.every().day.at(POPUP_TIME).do(show_window)
schedule.every().day.at(DEADLINE_TIME).do(check_missed)
check_schedule()
root.mainloop()