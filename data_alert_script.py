#This python script reads from a config file 'config_file.txt' to read the content to execute which for example can be, subject of a mail, query, description etc.
#Make sure you write a config file to read from(pretty easy) for example file would have something like "query to be executed on your DB | Thresholds if you define(In case of data arrival) | Subject"
#In this case, this is how the txt file should look -> ´Query | LT | UT | Subject for Alerts´


import mysql.connector
import logging
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Adding Logger Module
logger = logging.getLogger(name='Alert mail')
logger.setLevel(logging.DEBUG)
print logger.name

logger.info("Logger Created")

logger_handler = logging.FileHandler('python_logging.log')
logger_handler.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.info('Completed configuring logger()!')

TOADDR = 'EMAILID1 EMAILID2 EMAILID3'
# CCADDR = ['EMAILID1', 'EMAILID2']
# If we are running in python then only un-comment this, In unix platform CC address can be taken care in TOADDR


def send_mail(subject, body):
    print subject
    print body
    try:
        process = subprocess.Popen('echo -e '+ str("'"+body+"'")+ '| mail -s '+str("'"+subject+"' ")+ TOADDR, stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print proc_stdout
        print "successfully sent the mail"
    except:
        print "failed to send mail"

# file containing alert records

with open('config_file.txt') as fil:                #(This file has | seperated contents that are read by this script in sequence of Z()s)
    for line in fil:
        content = line

        # Establish Database Connection
        cnx = mysql.connector.connect(user='user', password='password', host='00.00.00.00', database='dbname')
	cursor = cnx.cursor()

        print 'MySQL Connecting...'

        # Read line by line     from config_file
        z = content.split('|')

        if z[0].strip() == '#':
            break

        elif len(z) == 5:
            print 'From Else Block'
            query = z[0].strip()                    #(Customize the config_file.txt in this order of contents of Z[]s)
            lowerT = z[1].strip()
            upperT = z[2].strip()
            subject = z[3].strip()

            # Execute Query
            cursor.execute(query)

            for val in cursor:
                print 'Val is ', val
                if int(val[0]) < int(lowerT) or int(val[0]) > int(upperT):
                    body = 'Alert name : ' + subject + '\nAlert description : ' + z[4].strip() \
                           + '\nAlert query executed : ' + query + '\nAlert Query result : ' \
                           + ((str(val).strip('(),')) + '\nAlert lower threshold : ' + lowerT + '\nAlert upper threshold : ' + upperT)

                    print 'Before Send Mail'
                    send_mail(subject, body)
                    print 'After Send Mail'

        cursor.close()
        cnx.close()
        print 'Done..!'
