### Import Libraries ###
from bottle import Bottle, run, template, request, response, redirect, static_file, HTTPError
from appendix import *
from maindb import Gpapidb
from randomart import Randimage
import random 
import sqlite3
import os

class CacheUsers:
	def __init__(self):
		self.data={}
	def __str__(self):
		return str(self.data)
	def add(self,uname):
		self.data[uname]={}
		self.data[uname]["challenge"]=[]
		self.data[uname]["flogin"]=3
		self.data[uname]["authen"]=0
	def authenticate(self,uname):
		self.data[uname]["authen"]=3
		self.data[uname]["challenge"]=[]
	def check_authen(self,uname):
		if self.data[uname]["authen"]<=0:
			return False
		else:
			return True
	def check_flogin(self,uname):
		if self.data[uname]["flogin"]<=0:
			return False
		else:
			return True
	def create_challenge(self,uname,psw):
		self.data[uname]["challenge"]=psw
	def get_challenge(self,uname):
		return self.data[uname]["challenge"]
	def get_flogin(self,uname):
		return self.data[uname]["flogin"]
	def search(self,uname):
		return uname in self.data
	def remove(self,uname):
		del self.data[uname]
	def update_authen(self,uname):
		self.data[uname]["authen"]-=1
	def update_flogin(self,uname):
		self.data[uname]["flogin"]-=1


##### Initialization ####
debug=True
##### Initialization ####
# Global Variables #
M=40;m=20;N=8;n=4;num_rows=8;num_cols=5;
fnamelist=[]
# Image Location
imgpsw="psw/img_"
img1="content/img1.png";img2="content/img2.png"
img3="content/img3.png";img4="content/img4.png"
img5="content/img5.png";img6="content/img6.png"
img7="content/img7.png"
if debug: print "\n---------- API: Graphical Passwords for User Authentification ----------\n"
# Application Classes #
app=Bottle()
ra=Randimage()
users=CacheUsers()
db=Gpapidb(M,N,ra,debug=debug)

@app.route('/gpapi/login', method="get")
def login_form():
	params={'unameErr':"",'img1':img1,'img2':img2}
	return template('login_wp.tpl',params)

@app.route('/gpapi/login', method="post")
def submit_login_form():
	params={'unameErr':"",'img1':img1,'img2':img2}
	uname=clean(request.forms.get('uname'))
	if debug: print "Users: ", users
	if len(uname)==0:
		params['unameErr']="Username is required"
		return template('login_wp.tpl',params)
	elif not db.select_user(uname):
		params['unameErr']="Username is not valid"
		return template('login_wp.tpl',params)
	else:
		if users.search(uname): 
			if users.check_authen(uname):
				url="/gpapi/success?uname='%s'"%(uname)
				redirect(url)
			else:
				url="/gpapi/challenge?uname='%s'"%(uname)
				redirect(url)	
		else:
			users.add(uname)
			url="/gpapi/challenge?uname='%s'"%(uname)
			redirect(url)			

@app.route('/gpapi/register', method="get")
def register_form():
	global fnamelist
	params={'unameErr':"",'uemailErr':"",'M':M,'N':N,
			'num_rows':num_rows,'num_cols':num_cols,
			'img2':img2,'img3':img3,'img4':img4,
			'img5':img5,'imgpsw':imgpsw}
	if debug: print "\n"
	for index in range(1,M+1):
		fname=ra.regenerate(db.select_img(index))
		if debug: print "----- Image Index #%d# Complete -----" % (index)
		fnamelist.append(fname)
	# if debug: print "----- Image File List: ", fnamelist, "-----"
	return template('register_user_wp.tpl', params)

@app.route('/gpapi/register', method="post")
def submit_register_form():
	global fnamelist
	params={'unameErr':"",'uemailErr':"",'M':M,'N':N,
			'num_rows':num_rows,'num_cols':num_cols,
			'img2':img2,'img3':img3,'img4':img4,
			'img5':img5,'imgpsw':imgpsw}
	uname=clean(request.forms.get('uname'))
	uemail=clean(request.forms.get('uemail'))
	psw=[int(request.forms.get('Select_'+str(i))) for i in range(1,N+1)]
	valid=True
	if debug: print "Users: ", users
	if len(uname)==0: 
		params['unameErr']="Username is required"
		valid=False
	elif db.select_user(uname):
		params['unameErr']="Username is already taken"
		valid=False
	if len(uemail)==0:
		params['uemailErr']="User email is required"
		valid=False
	if any([tmp==0 for tmp in psw]):
		valid=False 
	if valid:
		psw=[str(db.select_img(num)) for num in psw]
		if any([not tmp for tmp in psw]):
			pass # Exit due to not upload
		else:
			db.add(uname,uemail,psw)
			while fnamelist:
				fname=fnamelist.pop()
				try: os.remove(os.getcwd()+'/static/figs/psw/'+fname)
				except OSError: pass
			redirect('/gpapi/login')
		return
	else:
		return template('register_user_wp.tpl',params)

@app.route('/gpapi/challenge', method="get")
def challenge_form():
	global fnamelist
	uname=request.query.uname.replace("'","")
	if debug: print "Users: ", users
	if users.search(uname) is not False:
	 	params={'uname':uname,'unameErr':"",'uemailErr':"",
				'M':M,'N':N,'m':m,'n':n,'num_rows':num_rows/2,
				'num_cols':num_cols,'img2':img2,'img3':img3,
				'img4':img4,'img5':img5,'imgpsw':imgpsw,
				'attemps':users.get_flogin(uname)}
		users.create_challenge(uname,db.draw_challenge(uname,m,n))
		if debug: print "\n"
		for hseed in users.get_challenge(uname):
			fname=ra.regenerate(hseed)
			if debug: print "----- Image Index #%d# Complete -----" % (hseed)
			fnamelist.append(fname)
			# if debug: print "----- Image File List: ", fnamelist, "-----"
		return template('challenge_wp.tpl',params)
	else:
		return HTTPError(404, "Invalid Username")

@app.route('/gpapi/challenge/<uname>', method="post")
def submit_challenge_form(uname):
	params={'uname':uname,'unameErr':"",'uemailErr':"",
			'M':M,'N':N,'m':m,'n':n,'num_rows':num_rows/2,
			'num_cols':num_cols,'img2':img2,'img3':img3,
			'img4':img4,'img5':img5,'imgpsw':imgpsw}
	new_psw=[int(request.forms.get('Select_'+str(i)))-1 for i in range(1,n+1)]
	new_psw=[users.get_challenge(uname)[num] for num in new_psw]
	if debug: print "Users: ", users
	if any([not tmp for tmp in new_psw]):
		pass # Exit due to not upload
	else:
		if db.check_user_psw(uname, new_psw):
			users.authenticate(uname)
			response.set_header('Location','/gpapi/challenge/success');
		else:
			users.update_flogin(uname)
			if users.check_flogin(uname):
				params["attemps"]=users.get_flogin(uname)
				return template('challenge_wp.tpl',params)
			else:
				users.remove(uname)
				response.set_header('Location','/gpapi/challenge/failure')
		response.status=303
		while fnamelist:
			fname=fnamelist.pop()
			# print os.getcwd()+'/static/figs/psw/'+fname
			try: os.remove(os.getcwd()+'/static/figs/psw/'+fname)
			except OSError: pass
		return

@app.route('/gpapi/success', method="get")
def success():	
	params={'img2':img2,'img6':img6}
	uname=request.query.uname.replace("'","")
	users.update_authen(uname)
	if not users.check_authen(uname):
		users.remove(uname)
	return template('success_wp.tpl',params)

@app.route('/gpapi/challenge/success', method="get")
def challenge_success():
	params={'img2':img2,'img6':img6}
	return template('challenge_success_wp.tpl',params)

@app.route('/gpapi/challenge/failure', method="get")
def chanllenge_failure():
	params={'img2':img2,'img7':img7}
	return template('challenge_failure_wp.tpl',params)

### Manage Figures ###
@app.route('/gpapi/figs/<dir>/<img>')
def upload_img(dir,img):
	global fnamelist
	if dir == "psw":
		index=int(''.join([char for char in img if char.isdigit()]))-1
		img=fnamelist[index]
	root=os.getcwd()+'/static/figs/'+dir
	return static_file(img, root=root)

run(app, host='localhost',port=8080,debug=False)
