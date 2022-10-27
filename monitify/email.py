import email
import imaplib
import json


def check_email(host: str, user: str, password: str, file_path: str) -> list[str]:
    last_inbox = []
    with open(file_path, "r") as f:
        last_inbox = json.load(f)
    imap = imaplib.IMAP4_SSL(host)
    imap.login(user, password)
    imap.select("INBOX")
    (_, data) = imap.search(None, "ALL")
    new_inbox = str(data[0], "utf-8").split()
    new_mails = []
    for uid in [item for item in new_inbox if item not in last_inbox]:
        new_mails.append(_fetch_mail(imap, uid))
    if new_mails:
        with open(file_path, "w+") as f:
            json.dump(new_inbox, f)
    return new_mails


def _fetch_mail(imap: imaplib.IMAP4_SSL, id: str) -> str:
    (_, data) = imap.fetch(id, "(BODY.PEEK[HEADER])")
    msg = email.message_from_bytes(data[0][1])
    return f"{msg['from']}: {msg['subject']}"
