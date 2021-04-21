import imaplib
import email
import time

def checkEmail():
    
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('vaccinebot786@gmail.com', '809Tfinale')
    mail.list();
    
    count = 0
    
    while count < 60:
        try:
            #connect to inbox
            mail.select("inbox")
            
            #search for an unread email form user's email address
            result, data = mail.search(None, '(UNSEEN FROM "spatan07@terpmail.umd.edu")')
            #result, data = mail.search(None, '(UNSEEN FROM "ENPM809TS19@gmail.com")')
            
            print(result)
            print(len(data))
            
            ids = data[0] #data is the list of the emails
            id_list = ids.split()
            
            latest_email_id = id_list[-1] #get the last email
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            
            if data is None:
                print("Waiting ...")
                
            if data is not None:
                print("Process Initiated!")
                
        except IndexError:
            time.sleep(2)
            if count < 59:
                count = count + 1
                continue
            else:
                print("Gameover")
                count = 60
                
checkEmail()