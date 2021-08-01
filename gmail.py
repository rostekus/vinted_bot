import smtplib




with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login('wobskna@gmail.com','wbh-Rtk-H26-F4B')

    sub = 'Hello'
    body = 'lol, first email'
    
    msg = f'Subject: {sub} \n\n{body}'
    smtp.sendmail('wobskna@gmail.com','wobskna@gmail.com', msg)