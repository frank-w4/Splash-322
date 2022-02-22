#!/usr/bin/env python
# coding: utf-8

# # Project Splash

# Install needed Python libraries

# In[ ]:


get_ipython().system('pip3 install numpy')
get_ipython().system('pip3 install pyserial')
get_ipython().system('pip3 install matplotlib')
get_ipython().system('pip3 install datetime')


# Import necessary libraries

# In[12]:


import serial
import numpy as np
import matplotlib.pyplot as plt
import sys

import smtplib, ssl
from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime



N = 200000  # number of samples to collect | limit to the system before mandatory reset
i=0
x=np.zeros(N)
y=np.zeros(N)
i=0

low_count = 0
up_count = 0

dist_thresh = 800
inch_dist_thresh = dist_thresh/148
formatted_thresh = "{:.2f}".format(inch_dist_thresh)

arduino = serial.Serial(port='/dev/cu.usbmodem142201', baudrate=9600, timeout=.1)
arduino.close()
arduino.open()

while i < N:
    data = arduino.readline()
    if data:
        tokens = data.decode().split(',')
        y[i] = float(tokens[0])
        x[i] = float(tokens[1])
        i += 1
        distance = float(tokens[0])
        print(distance)
        
        if distance < dist_thresh:
            up_count+=1
            low_count=0
            print("up_count")
            print("low_count reset")
        if distance >= dist_thresh:
            low_count+=1
            print("low_count added one")
        if low_count==2:
            up_count=0
            print("up_count reset")
        print(" . . . ")
        print("low_count = " + str(low_count))
        print("up_count = " + str(up_count))
        if low_count==3:  
            print('firing email')
            port=465
            context = ssl.create_default_context()
            EMAIL_ADDRESS = 'coverletterwriter@gmail.com'
            EMAIL_PASSWORD = 'pythonemail'
            now = datetime.now()
            datetime_subject_line = now.strftime("%m/%d/%Y @ %H:%M")
            formatted_dist = "{:.2f}".format(distance/148)
            
            msg = MIMEMultipart()
            msg['Subject'] = 'Splash Device Notification - ' + datetime_subject_line
            subject = 'Splash Device Notification - ' + str(datetime_subject_line)
            msg['From'] = EMAIL_ADDRESS
            from_txt = EMAIL_ADDRESS
            msg['To'] = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com']
            to_txt = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com']
            # to_txt = ['whitfd18@wfu.edu', 'coverletterwriter@gmail.com', 'aspiers10@gmail.com', 'paucavp@wfu.edu']
            body_txt = """
Customer,

Your plants have crossed over your distance threshold of """ + str(formatted_thresh) + """ inches.

Your Splash device is currently reading """ + str(formatted_dist) + """ inches. 
    
Please water your plant! 
    
Have a great day.

        -Splash Team
        

Sent on """ + str(datetime_subject_line)
            
            # email_txt = """From: """ + from_txt + """
    # To: """ + ", ".join(to_txt) + """
    # Subject: """ + subject + """
    
    # """ + body_txt
            email_txt = body_txt
    
            msg.attach(MIMEText(body_txt))

            # msg = msg.as_string()
            sent = 0
            try:
                print(subject)
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                print('started tls')
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                print("logged in")
                server.sendmail(EMAIL_ADDRESS, to_txt, email_txt)
                server.quit()
                print("Email sent successfully")
                sent = 1
            except:
                print("Email could not be sent...")
            if sent == 1:
                sys.exit("Success")
            else:
                sys.exit("didn't send")
            up_count = 0
            low_count = 0
            sent = 0
        

arduino.close()




