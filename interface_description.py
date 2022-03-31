# -*- coding: UTF-8 -*
import paramiko, sys, time, socket, string, re
from time import gmtime, strftime
import time, datetime
import base64
import os
import xlwt
import threading

from queue import Queue
import re
############################ VARIABLES ###############################
print("Etki Listesine hoşgeldiniz")
print("Şimdiye kadar yapılanların en iyisi")

line_break = "\r\n"
line_end = "\r"
vrp_cli_length = "screen-length 0 tempo"

while True:
    LDAP =  input("Lutfen calisma yapacak kullanici adini giriniz:  ")
    if not LDAP  == "":
        break

while True:
    password = input("Lutfen kullanıcı için pass giriniz:  ")
    if not password == "":
        break

while True:
    change = input("Lutfen Change numarası giriniz:  ")
    if not change == "":
        break

router=[]
while True:
    IP = input("IP adresini girebilir misiniz? Çıkmak için 1 e basınız:  ")
    if IP == "1":
        break
    else:
        router.append(IP)



print("Etki listesi çıkartılıyor...")



filetimestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filepath = os.getcwd()
LOGfile = xlwt.Workbook()

sheet1= LOGfile.add_sheet("Sheet1")
cols= ["VLAN", "DEVRE","MUSTERI"]
first =sheet1.row(0)
first.write(0,"VLAN")
first.write(1,"DEVRE")
first.write(2,"MUSTERI")


class SSH(object):

    def __init__(self):
        self.connections = []

    def execute_command(self, router, ldap_user, ldap_pass, route_command):
        """Connect to all hosts in the hosts list"""
        client = paramiko.SSHClient()
        # client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect("10.222.247.240", 2222, ldap_user, ldap_pass)
        # print ("could not open a connection to %s" ,router)
        except:
            print("could not open a connection to %s" % router)
            return

        chan = client.invoke_shell(width=200, height=0)
        buff = ""
        resp = ""
        i = 1
        IMT = []
        PROMPT = ">"

        for n40ip in router:
            print(n40ip)
            resp = ""
            buff = ""

            chan.send(n40ip + line_end)
            time.sleep(30)
            resp = chan.recv(999999999999)
            try:
                buff += resp.decode()
            except:
                print("can not decode")
                pass

            row2 = sheet1.row(i)
            if  "Authentication failed" in buff or "Timeout" in buff or "Cannot connect" in buff or "ress any key" in buff or "Search results;" in buff or "No device " in buff:

                resp = ""
                buff = ""
                chan.send(" " + line_end)
                time.sleep(2)
                print("Girilemeyen HI: {}".format(n40ip))

                row2.write(0, "Girilemeyen Router")
                row2.write(1, n40ip)
                i=i+1
                continue
            elif "[y/n]" in buff:
                resp = ""
                buff = ""
                chan.send("n" + line_end)
                time.sleep(2)
                resp = ""
                buff = ""
                print("Girilemeyen HI: {}".format(n40ip))
                row2.write(0, "Girilemeyen Router")
                row2.write(1, n40ip)
                i=i+1
                continue
            else:
                resp = ""
                buff = ""
                print(" %s a bağlandınız" %n40ip)
                chan.send(vrp_cli_length + line_end)
                while buff.find(">") == -1:
                    time.sleep(4)
                    resp = chan.recv(999999999999)
                    buff += resp.decode()
                    output = buff.split(line_break)

                resp = ""
                buff = ""

                chan.send(route_command + line_end)
                while buff.find(">") == -1:
                    time.sleep(4)
                    resp = chan.recv(99999999999999999999999999999)
                    buff += resp.decode()
                buff1 = buff.split('\n')

                virtualIMT=[]
                for descs in buff1:
                    if "down" in descs or "uppress" in descs:
                        continue
                    elif "up" in descs:
                        parts = descs.split()

                        IMTno = str(parts[3].split("|")[0])
                        k = " ".join(parts[3:])
                        virtual= parts[0].split("E")[0]
                        if virtual == "V":
                            virtualIMT.append(IMTno)

                        if virtual == "V" and virtualIMT.count(IMTno)==2:


                            if not ( las == 'L' or las == '0'):
                                if (descs.count("|") == 3):

                                    row = sheet1.row(i)
                                    row.write(0, parts[0])
                                    row.write(1, k)
                                    if (("-") in k):
                                        row.write(2, k.split("-")[1].split("|")[0])
                                    else:
                                        row.write(2, k.split("|")[1])
                                    i = i + 1

                        if not IMTno in IMT:
                            IMT.append(IMTno)
                            if not virtual=="V":
                                last=len(parts)
                                lastelement=str(parts[last-1])
                                las=lastelement[len(lastelement)-1]
                                if not (las == 'L' or las == '0'):
                                    if(descs.count("|")>=3):

                                        row= sheet1.row(i)
                                        row.write(0,parts[0])
                                        row.write(1,k)
                                        if (("-") in k):
                                            row.write(2,k.split("-")[1].split("|")[0])
                                        else:
                                            row.write(2,k.split("|")[1])
                                        i=i+1

                resp = ""
                buff = ""
                chan.send("quit" + line_end)
                time.sleep(4)
                resp = chan.recv(99999999)
                chan.send("\n")
                time.sleep(1)

        LOGfile.save( change + ".xls")

        client.close()



################# MAIN #################



ssh = SSH()
try:
    ssh.execute_command(router, LDAP, password, 'dis int des | i  up      up       10')
except Exception as e:
    print(str(e))

print("END")






