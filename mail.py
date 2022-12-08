import smtplib
 
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s.starttls()
 
# Authentication
s.login("0007Asta@gmail.com", "Kandarp@1234")
 
# message to be sent
message = "hello"
 
# sending the mail
s.sendmail("009kandarp@gmail.com", "009kandarp@gmail.com", message)
 
# terminating the session
s.quit()