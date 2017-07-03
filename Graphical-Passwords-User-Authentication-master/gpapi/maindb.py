### Import Libraries ####
import sqlite3
import random

class Gpapidb:

	def __init__(self,M,N,ra,debug):
		self.M=M;self.N=N;self.debug=debug
		# Create Database
		self.db=sqlite3.connect('gpapi.db')
		# Check for Table Existance
		c=self.db.cursor()
		c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND (name='imgbank')");
		data1=c.fetchall()
		c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND (name='userbank')");
		data2=c.fetchall()
		if (not data1 or int(data1[0][0])==0):
			self.db.execute("CREATE TABLE imgbank (num INTEGER PRIMARY KEY, hseed VARCHAR(255) NOT NULL)")
			if self.debug: print "\n---------- Generating a Set of %d Randomart Images ----------" % (M)
			for i in range(1,M+1):
				hseed=str(ra.generate())
				self.db.execute("INSERT INTO imgbank (num, hseed) VALUES ('%d', '%s')" % (i, hseed))
				if self.debug: print "----- Image Index #%d# Complete -----" % (i)
			self.db.commit()
			if self.debug: print "\n---------- Completed Randomart Image Generation ----------"
		if (not data2 or int(data2[0][0])==0):
			tmp="CREATE TABLE userbank (uname VARCHAR(255) PRIMARY KEY, " + \
				"uemail VARCHAR(255), "	+ \
				', '.join(["hseed%d VARCHAR(255) NOT NULL" % (i) for i in range(1,self.N+1)]) + \
				")"
			self.db.execute(tmp)
			self.db.commit()

	def add(self, uname, uemail, psw):
		# Add (Username, Email, Password) Record
		self.db.execute("INSERT INTO userbank VALUES ('%s', '%s', '%s')" % (uname, uemail, "', '".join(psw)))
		self.db.commit()

	def select_user(self, uname):
		# Check (Username, Password) Record
		self.db=sqlite3.connect("gpapi.db")
		c=self.db.cursor()
		c.execute("SELECT uname FROM userbank WHERE uname =?",(uname,))
		data = c.fetchall()
		if data: return 1
		else: return 0

	def select_user_psw(self, uname):
		# Check (Username, Password) Record
		self.db=sqlite3.connect("gpapi.db")
		c=self.db.cursor()
		c.execute("SELECT * FROM userbank WHERE uname =?",(uname,))
		data = c.fetchall()[0]
		if data:
			return [int(data[i]) for i in range(2,self.N+2)]
		else:
			return False

	def check_user_psw(self, uname, new_psw):
		psw=self.select_user_psw(uname)
		tmp=iter(psw)
		return all(a in tmp for a in new_psw)		

	def select_img(self,num):
		# Check (Index, Hseed) Record
		self.db=sqlite3.connect("gpapi.db")
		c=self.db.cursor()
		c.execute("SELECT hseed FROM imgbank WHERE num =?",(num,))
		data = c.fetchall()
		if data: return int(data[0][0])
		else: return False 

	def draw_challenge(self,uname,m,n):
		# Select Decoy and Challenge Sets
		self.db=sqlite3.connect("gpapi.db")
		c=self.db.cursor()
		## Draw User Password Subset 
		psw=random.sample(self.select_user_psw(uname),n);
		## Draw Challenge Subset
		decoy=[] 
		for index in range(m-n-len(set(psw))+2):
			## Check If Challenge Subset in User Password Subset ##
			while True:
				num=random.randint(1,self.M)
				c.execute("SELECT hseed FROM imgbank WHERE num =?",(num,))
				data=c.fetchall()[0]
				if data:
					if (int(data[0]) not in self.select_user_psw(uname) and
						int(data[0]) not in decoy): break
			decoy.append(int(data[0]))

		ch=psw+decoy;random.shuffle(ch)
		return ch

