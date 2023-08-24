# Python Email Trading Automation Requirements Document

## Overview

The Python Email Trading Automation script is designed to automate trading actions based on email notifications. The script monitors a Gmail inbox for specific email subjects, extracts relevant information, and triggers trading actions accordingly.

## requirements
pip install -r requirements.txt


## Functional Requirements

1. **Open NinjaTrader Application**
   - The script must be able to open the NinjaTrader application using automated GUI interactions.

2. **Perform Buy Action**
   - The script must perform a "buy" action by executing a specified Node.js script.
   - The trading action must be triggered based on email notifications with specific subjects.
   - The subject of the email should contain the term "BOUGHT" and "MNQ".

3. **Perform Sell Action**
   - Similar to the "buy" action, the script must perform a "sell" action based on specific email subjects.
   - The subject of the email should contain the term "SOLD" and "MNQ".

4. **Node.js Script Execution**
   - The script should be able to execute Node.js scripts specified by their file paths.
   - The executed Node.js scripts are responsible for actual trading actions.

5. **Email Inbox Monitoring**
   - The script must continuously monitor the Gmail inbox for new and unread emails.
   - Unread emails are identified by the UNSEEN flag.

6. **Email Processing**
   - The script should process email notifications and extract relevant information from the subject line.
   - The extracted information includes the number of shares to be traded.

7. **Flagging Processed Emails**
   - Processed emails that trigger trading actions should be flagged to prevent duplicate processing.
   - Flagging involves adding or removing flags (FLAGA, FLAGB, etc.) to emails.

8. **Graceful Exit**
   - The script should run continuously but allow for a graceful exit when needed.

## Non-Functional Requirements

1. **Usability and GUI Interaction**
   - The script should provide automated GUI interactions to open NinjaTrader.
   - The GUI interactions should be intuitive and efficient.

2. **Stability and Reliability**
   - The script should handle exceptions and errors gracefully to ensure stability.
   - Trading actions should be triggered reliably based on email notifications.

3. **Efficiency and Performance**
   - The script should execute trading actions and email processing with minimal delay.
   - Performance optimizations should be considered to reduce execution time.

4. **Security**
   - Sensitive information like email credentials and file paths should be securely managed.
   - Access to the Gmail account and trading actions should be secured.

## Dependencies

1. **Python Modules**
   - `email`: For email processing and parsing.
   - `imaplib`: For interacting with the IMAP server.
   - `os`: For executing Node.js scripts and system operations.
   - `time` and `datetime`: For handling time-related operations.
   - `pyautogui`: For automated GUI interactions.

## Conclusion

The Python Email Trading Automation script provides an automated solution for executing trading actions based on email notifications. The script interacts with the NinjaTrader application, performs buy and sell actions, and extracts relevant information from email subjects. By continuously monitoring the Gmail inbox, the script enables efficient and automated trading operations.

---

Please customize the requirements document according to your project's specific needs and any additional details you'd like to include. This document is intended to provide a foundation for your project's requirements and can be expanded upon to include more details as necessary.