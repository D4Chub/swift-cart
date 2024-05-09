import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os 
from dotenv import load_dotenv

load_dotenv()

def send_mail(receiver_email, product_name, total_price, quantity, name):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv('MAIL')
    password = os.getenv('MAIL_PASSWORD')

    # Читаем содержимое HTML-файла
    with open("templates/mail.html", "r") as file:
        html_content = file.read()

    # Подставляем данные из запроса в HTML-шаблон
    html_content = html_content.replace("[[product_name]]", product_name)
    html_content = html_content.replace("[[quantity]]", str(quantity))
    html_content = html_content.replace("[[total_price]]", str(total_price))
    html_content = html_content.replace("[[name]]", name)

    # Создаем MIMEMultipart сообщение
    message = MIMEMultipart("alternative")
    message["Subject"] = "Заказ"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Создаем MIMEText объект с содержимым HTML файла
    part1 = MIMEText(html_content, "html")

    # Добавляем часть в сообщение
    message.attach(part1)

    # Создаем защищенное соединение с сервером и отправляем письмо
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
