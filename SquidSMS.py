# Author: https://github.com/Namelocms
# Last updated: 10/23/2024
# GitHub Repository: https://github.com/Namelocms/Squid_SMS
# Copyright (c) 2024 Sean Coleman

import smtplib as smt
import logging as log

class SquidSMS:
    def __init__(self, email, password):
        # Cellular Service Providers
        self.CARRIERS = {
            'att': '@mms.att.net',
            'Att': '@mms.att.net',
            'ATT': '@mms.att.net',

            'att1': '@txt.att.net',
            

            'tmobile': '@tmomail.net',
            'Tmobile': '@tmomail.net',
            'TMobile': '@tmomail.net',
            'TMOBILE': '@tmomail.net',

            'verizon': '@vtext.com',
            'Verizon': '@vtext.com',
            'VERIZON': '@vtext.com',
            'Ve': '@vzwpix.com',
            'Msv': '@mypixmessages.com',

            'sprint': '@page.nextel.com',
            'Sprint': '@page.nextel.com',
            'SPRINT': '@page.nextel.com',

            'tmobile1':'@voicestream.net',
            'Tmobile2':'@voicestream.net',
            'Tmobile3':'@voicestream.net',
            'Tmobile4':'@voicestream.net',

            'uscc': '@email.uscc.net',
            'sprintpcs': '@messaging.sprintpcs.com',
            'metropcs': '@mymetropcs.com',

        }

        # Email to use in sending the SMS
        self.AUTH_EMAIL = email

        # App Password (not email password) for 'AUTH_EMAIL'
        self.AUTH_PASS = password

        # Email + Password used to send message
        self.auth = (self.AUTH_EMAIL, self.AUTH_PASS)

    # Connect to the SMTP server
    def connect(self):
        try:
            # Establish a secure session with gmail's outgoing SMTP server using your gmail account
            server = smt.SMTP("smtp.gmail.com", 587)
            server.starttls()
            if server.login(self.auth[0], self.auth[1]):
                return server
            else:
                raise smt.SMTPAuthenticationError
        except smt.SMTPAuthenticationError:
            log.error('Error connecting to the server (check credentials)')
            return server.quit()  # end server connection


    def send(self, server, phone_number, carrier, message, bcc=None):
        """
        Send an email/SMS message.
        :param server: Active SMTP server connection.
        :param phone_number: Phone number of the primary recipient.
        :param carrier: Carrier of the primary recipient.
        :param message: Email content.
        :param bcc: List of additional BCC recipients (optional).
        :return: True if the message was sent successfully, False otherwise.
        """
        if server is None:
            log.error('Server is not connected, check email and app password')
            return False

        # Validate the phone number and carrier
        if not self.check_phone_number(phone_number) or not self.check_carrier(carrier):
            log.error('Issue with phone number or carrier')
            return False

        # Convert phone_number and carrier into recipient email address
        recipient = f"{phone_number}{self.CARRIERS[carrier]}"
        bcc_recipients = bcc or []
        all_recipients = [recipient] + bcc_recipients

        # Prepare the message
        try:
            server.sendmail(self.auth[0], all_recipients, message)
            return True
        except smt.SMTPException as e:
            log.error(f"Send failed: {e}")
            return False
    @staticmethod
    def disconnect(server):
        try:
            server.quit()
        except AttributeError:
            pass

    @staticmethod
    def check_phone_number(phone_number):
        if len(phone_number) != 10:
            log.error('Phone number length not 10')
            return False
        try:
            int(phone_number) # is number?
            return True
        except ValueError:
            log.error('Phone number contains non-numerical character(s)')
            return False

    def check_carrier(self, carrier):
            if carrier in self.CARRIERS:
                return True
            log.error('Carrier does not exist')
            return False
