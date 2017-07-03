### Import Libraries ###
import cgi

def clean(uname):
	# Clean Input String 
	uname=uname.replace(" ", "")
	uname.decode('string-escape')
	uname=cgi.escape(uname)
	return uname