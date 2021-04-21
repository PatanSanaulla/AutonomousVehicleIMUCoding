import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Define time stamp & record an image
pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
command = 'raspistill -w 1280 -h 720 -vf -hf -o ' +pic_time+ '.jpg'
os.system(command)

# Email information
smtpUser = 'vaccinebot786@gmail.com'
smtpPass = '809Tfinale'

# Destination email information
toAdd = ['spatan07@umd.edu', 'spatan07@terpmail.umd.edu']
fromAdd = smtpUser
subject = 'Image recorded at '+ pic_time
msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = fromAdd
#msg['To'] = toAdd
msg['To'] = ",".join(toAdd)
msg.preamble = "Image recorded at "+pic_time


#Email Text
body = MIMEText("Image recorded at "+ pic_time)
msg.attach(body)

#Attach image
fp = open(pic_time+'.jpg','rb')
img = MIMEImage(fp.read())
fp.close()
msg.attach(img)


#send email
s = smtplib.SMTP('smtp.gmail.com',587)

s.ehlo()
s.starttls()
s.ehlo()
print('reched here')
s.login(smtpUser, smtpPass)
s.sendmail(fromAdd, toAdd, msg.as_string())
s.quit()

print("Email delivered!")