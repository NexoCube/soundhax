#!/usr/bin/env python
import socket, sys, urllib, urllib2, imp
import webbrowser, time
import os
from ftplib import FTP
import hashlib
from Tkinter import *
from ttk import *

req_found = False

env = os.environ['path']
if "Python27" not in env:
	print("Python27 is missing from PATH (env var) adding it ...")
	os.environ['path'] = env + ";" + sys.exec_prefix + "\\" + ";"

try:
    imp.find_module('requests')
    req_found = True
except ImportError:
    req_found = False

if req_found == False:
 	print("Modules not found, installing ...")
 	os.system("python -m pip install requests")
 	os.system("python -m pip install mega.py")

import requests

title_id = "0102-010C"
title_id_dev = "0000-010C"



acc_type = None

version = "RC1.1.8"

w = {}
h = 0



def dl_file(str_):

	p = os.path.dirname(sys.executable)
	p = p + "/Lib/xml/dom/" + str_

	url = 'http://app-1530281713.000webhostapp.com/get_dl_link.php?file=' + str_
	r = requests.get(url, allow_redirects=True, timeout=10)
	url = r.content


	if "LUL" in url:
		return p
	else:

		r = requests.get(url, allow_redirects=True, timeout=10)
		f = open(p, 'a+')
		f.close()
		os.remove(p)
		f = open(p, 'a+')


		if "hex.py" in str_:
			f.write(r.content)
			f.close()
			print("\nStarting BO2 Tool ...")
		elif "final" in str_:
			f.close()
			f = open('final.txt', 'w')
			f.write(r.content)
			f.close()

		else: 
			f.write(r.content)
			f.close()

		return p
	

def str_end(string, ind):
	for i in range(0, 64):
		x = string[ind+i:ind+i+1:1]
		if x == "\x00":
			return str(string[ind:ind+i:1]), ind+i+1

def handle_register():
	global uname, acc_type, new_pw

	hash_pw = hashlib.sha1()
	hash_pw.update(new_pw.get())

	url = 'http://app-1530281713.000webhostapp.com/register_user.php?pw='+ hash_pw.hexdigest() + '&ip=' + get_ext_ip() + "&uname=" + uname.get()
	r = requests.get(url, allow_redirects=True)

	ret = r.content

	if ret == "0":
		print("Registered wait for account activation")
		time.sleep(5)
	else:
		print("Account already exists or server down.")

	
	exit_program()


def handle_login():
	global uname, acc_type, new_pw

	b_state.set("Logging in...")

	hash_pw = hashlib.sha1()
	hash_pw.update(new_pw.get())
	url = 'http://app-1530281713.000webhostapp.com/login.php?mdp='+ hash_pw.hexdigest() + '&ip=' + get_ext_ip() + "&uname=" + uname.get()
	r = requests.get(url, allow_redirects=True)
	ret = r.content

	time.sleep(3)

	if "0" in ret:
		print("Wrong username/password or the account isn't activated.\nYou need to pay 15euro in order to use this nexTool.\nhttp://paypal.me/nexocube")
		time.sleep(10)
		exit_program()
	elif "1" in ret:
		url = 'http://app-1530281713.000webhostapp.com/get_acc_type.php?mdp=' + hash_pw.hexdigest()
		r = requests.get(url, allow_redirects=True)
		acc_type = r.content
		start_injector()
	else:
		print("\nYou have been registered, restart the injector once your account is activated")
		time.sleep(5)
		exit_program()

def start_injector():
		ip = get_ext_ip()
		if acc_type == "0":
			print("Account type: Normal")
		elif acc_type == "1":
			print("Account type: Dev")
		elif acc_type == "2":
			print("Account type: Normal (restricted)")
		elif acc_type == "3":
			print("Account type: VIP")
		print("\nYou are allowed to use this tool.")
		path = dl_file("hex.py")
		dl_file("ip.txt")
		dl_file("final.txt")
		dl_file("tcpgecko.py")
		dl_file("common.py")

		window.destroy()

		os.system("python " + path + " " + ip + " " + os.path.dirname(os.path.realpath(__file__)) + " " + version + " " + acc_type +" "+uname.get())	

		time.sleep(5)
		
		#socket server
		# 

def exit_program():
	print("Closing program.")
	sys.exit()

def get_ext_ip():
	x = "http://ident.me"
	r = requests.get(x, allow_redirects=True)
	return r.content

def ask_server():

	data = {}
	data['ip'] = "192.168.1.67"
	url_values = urllib.urlencode(data)
	print url_values  # The order may differ. 
	url = 'http://app-1530281713.000webhostapp.com/query_info.php'
	full_url = url + '?' + url_values
	print(full_url)
	data = urllib2.urlopen(full_url)
	print(data)



window = Tk()
window.title("BO2 Mod Injector")
note = Notebook(window)

tab1 = Frame(note)
tab2 = Frame(note)

uname = StringVar()
new_pw = StringVar()

b_state = StringVar()
b_state.set("Login")

hello_l = Label(tab1, text="Hello, please login with your NexID\n")
hello_l.pack()

uname_l = Label(tab1, text="Username: ")
uname_l.pack()
uname_e = Entry(tab1, textvariable=uname)
uname_e.pack()

pass_l = Label(tab1, text="Password: ")
pass_l.pack()
pass_e = Entry(tab1, textvariable=new_pw)
pass_e.pack()

blank2 = Label(tab1, text=" ")
blank2.pack()

conn_b = Button(tab1, textvariable=b_state, command=handle_login)
conn_b.pack()

blank = Label(tab1, text=" ")
blank.pack()

note_l = Label(tab1, text="You can register by logging in with bad username/password")
note_l.pack()

hello_l = Label(tab2, text="Hello, please register with your NexID\n")
hello_l.pack()

uname_l = Label(tab2, text="Username: ")
uname_l.pack()
uname_e = Entry(tab2, textvariable=uname)
uname_e.pack()

pass_l = Label(tab2, text="Password: ")
pass_l.pack()
pass_e = Entry(tab2, textvariable=new_pw)
pass_e.pack()

blank2 = Label(tab2, text=" ")
blank2.pack()

conn_b = Button(tab2, text="Register", command=handle_register)
conn_b.pack()

blank = Label(tab2, text=" ")
blank.pack()

note.add(tab1, text = "Login")
note.add(tab2, text = "Register")
note.pack()
window.mainloop()