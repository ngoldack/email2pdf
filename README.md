# Email2Pdf

An email to pdf downloader written in python.

## Introduction

Docker container for downloading emails in pdf-format. 
It scans an imap-folder in an defined interval and then downloads it with all pdf-attachments.
If attachments were found, then it will merge those with the email to one single pdf.

## Use-cases

I use it for invoices that i want to be persisted in my DMS (Paperless). 

## Using

The easiest way is to use the docker-compose:

1. Edit the docker-compose-template.yml to your needs:
    - IMAP_SERVER = Your imap server address. Google is your friend.
    - IMAP_USERNAME = Your imap username
    - IMAP_PASSWORD = Your imap password
    - IMAP_INPUT_FOLDER = The imap folder, which is watched
    - IMAP_OUTPUT_FOLDER = The imap folder which the processed mails are moved to
    - IMAP_SCAN_INTERVAL = The interval in which the folder is watched/scanned

2. Save this file to docker-compose.yml

3. Start the file with docker-compose up (Use docker-compose up -d for detached-mode)

4. Enjoy!