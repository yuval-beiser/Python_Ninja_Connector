import datetime
import email
import imaplib
import os
import time
from time import sleep
import pyautogui


def open_ninja():
    pyautogui.moveTo(1204, 2830, duration=1)
    pyautogui.click(1204, 2830)
    sleep(0.3)
    pyautogui.moveTo(1130, 2648, duration=1)
    pyautogui.click(1130, 2648)


def buy():
    # pyautogui.click(4802, 76)
    run_node_script(buy_path)
    # pyautogui.moveTo(4802, 76, duration=1)
    print("Buy")
    # buy


def sell():
    run_node_script(sell_path)
    # pyautogui.click(4998, 86)
    # pyautogui.moveTo(4998, 86, duration=1)
    print("Sell")


def run_node_script(script_path):
    return os.system(f"node {script_path}")


# Replace "path/to/your/node/appBuy.js" with the actual path to your Node.js script
buy_path = "C:/Users/Main/downloads/GmailNinjaMarketTrader/GmailNinjaMarketTrader/appBuy.js"
sell_path = "C:/Users/Main/downloads/GmailNinjaMarketTrader/GmailNinjaMarketTrader/appSell.js"

# buy x=4296, y=266
# sell x=4556, y=258

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'yuval2604@gmail.com'
password = 'udxevmpjelxwqhvg'

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("yuval2604@gmail.com", "udxevmpjelxwqhvg")  # Replace with your email and password


def check_email():
    mail.select("inbox")
    result, data = mail.search(None, 'UNSEEN')
    print("Connection time", datetime.datetime.now())
    if result == 'OK':
        email_ids = data[0].split()
        LoopEmailIDsFirst(email_ids, '+FLAGS', 'FLAGB')

    result, data = mail.search(None, 'KEYWORD FLAGA')
    if result == 'OK':
        email_ids = data[0].split()
        LoopEmailIDsFirst(email_ids, '-FLAGS', 'FLAGA')

    mail.logout()


def LoopEmailIDsFirst(email_ids, flagsOnOff, flagSig):
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        if result == 'OK':
            msg = email.message_from_bytes(msg_data[0][1])
            if "BOUGHT" in msg["subject"] and "MNQ" in msg["subject"]:
                mail.store(email_id, flagsOnOff, flagSig)
                print("Buy", msg["subject"])
                buy()

            if "SOLD" in msg["subject"] and "MNQ" in msg["subject"]:
                mail.store(email_id, flagsOnOff, flagSig)
                print("Sell", msg["subject"])
                sell()


while True:
    check_email()
    time.sleep(2)
