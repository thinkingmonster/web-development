import datetime
import json
import smtplib
import time
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
counter = 0
while True:
    area_pin = 560076
    # The mail addresses and password
    sender_address = '**********@gmail.com'
    sender_pass = '**********'
    receiver_address = '**********@gmail.com'

    today = datetime.datetime.today().strftime('%d-%m-%Y')
    base_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode='
    vaccination_url = base_url + str(area_pin) + '&date=' + today

    webUrl = urllib.request.urlopen(vaccination_url)
    data = webUrl.read()
    string_data = data.decode('utf8').replace("'", '"')
    my_json = json.loads(string_data)


    def send_email(subject, body_msg):

        # Create Email
        mail_content = body_msg
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()


    centers = my_json["centers"]
    all_center_details = []
    for center in centers:
        details = {}
        details["name"] = center['name']
        details["block_name"] = center['block_name']
        details["min_age_limit"] = center['sessions'][0]['min_age_limit']
        details["available_capacity"] = center['sessions'][0]['available_capacity']
        all_center_details.append(details)

    # Find my target centers
    available_centers = []
    for details in all_center_details:
        if details['min_age_limit'] == 18 and details['available_capacity'] > 0:
            available_centers.append(details)

    final_message = ''''''
    for data in available_centers:
        subject = 'Vaccination found'
        message = '''\nCenter Details: \n\n Center_name: {} \n age_limit: {} \n Capacity: {}\n\n'''.format(data['name'],
                                                                                                         data[
                                                                                                             'min_age_limit'],
                                                                                                         data[
                                                                                                             'available_capacity'])
        final_message += message

    if len(available_centers) > 0:
        send_email(subject, final_message)
    counter += 1
    print('\n-----------------------------\n{}: Checked on {}: {}\n-----------------------------'.format(counter,today,final_message))
    time.sleep(1800)
