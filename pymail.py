import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyttsx3
import speech_recognition as sr

email_list = {
    'jai':'email1',
    }
listener = sr.Recognizer()

def talk(text):
    pyttsx3.speak(text)

def get_info():
    try:
        with sr.Microphone() as source:
            print('I am listening..')
            talk('I am listening')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except:
        print("Cant listen")
        talk("Cant listen")


def hear_mail(N):
    try:
        user = 'sample2021email@gmail.com'
        password = '*********'
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(user, password)
        mail.select("Inbox")
        data = mail.search(None, 'ALL')
        mail_ids = data[1][0]
        id_list = mail_ids.split()
        latest_email_id = int(id_list[-1])
    except:
        print("No new Mails")
        talk("No new Mails")
        return

    for i in range(latest_email_id,latest_email_id-N, -1):
        data = mail.fetch( str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                if msg.is_multipart():
                    mail_content = ''
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = msg.get_payload()
                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')
                print('Content -' + mail_content)
                talk('From : ' + email_from + '\n')
                talk('Subject : ' + email_subject + '\n')
                talk('Content -' + mail_content)

    mail.close()

def send_mail(rec,Messagee,subject):
    try:
        sender = 'sample2021email@gmail.com'
        password = '*********'
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = rec
        message['Subject'] = subject
        message.attach(MIMEText(Messagee, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender, password)
        text = message.as_string()
        session.sendmail(sender, rec,text)
        session.quit()
    except:
        print("Sorry unable to send email")
        talk("Sorry unable to send email")

def newmail():
    try:
        talk("Say the email id whom you would like to send a mail")
        email_id=get_info()
        a=email_id.replace(' ','')
        print('What is the subject of the email')
        talk('What is the subject of the email')
        subject = get_info()
        print('What is the content of the email')
        talk('What is the content of the email')
        message = get_info()
        send_mail(a, message, subject)
    except:
        print("Invalid info")
        talk("Invalid info")

def get_email_info():
    try:
        talk('To whom you would like to send the mail')
        name = get_info()
        receiver = email_list[name]
        print(receiver)
        print('What is the subject of the email')
        talk('What is the subject of the email')
        subject = get_info()
        print('What is the content of the email')
        talk('What is the content of the email')
        message = get_info()
        send_mail(receiver,message,subject)
        print("Mail sent to "+name)
        talk("Mail sent to " + name)
    except:
        print("Invalid Name")
        talk("Invalid Name")

def main():
    print("Hello I am your Email Assistant")
    talk("Hello I am your Email Assistant")
    command=''
    while(command!='exit'):
        print("Say send to send an email , Say listen to listen latest email , Say exit to exit email assistant")
        talk("Say send to send an email , Say listen to listen latest email , Say exit to exit email assistant")
        command=get_info()
        if(command=='send'):
            print("Say contact to send email to existing contact say new to send email to a new person")
            talk("Say contact to send email to existing contact say new to send email to a new person")
            cmdd=get_info()
            if (cmdd=="contact"):
                get_email_info()
            else:
                newmail()
        elif(command=='listen'):
            print("Say the number of emails you would like to listen")
            talk("Say the number of emails you would like to listen")
            try:
                N=int(get_info())
                hear_mail(N)
            except:
                print("Sorry Wrong Input")
                talk("Sorry Wrong Input")
        elif(command=='exit'):
            print('Bye')
            talk('Byee')
        else:
            print("Cant recognise command please try again")
            talk("Cant recognise command please try again")

main()
