
import email
import imaplib
import os
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

fetched_imgs = {}

def getImages(user, pwd):
    try:
        imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
        typ, accountDetails = imapSession.login(user, pwd)
        if typ != 'OK':
            print('Not able to sign in!')
            raise
        
        imapSession.select('Inbox')
        typ, data = imapSession.search(None, 'UNSEEN')
        if typ != 'OK':
            print('Error searching Inbox.')
            raise
        
        # Iterating over all emails
        for msgId in data[0].split():
            typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
            if typ != 'OK':
                print('Error fetching mail.')
                raise
    
            emailBody = messageParts[0][1]
            raw_emailBody = emailBody.decode('utf-8')
            mail = email.message_from_string(raw_emailBody)
            source = mail["From"]
            fetched_imgs[source] = []
            for part in mail.walk():
        
                if part.get_content_maintype() == 'multipart':
                    # print part.as_string()
                    continue
                if part.get('Content-Disposition') is None:
                    # print part.as_string()
                    continue
                
                fileName = part.get_filename()
                fetched_imgs[source].append(os.path.join('/media/jatin/Work/Work/FaceRecognition/attachments', fileName))
                print(fileName)
                
                if bool(fileName):
                    filePath = os.path.join('/media/jatin/Work/Work/FaceRecognition/attachments', fileName)
                    if not os.path.isfile(filePath) :
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        print("Image saved.")
                        fp.close()
                        
        imapSession.close()
        imapSession.logout()
        
    except :
        
        print('Not able to download attachments.')

def reply(userName, passwd, src, img, match):
    
    msg = MIMEMultipart() 
    msg['From'] = userName
    msg['To'] = src
    msg['Subject'] = "Face Recogniton request"
    body = match
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(img, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" %"image.jpg")   
    msg.attach(p)
    
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(userName, passwd)
    text = msg.as_string() 
    s.sendmail(userName, src, text) 
    s.quit() 