#!/usr/bin/env python3
#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class EsunMailHelper:
    def __init__(self, sender, host, port):
        '''Constructor'''
        self.__sender = sender
        self.__host = host
        self.__port = port
        
    def send(self, receivers, subject, body):
        message = MIMEText(body, 'plain', 'utf-8')
        message['From'] = Header("CRV PMO通知信件", 'utf-8') 
        #message['To'] =  Header("To", 'utf-8')
        
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP(host = self.__host, port= self.__port)
            smtpObj.sendmail(self.__sender, receivers, message.as_string())
            print("mail send success")
        except smtplib.SMTPException:
            print("Error: mail failure")

    