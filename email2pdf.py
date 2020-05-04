import os
from PyPDF2 import PdfFileMerger
from chilkat import CkEmail
from imap_tools import MailBox
import pdfkit
import time

IMAP_SERVER = os.environ['IMAP_SERVER']
IMAP_USERNAME = os.environ['IMAP_USERNAME']
IMAP_PASSWORD = os.environ['IMAP_PASSWORD']
IMAP_INPUT_FOLDER = os.environ['IMAP_INPUT_FOLDER']
IMAP_OUTPUT_FOLDER = os.environ['IMAP_OUTPUT_FOLDER']
IMAP_SCAN_INTERVAL = int(os.environ['IMAP_SCAN_INTERVAL'])

OUTPUT_DIR = "/output/"
TMP_DIR = "/tmp/"

ALLOWED_TYPES = [
    "application/pdf"
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
while True:
    print("Starting!")
    with MailBox(IMAP_SERVER).login(IMAP_USERNAME, IMAP_PASSWORD, initial_folder=IMAP_INPUT_FOLDER) as mailbox:
        for mail in mailbox.fetch():
            print("Processing Message: " + mail.subject)
            if not os.path.exists(TMP_DIR + mail.subject + "/attachments/"):
                os.makedirs(TMP_DIR + mail.subject + "/attachments/")

            for attachment in mail.attachments:
                if attachment.content_type in ALLOWED_TYPES:
                    print("Processing attachment: ", attachment.filename, " | Type: ", attachment.content_type)
                    with open(TMP_DIR + mail.subject + "/attachments/" + attachment.filename, "wb") as attachment_file:
                        attachment_file.write(attachment.payload)

            with open(TMP_DIR + mail.subject + "/" + mail.subject + ".eml", "w") as file:
                file.write(mail.obj.as_string())

            print("Converting Email: eml to html")
            eml = CkEmail()
            success = eml.LoadEml(TMP_DIR + mail.subject + "/" + mail.subject + ".eml")
            if success is False:
                print(eml.lastErrorText())
                exit(-1)
            else:
                with open(TMP_DIR + mail.subject + "/" + mail.subject + ".html", "w") as file:
                    file.write(eml.body())

            print("Converting Email: html to pdf")
            pdfkit.from_file(TMP_DIR + mail.subject + "/" + mail.subject + ".html",
                             TMP_DIR + mail.subject + "/" + mail.subject + ".pdf")

            merger = PdfFileMerger()
            merger.append(TMP_DIR + mail.subject + "/" + mail.subject + ".pdf")
            for pdf in os.listdir(TMP_DIR + mail.subject + "/attachments/"):
                if pdf.endswith(".pdf"):
                    merger.append(TMP_DIR + mail.subject + "/attachments/" + pdf)

            merger.write(OUTPUT_DIR + mail.subject + ".pdf")

        print("Moving all mails to IMAP_OUTPUT folder")
        mailbox.move(mailbox.fetch(), IMAP_OUTPUT_FOLDER)

    print("Finished!")

    time.sleep(IMAP_SCAN_INTERVAL)

