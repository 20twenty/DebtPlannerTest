import imaplib
import email

def get_object():
    obj = imaplib.IMAP4_SSL('imap.gmail.com')
    obj.login('stiply.tone@gmail.com', 'debtPayoff!')
    obj.select("inbox")
    return obj

def get_code():
    obj = get_object()
    typ, data = obj.search(None, 'ALL')
    for num in data[0].split():
        typ, data = obj.fetch(num, '(RFC822)')
        msg = data[0][1]
        msg_object = email.message_from_string(msg)

        if msg_object.get_content_maintype() == 'multipart':
            for part in msg_object.walk():       
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                else:
                    continue
    obj.close()
    obj.logout()
    text_find = 'validation code into the application: '
    start_position = body.index(text_find) + len(text_find)
    return body[start_position: start_position + 6]
    
def mark_seen():
    obj = get_object()
    typ, data = obj.search(None,'UnSeen')
    if data[0] != '':
        obj.store(data[0].replace(' ',','),'+FLAGS','\Seen')
    obj.close()
    obj.logout()    
    
def wait_email(timeout):
    i = 0
    obj = get_object()
    while obj.search(None,'UnSeen')[1][0] == '' and i < timeout:
        i = i + 1
        obj = get_object()
    obj.close()
    obj.logout()