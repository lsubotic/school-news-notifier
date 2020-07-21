from email.message import EmailMessage
from bs4 import BeautifulSoup
import pandas as pd
import requests
import smtplib
import imghdr
import csv
import sys
import os



# Constants
SEND_EMAIL = 'send.email@example.com' 
EMAIL_PASSWORD = 'testpass123'  # Sending mail address pass
RECV_EMAIL = 'recv.email@example.com'  # Recieving mail address



def get_news():
    """
    Scrapes the site
    """
    url = 'http://www.ets-zemun.edu.rs/vesti.html'

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,sr;q=0.8,hy;q=0.7,bs;q=0.6',
        'Accept-Encoding': 'gzip, deflate'
    }

    try:
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        r.encoding = 'utf-8'  # Encoding must be utf-8 because of cyrilic
    except:
        print('Error')
        return

    soup = BeautifulSoup(r.text, 'lxml')
    
    header = soup.select_one('#content  article > header')
    if header:
        try:
            title = header.select_one('h2 > a').get_text(strip=True)
            subtitle = header.find('p').get_text(strip=True)

            if scraped_title == title:
                print('There are no news')
                return
                       
            print('Save')
            csv_writer.writerow([title, subtitle])  # save

            print('Sending Message')
            send_message(title, subtitle)  # send message
        except:
            pass


def send_message(title, subtitle):
    """
    Sending the message through gmail
    """
    msg = EmailMessage()
    msg['Subject'] = title
    msg['From'] = SEND_EMAIL
    msg['To'] = RECV_EMAIL
    msg.set_content(subtitle)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SEND_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)


def execute():
    """
    Reads the .csv file and checks if the latest news article has changed, updates the .csv file if yes
    """
    global scraped_title, csv_writer
    scraped_title = ''
    
    filename = 'news.csv'
    
    file_exists = os.path.exists(filename)
        
    with open(filename, 'a', errors='ignore', newline='') as f:
        csv_writer = csv.writer(f)
        
        if file_exists:
            df = pd.read_csv(filename)
            if not df.empty:
                scraped_title = df['title'].iloc[-1]
        else:
            csv_writer.writerow(['title', 'subtitle'])
        
        # Run get news
        get_news()
        

###############################
execute()
###############################






