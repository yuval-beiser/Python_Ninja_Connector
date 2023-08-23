
import datetime
import signal

import pyautogui
from time import sleep


def open_ninja():
    pyautogui.moveTo(1204, 2830, duration=1)
    pyautogui.click(1204, 2830)
    sleep(0.3)
    pyautogui.moveTo(1130, 2648, duration=1)
    pyautogui.click(1130, 2648)


def buy():
    pyautogui.click(4802, 76)

    pyautogui.moveTo(4802, 76, duration=1)
    print("Buy")



def sell():

    pyautogui.click(4998, 86)
    pyautogui.moveTo(4998, 86, duration=1)
    print("Sell")






# buy x=4296, y=266
# sell x=4556, y=258

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'yuval2604@gmail.com'
password = 'udxevmpjelxwqhvg'

import imaplib
import email
import time


def check_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("yuval2604@gmail.com", "udxevmpjelxwqhvg")  # Replace with your email and password

    mail.select("inbox")
    result, data = mail.search(None, 'UNSEEN')
    print("Connection time", datetime.datetime.now())
    if result == 'OK':
        email_ids = data[0].split()
        for email_id in email_ids:
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                if "BOUGHT" in msg["subject"] and "MNQ" in msg["subject"]:
                    mail.store(email_id, '+FLAGS', 'FLAGB')
                    print("Buy", msg["subject"])
                    # open_ninja()
                    # sleep(0.5)
                    buy()

                if "SOLD" in msg["subject"] and "MNQ" in msg["subject"]:
                    mail.store(email_id, '+FLAGS', 'FLAGB')
                    print("Sell", msg["subject"])
                    # open_ninja()
                    # sleep(0.5)
                    sell()

    result, data = mail.search(None, 'KEYWORD FLAGA')
    if result == 'OK':
        email_ids = data[0].split()
        for email_id in email_ids:
            print("Flagged")
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                if "BOUGHT" in msg["subject"] and "MNQ" in msg["subject"]:
                    mail.store(email_id, '-FLAGS', 'FLAGA')
                    print("Buy", msg["subject"])
                    # open_ninja()
                    # sleep(0.5)
                    buy()

                if "SOLD" in msg["subject"] and "MNQ" in msg["subject"]:
                    mail.store(email_id, '-FLAGS', 'FLAGA')
                    print("Sell", msg["subject"])
                    # open_ninja()
                    # sleep(0.5)
                    sell()

    mail.logout()


while True:
    check_email()
    time.sleep(2)