import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets

from .models import TempPassKey

from django.urls import reverse

def send_link(send_user):
    send_address = send_user.email
    auth_address = 'sherisshavedauth@gmail.com'
    domain = 'https://shavedice.grimedesign.com'

    message = MIMEMultipart()
    message['From'] = auth_address
    message['To'] = send_address
    message['Subject'] = 'Password reset'

    pass_key = str(secrets.token_urlsafe(16))
    pass_url = domain + str(reverse('inv_manage:forgotpassword')) + pass_key

    temp_link = TempPassKey(user = send_user, pass_key = pass_key)
    temp_link.save()

    message.attach(MIMEText('Click this link to reset your password: ' + 
    pass_url))

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.ehlo()
    s.starttls()
    s.login(auth_address, '417shaved')
    s.send_message(message)
    s.quit()

def test_key(pass_key):
    worked = False
    try:
        TempPassKey.objects.get(pass_key = pass_key)
        worked = True
    except:
        pass
    return worked

def new_password(pass_key, password):
    get_key = TempPassKey.objects.get(pass_key = pass_key)
    this_user = get_key.user
    this_user.set_password(password)
    this_user.save()
    get_key.delete()