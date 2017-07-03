### Import Libraries ###
import os
import hashlib
import sys
import numpy as np
import random
import math
from PIL import Image

### Close to: http://math.andrej.com/wp-content/uploads/2010/04/randomart.py

##### Image Processing #####
### Ideal Low Pass Filter ###
def ideal2d_lp(shape, f, pxd=1):
    pxd = float(pxd)
    rows, cols = shape
    x = np.linspace(-0.5, 0.5, cols)  * cols / pxd
    y = np.linspace(-0.5, 0.5, rows)  * rows / pxd
    radius = np.sqrt((x**2)[np.newaxis] + (y**2)[:, np.newaxis])
    filt = np.ones(shape)
    filt[radius<f] = 0
    return filt
### Computing Noise Coefficient ###
def regular_img(img,thr):
	# Convert RBG image in GreyScale Image
	rgb_lin=np.asarray(img)*(1/float(499))
	greyscale=rgb2gray(rgb_lin)
	# Compute FFT
	f=np.fft.fftshift(np.fft.rfft2(greyscale,norm="ortho"))
	# Apply HP Filter
	filt=ideal2d_lp(f.shape, thr)
	new_f=f*filt
	res=(np.sum(np.absolute(new_f))/87448)*100
	return res
### Colour Scales ###
def randart2rgb(tup):
	return tuple(int((tup[i]+1)*250) for i in range(len(tup)))
def rgb2gray(tmp):
	return np.inner(tmp,np.array([0.299,0.587,0.114]))

##### Other Functions #####
def well3(x): return 1 - 2 / (1 + x*x) ** 8
def tent3(x): return 1 - 2 * math.fabs(x)
##### Evaluation Functions #####
def power_x2(tup):
	tmp=range(3);random.shuffle(tmp)
	return tuple(tup[tmp[i]] for i in range(len(tup)))
def add2(tup1,tup2):
	return tuple((tup1[i]+tup2[i])/2 for i in range(len(tup1)))
def prod2(tup1,tup2):
	return tuple(tup1[i]*tup2[i] for i in range(len(tup1)))
def max2(tup):
	return tuple(max(tup) for i in range(len(tup)))
def min2(tup):
	return tuple(min(tup) for i in range(len(tup)))
def perm2(tup):
	tmp=range(3); random.shuffle(tmp)
	return tuple(tup[tmp[i]] for i in range(len(tup)))
def neg2(tup):
	return tuple(-tup[i] for i in range(len(tup)))
def level2(thr,tup1,tup2,tup3):
	tup = [0]*3
	tup[0] = tup2[0] if tup1[0]>thr else tup3[0]
	tup[1] = tup2[1] if tup1[1]>thr else tup3[1]
	tup[2] = tup2[2] if tup1[2]>thr else tup3[2]
	return tuple(tup)
def sel2(thr,tup1,tup2,tup3):
	if (tup1[0]/3+tup1[1]/3+tup1[2]/3)>thr: return tup2
	else: return tup3
def mod2(tup1,tup2):
	try:
		return tuple(tup1[i]%tup2[i] for i in range(len(tup1)))
	except:
		return (0,0,0)
def mix2(tup1,tup2,tup3,tup4):
	try:
		w = tuple(math.fabs(tup3[i])/(math.fabs(tup3[i])+math.fabs(tup4[i])) for i in range(len(tup1)))
		return tuple(tup1[i]*w[i]+tup2[i]*(1-w[i]) for i in range(len(tup1)))
	except:
		return (0,0,0)
def torus2(tup):
	theta=tup[0]; phi=tup[1]
	r=1-tup[2]/2; R=1-r
	return ((R+r*math.cos(2*math.pi*theta)*math.cos(2*math.pi*phi)),
			(R+r*math.sin(2*math.pi*theta)*math.sin(2*math.pi*phi)),
			 r*math.sin(2*math.pi*theta))
def circle2(tup):
	r=tup[0]/2;theta=tup[1];phi=tup[2]
	x0=tup[0]/2;y0=tup[1]/2;z0=tup[2]/2
	return (x0+r*math.cos(2*math.pi*theta)*math.sin(math.pi*phi),
		    y0+r*math.sin(2*math.pi*theta)*math.sin(math.pi*phi),
		    z0+r*math.cos(math.pi*phi))
def gaussian2(tup):
	return tuple(math.exp(-(tup[i]**2)/0.5) for i in range(len(tup)))
def well2(tup):
	return tuple(well3(tup[i]) for i in range(len(tup)))
def tent2(tup):
	return tuple(tent3(tup[i]) for i in range(len(tup)))
def cos2(tup):
	return tuple(math.cos(2*math.pi*tup[i]) for i in range(len(tup)))
def sin2(tup):
	return tuple(math.sin(2*math.pi*tup[i]) for i in range(len(tup)))

##### Operation Classes #####
### Mix2 xy ###
class Mix1xy:
	arity=0
	def __init__(self):
		self.c1=random.random()*2-1
		self.c2=random.random()*2-1
		return
	def __str__(self):
		return "Mix1(x,y)"
	def eval(self,x,y):
		return (self.c1,-(x+y)/2,self.c2)
class Mix2xy:
	arity=0
	def __init__(self):
		return
	def __str__(self):
		return "Mix2(x,y)"
	def eval(self,x,y):
		return (x,-x/2,y/2)
class Mix3xy:
	arity=0
	def __init__(self):
		return
	def __str__(self):
		return "Mix3(x,y)"
	def eval(self,x,y):
		return (x,y,x)
class Mix4xy:
	arity=0
	def __init__(self):
		return
	def __str__(self):
		return "Mix4(x,y)"
	def eval(self,x,y):
		return (x**2,-math.fabs(x)**math.fabs(y),(x+y)/2)
class Mix5xy:
	arity=0
	def __init__(self):
		self.c1=random.random()*2-1
	def __str__(self):
		return "Mix5(x,y)"
	def eval(self,x,y):
		return (-x*y,(x+y)/2,math.fabs(x))
class Mix6xy:
	arity=0
	def __init__(self):
		self.c1=random.random()*2-1
		self.c2=random.random()*2-1
		self.c3=random.random()*2-1
		return
	def __str__(self):
		return "Mix6(x,y)"
	def eval(self,x,y):
		return (self.c1*x,(self.c2+x)/2,self.c3)
### Rgb ###
class rgb:
	arity=3
	def __init__(self, e1, e2, e3):
		self.e1=e1
		self.e2=e2
		self.e3=e3
	def __str__(self):
		return "rgb(%s,%s,%s)" % (str(self.e1), str(self.e2), str(self.e3))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		e3=(self.e3).eval(x,y)
		return (e1[0],e2[1],e3[2])
### Add ###
class add:
	arity=2
	def __init__(self, e1, e2):
		self.e1=e1
		self.e2=e2
	def __str__(self):
		return "add(%s,%s)" % (str(self.e1), str(self.e2))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		res=add2(e1,e2)
		return res
### Prod ###
class prod:
	arity=2
	def __init__(self, e1, e2): 
		self.e1=e1
		self.e2=e2
	def __str__(self):
		return "prod(%s,%s)" % (str(self.e1), str(self.e2))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		res=prod2(e1,e2)
		return res
### Sin ###
class sin:
	arity=1
	def __init__(self, e1): 
		self.e1=e1
	def __str__(self):
		return "sin(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return sin2(e1)
### Cos ###
class cos:
	arity=1
	def __init__(self, e1): 
		self.e1=e1
	def __str__(self):
		return "sin(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return cos2(e1)
### Max ###
class fmax:
	arity=1
	def __init__(self, e1): 
		self.e1=e1
	def __str__(self):
		return "max(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return max2(e1)
### Min ###
class fmin:
	arity=1
	def __init__(self, e1): 
		self.e1=e1
	def __str__(self):
		return "min(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return min2(e1)
### Permutate ###
class permute:
	arity=1
	def __init__(self, e1): 
		self.e1=e1
	def __str__(self):
		return "perm(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return perm2(e1)
### Negative ###
class neg:
	arity=1
	def __init__(self, e1): 
		self.e1=e1
	def __str__(self):
		return "neg(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return neg2(e1)
### Torus ###
class torus:
	arity=1
	def __init__(self,e1): 
		self.e1=e1
	def __str__(self):
		return "torus(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return torus2(e1)
### Circle ###
class circle:
	arity=1
	def __init__(self,e1): 
		self.e1=e1
	def __str__(self):
		return "circle(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return circle2(e1)
### Gaussian ###
class gaussian:
	arity=1
	def __init__(self,e1): 
		self.e1=e1
	def __str__(self):
		return "gaussian(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return gaussian2(e1)
### Well ###
class well:
	arity=1
	def __init__(self,e1): 
		self.e1=e1
	def __str__(self):
		return "well(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return well2(e1)
### Tent ###
class tent:
	arity=1
	def __init__(self,e1): 
		self.e1=e1
	def __str__(self):
		return "tent(%s)" % (str(self.e1))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		return tent2(e1)
### Level ###
class level:
	arity=3
	def __init__(self,level,e1,e2): 
		self.thr=random.random()*0.5-0.25
		self.level=level
		self.e1=e1
		self.e2=e2
	def __str__(self):
		return "level(%s,%s,%s)" % (str(self.level),str(self.e1),str(self.e2))
	def eval(self,x,y):
		level=(self.level).eval(x,y)
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		return level2(self.thr,level,e1,e2)
### Select ###
class sel:
	arity=3
	def __init__(self,e1,e2,e3): 
		self.thr=random.random()*2-1
		self.e1=e1
		self.e2=e2
		self.e3=e3
	def __str__(self):
		return "sel(%s,%s,%s)" % (str(self.e1),str(self.e2),str(self.e3))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		e3=(self.e3).eval(x,y)
		return sel2(self.thr,e1,e2,e3)
### Mod ###
class mod:
	arity=2
	def __init__(self,e1,e2):
		self.e1=e1
		self.e2=e2
	def __str__(self):
		return "mod(%s,%s)" % (str(self.e1),str(self.e2))
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		return mod2(e1,e2)
### Mix ###
class mix:
	arity=4
	def __init__(self,e1,e2,e3,e4):
		self.e1=e1
		self.e2=e2
		self.e3=e3
		self.e4=e4
	def __str__(self):
		return "mix(%s,%s,%s,%s)" % (self.e1,self.e2,self.e3,self.e4)
	def eval(self,x,y):
		e1=(self.e1).eval(x,y)
		e2=(self.e2).eval(x,y)
		e3=(self.e3).eval(x,y)
		e4=(self.e4).eval(x,y)
		return mix2(e1,e2,e3,e4)

### Operations ###
atomexp = [Mix1xy,Mix2xy,Mix3xy,Mix4xy,Mix5xy,Mix6xy,add,prod,cos,sin,rgb,torus,circle,gaussian,tent,well,mix,level,sel,mod]

##### Random Art Expression Generation Class #####
class Randomart:
	def __init__(self,atomexp):
		self.G0=tuple(tmp for tmp in atomexp if tmp.arity==0)
		self.G1=tuple(tmp for tmp in atomexp if tmp.arity>0)

	def __str__(self):
		return str(self.E)

	def expression(self,d):
		def expression2(d):
			if d<=0:
				op=random.choice(self.G0)
				return op()
			else:
				op=random.choice(self.G1); args=[]
				a=[random.randint(0,d-1) for _ in range(op.arity)]
				for i in sorted(a):
					tmp=expression2(i)
					args.append(tmp)
				return op(*args)
		self.E=expression2(d)

	def evaluate(self,x,y):
		return (self.E).eval(x,y)

##### Drawing Random Art Image Class #####
class Randimage:

	def __init__(self):
		self.F=Randomart(atomexp)

	def draw(self):

		## Create new image ##
		img=Image.new('RGB',(500,499),"black")
		pix=img.load()
		## Generate Random Art Image ##
		for x in range(img.size[0]):   
		    for y in range(img.size[1]):
		    	x_sc=x/float(img.size[0])-1
		    	y_sc=y/float(img.size[1])-1
		    	rgb_sc=(self.F).evaluate(x_sc,y_sc)
		    	rgb=randart2rgb(rgb_sc)
		        pix[x,y]=rgb
		return img

	def generate(self):

		tmp="";	md5 = hashlib.md5()
		random.seed()
		seed = random.randint(0, sys.maxint)
		md5.update(str(seed)); hseed=int(md5.hexdigest(),16)
		random.seed(hseed)

		while True:
			self.F.expression(10)
			img=self.draw()
			## Minimum Complexity Property ##
			res=regular_img(img,110)
			if 0.15<res<0.7: break

		return hseed

	def regenerate(self, hseed):

		random.seed(hseed)
		self.F.expression(10)
		img=self.draw()
		random.seed(); id=random.randint(0,100000)
		fname="img%d.png" % (id)
		faddress="%s/static/figs/psw/%s" % (os.getcwd(),fname)
		img.save(faddress)
		return fname
			