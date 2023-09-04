import datetime
import email
import imaplib
import os
import time
from time import sleep
import pyautogui
import base64


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
buy_path = "C:\\Users\windows\Documents\Python_Ninja_Connector/appBuy.js"
sell_path = "C:\\Users\windows\Documents\Python_Ninja_Connector/appSell.js"

# buy x=4296, y=266
# sell x=4556, y=258

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'yuval2604@gmail.com'
password = 'udxevmpjelxwqhvg'

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("yuval2604@gmail.com", "udxevmpjelxwqhvg")  # Replace with your email and password

mail.select("inbox")
result, data = mail.search(None, 'UNSEEN')

All_Users = ['FLAGA', 'FLAGB', 'FLAGC']
Own_User = 0
new_list = All_Users[:Own_User] + All_Users[Own_User + 1:]


def extract_number_shares(subject):
    words = subject.split()
    number_index = next((i for i, word in enumerate(words) if not word.isalpha()), None)
    shares = words[number_index]

    return shares

def check_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("yuval2604@gmail.com", "udxevmpjelxwqhvg")  # Replace with your email and password

    mail.select("inbox")
    result, data = mail.search(None, 'UNSEEN')
    #print("Connection time", datetime.datetime.now())
    if result == 'OK':
        email_ids = data[0].split()
        print(data[0], email_ids)
        for i in new_list:
            LoopEmailIDsFirst(email_ids, '+FLAGS', new_list)

    result, data = mail.search(None, 'KEYWORD FLAGA')
    if result == 'OK':
        email_ids = data[0].split()
        LoopEmailIDsFirst(email_ids, '-FLAGS', All_Users[Own_User])

    mail.logout()


def decode_subject(encoded_subject):

    # Decode the subject
    decoded_subject = ""
    parts = encoded_subject.split("?=")
    for part in parts:
        if part.startswith("=?UTF-8?B?"):
            encoded_text = part[len("=?UTF-8?B?"):].strip()
            decoded_text = base64.b64decode(encoded_text).decode("utf-8")
            decoded_subject += decoded_text

    return (decoded_subject)


def LoopEmailIDsFirst(email_ids, flagsOnOff, flagSig):
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        if result == 'OK':
            raw_email = msg_data[0][1].decode('utf-8')
            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_subject(msg["subject"])
            print(subject)
            if "BOUGHT" in subject and "MNQ" in subject:
                mail.store(email_id, flagsOnOff, flagSig)
                print("Buy", msg["subject"])
                buy()

            if "SOLD" in subject and "MNQ" in subject:
                mail.store(email_id, flagsOnOff, flagSig)
                print("Sell", msg["subject"])
                sell()


while True:
    try:
        check_email()
        time.sleep(2)

    except Exception as e:
        print("WOW ERROR !!!!!!!", e)
        time.sleep(3)
