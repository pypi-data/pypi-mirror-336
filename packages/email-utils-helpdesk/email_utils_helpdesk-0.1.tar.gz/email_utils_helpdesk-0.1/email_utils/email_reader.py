import email
from email.header import decode_header

def extract_email_content(mail, email_id):
    """Extract subject, sender, and body."""
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    if status != "OK": return None, None, None
    msg = email.message_from_bytes(msg_data[0][1])
    subject, encoding = decode_header(msg["Subject"])[0]
    sender = msg.get("From")
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
    print("✅ Extracted email content.")
    return subject, sender, body


def fetch_unread_emails(mail):
    """Fetch unread emails."""
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split() if status == "OK" else []
    print(f"✅ Found {len(email_ids)} unread emails.")
    return email_ids
