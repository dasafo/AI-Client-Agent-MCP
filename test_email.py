import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg['Subject'] = 'Test desde script manual'
msg['From'] = 'salas.forever@gmail.com'
msg['To'] = 'dsf@protonmail.com'
msg.set_content('Este es un correo de prueba enviado desde un script Python usando SMTP_SSL.')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('salas.forever@gmail.com', 'thtkwvyasfedqrbg')
    smtp.send_message(msg)

print("Correo enviado (si no hay excepción).")