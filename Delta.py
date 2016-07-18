# Import all libraries needed for the tutorial

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
import pandas as pd 
import numpy as np
import csv
import os as os
import glob
import json
import requests
import smtplib
import base64
import email.encoders as Encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import time

timeVar = time.strftime('%X %x')
header = ["IP Address", "DNS Name", "NetBios Name", "Asset Label", "Asset Criticality", "Operating System", "Asset Owner", "Workgroup", "Service Name", "Service Port", "Protocol", "Banner"]
l=[]
sorted_list = sorted(glob.iglob('*.csv'), key=os.path.getctime)
newFile = sorted_list[-1]#get the newest CSV file in the directory
oldFile = sorted_list[-2]#get the 2nd newest CSV file in the directory

def main():
    csvDiff()
    makeCsv()
    #makeJson()
    email("hannanmartin@gmail.com",
   "New Connections " + str(timeVar),
   "This is a file containing a list of new connections to the server.",
   "report/report.csv")
    #post()


#This function reads in 2 CSV files and determines the difference
def csvDiff():
    f = open(newFile, 'r')
    csv_f = csv.reader(f)
    old=set(pd.read_csv(oldFile, index_col=False, header=None)[0]) #reads the csv, takes only the first column and creates a set out of it.
    new=set(pd.read_csv(newFile, index_col=False, header=None)[0]) #same here
    diff = new - old
    #Convert the diff set into a list
    diff=list(diff)
    #print(diff)
    for row in csv_f:
        if row[0] in diff:
            l.append(row)


def makeJson():
    csvfile = open('report/report.csv', 'r')
    jsonfile = open('json.json', 'w')
    reader = csv.DictReader(csvfile, header)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')



def makeCsv():
        toCsv = open('report/report.csv','w')
        wr = csv.writer(toCsv, delimiter=',')
        wr.writerow(header)
        wr.writerows(l)
        toCsv.close()


def post():
    
    data = []
    with open('json.json') as f:
        for line in f:
            data= json.loads(line)
            url = 'https://hooks.slack.com/services/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'
            payload= {"text" : "Email sent to admin! Please check email!"}
            r = requests.post(url, json=payload)
            print(r)

def email(to, subject, text, attach):

    gmail_user = "testingthetestymctest@gmail.com"
    gmail_pwd = "Bellharbour2016"
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()


if __name__ == "__main__": main()