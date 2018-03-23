from tkinter import *
import time
import numpy as np
import cv2
import global_vars as gv
import DensityChecker as dc
from threading import Thread
gv.init()

tfnet = dc.loadmodel()

def getden(frame, tfnet):
	gv.ans = dc.getDensity(frame, tfnet)

timer = 0

def getTimefromDensity(density):

	if (density > 0.9):
		an = 30
	elif(density > 0.6 and density < 0.9):
		an=25
	elif(density > 0.4 and density < 0.6):
		an=20
	elif(density > 0.1 and density < 0.4):
		an=15
	else:
		an=10
	return	an


#inital value
ttime = 0
rtime = 0
btime = 0
ltime = 0
ts = 0
rs = 0
bs = 0
ls = 0

#open one

#get top density
#density 80
openis = 'top'
nextis = 'right'
ttime = 10
rtime = 10
btime = 0
ltime = 0
ts = 1
rs = 0
bs = 0
ls = 0

back1 = cv2.imread('back.jpg')


while(1):
	img_temp = cv2.imread('sample.jpg')
	cv2.imshow('Imgabe',img_temp)

	img = cv2.resize(back1,(500,500),interpolation=cv2.INTER_CUBIC)


	time.sleep(1)
	timer = timer +1


	#top
	img = cv2.circle(img,(250,10), 10, (0,100,0), -1)
	img = cv2.circle(img,(250,30), 10, (0,0,255), -1)
	#right
	img = cv2.circle(img,(10,250), 10, (0,100,0), -1)
	img = cv2.circle(img,(30,250), 10, (0,0,255), -1)
	#bottom
	img = cv2.circle(img,(250,470), 10, (0,100,0), -1)
	img = cv2.circle(img,(250,490), 10, (0,0,255), -1)
	#left
	img = cv2.circle(img,(490,250), 10, (0,100,0), -1)
	img = cv2.circle(img,(470,250), 10, (0,0,255), -1)


	font = cv2.FONT_HERSHEY_SIMPLEX
	
	
	if(openis=="top" and nextis=="right"):
		ttime = ttime-1
		rtime = rtime-1

		cv2.putText(img,str(ttime),(240,60), font, 0.5,(0,255,0),1,cv2.LINE_AA)
		cv2.putText(img,str(rtime),(450,250), font, 0.5,(0,0,255),1,cv2.LINE_AA)
		
		img = cv2.circle(img,(250,10), 10, (0,255,0), -1)
		img = cv2.circle(img,(250,30), 10, (0,0,100), -1)
		if(ttime==5):
			Thread(target = getden(img_temp, tfnet)).start()
			
		if(ttime==0):
			timer=0


			if(gv.ans>0):
				print (gv.ans)
				updatetime =getTimefromDensity(gv.ans)
				rtime = updatetime
				btime = updatetime
				gv.ans=-1
			openis = 'right'
			nextis = 'bottom'
			
			ts = 0
			rs = 1
			bs = 0
			ls = 0
	elif(openis=='right' and nextis=='bottom'):
		rtime = rtime-1
		btime = btime-1
		cv2.putText(img,str(rtime),(450,250), font, 0.5,(0,255,0),1,cv2.LINE_AA)
		cv2.putText(img,str(btime),(240,450), font, 0.5,(0,0,255),1,cv2.LINE_AA)
		img = cv2.circle(img,(490,250), 10, (0,255,0), -1)
		img = cv2.circle(img,(470,250), 10, (0,0,100), -1)
		if(rtime==5):
			Thread(target=getden(img_temp, tfnet)).start()
			
		if(rtime==0):#updatetime
			timer=0
			if(gv.ans>0):
				updatetime = getTimefromDensity(gv.ans)
				btime = updatetime
				ltime = updatetime
				gv.ans = -1
			openis = 'bottom'
			nextis = 'left'
			
			ts = 0
			rs = 0
			bs = 1
			ls = 0
	elif(openis=='bottom' and nextis=='left'):
		btime = btime-1
		ltime = ltime-1
		cv2.putText(img,str(btime),(240,450), font, 0.5,(0,255,0),1,cv2.LINE_AA)
		cv2.putText(img,str(ltime),(50,250), font, 0.5,(0,0,255),1,cv2.LINE_AA)
		img = cv2.circle(img,(250,470), 10, (0,255,0), -1)
		img = cv2.circle(img,(250,490), 10, (0,0,100), -1)
		if(btime==5):
			Thread(target=getden(img_temp, tfnet)).start()
			
		if(btime==0):
			#updatetime
			timer=0
			if(gv.ans>0):
				updatetime = getTimefromDensity(gv.ans)
				ltime = updatetime
				ttime = updatetime
				gv.ans = -1
			openis = 'left'
			nextis = 'top'
			
	
			ts = 0
			rs = 0
			bs = 0
			ls = 1
	elif(openis=='left' and nextis=='top'):
		ltime = ltime-1
		ttime = ttime-1
		cv2.putText(img,str(ltime),(50,250), font, 0.5,(0,255,0),1,cv2.LINE_AA)
		cv2.putText(img,str(ttime),(240,60), font, 0.5,(0,0,255),1,cv2.LINE_AA)
		img = cv2.circle(img,(10,250), 10, (0,255,0), -1)
		img = cv2.circle(img,(30,250), 10, (0,0,100), -1)
		if(ltime==5):
			#density of top
			Thread(target=getden(img_temp, tfnet)).start()
		if(ltime==0):
			#updatetime
			timer=0
			if(gv.ans>0):

				updatetime = getTimefromDensity(gv.ans)
				ttime = updatetime
				rtime = updatetime
				gv.ans = -1
			openis = 'top'
			nextis = 'right'
			

			ts = 1
			rs = 0
			bs = 0
			ls = 0

	print('time'+str(timer))
	print('toptime: '+str(ttime)+' righttime: '+str(rtime)+'bottomtime: '+str(btime)+'lefttime: '+str(ltime))
	print('tops: '+str(ts)+' rights: '+str(rs)+'bottoms: '+str(bs)+'lefts: '+str(ls))
	cv2.imshow('window',img)
	cv2.waitKey(1)

cv2.destroyAllWindows()

		

