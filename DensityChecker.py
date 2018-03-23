from darkflow.net.build import TFNet
import numpy as np
import cv2
import json
from threading import Thread



def loadmodel():
	options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.2}
	tfnet = TFNet(options)

	return tfnet


def getdensity(image,tfnet):
    imgcv =np.array(image)
    height, width = imgcv.shape[:2]
    #print(height , ":", width)
    
    result = tfnet.return_predict(imgcv)
    
    motorbike=0;
    bicycle=0;
    car=0;
    bus=0;
    truck=0;

    a = np.zeros((height,width))

    for value in result:
        if(value["label"]=='car'):
            car = car+1
            ones = np.ones((value['bottomright']['y']-value['topleft']['y'],value['bottomright']['x']-value['topleft']['x']))

            bounding_box = [value['topleft']['x']-5,value['topleft']['y']-5,value['bottomright']['x']-value['topleft']['x']-5,value['bottomright']['y']-value['topleft']['y']-5]

            a[bounding_box[1]:bounding_box[1] + bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]] = 1
        if(value["label"]=='bus'):
            bus = bus+1
            ones = np.ones((value['bottomright']['y']-value['topleft']['y'],value['bottomright']['x']-value['topleft']['x']))

            bounding_box = [value['topleft']['x']-5,value['topleft']['y']-5,value['bottomright']['x']-value['topleft']['x']-5,value['bottomright']['y']-value['topleft']['y']-5]

            a[bounding_box[1]:bounding_box[1] + bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]] = 1
        if(value["label"]=='truck'):
            truck = truck+1
            ones = np.ones((value['bottomright']['y']-value['topleft']['y'],value['bottomright']['x']-value['topleft']['x']))

            bounding_box = [value['topleft']['x']-5,value['topleft']['y']-5,value['bottomright']['x']-value['topleft']['x']-5,value['bottomright']['y']-value['topleft']['y']-5]

            a[bounding_box[1]:bounding_box[1] + bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]] = 1
        if(value["label"]=='motorbike'):
            motorbike = motorbike+1
            ones = np.ones((value['bottomright']['y']-value['topleft']['y'],value['bottomright']['x']-value['topleft']['x']))

            bounding_box = [value['topleft']['x']-5,value['topleft']['y']-5,value['bottomright']['x']-value['topleft']['x']-5,value['bottomright']['y']-value['topleft']['y']-5]

            a[bounding_box[1]:bounding_box[1] + bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]] = 1
        if(value["label"]=='bicycle'):
            bicycle = bicycle+1
            ones = np.ones((value['bottomright']['y']-value['topleft']['y'],value['bottomright']['x']-value['topleft']['x']))

            bounding_box = [value['topleft']['x']-5,value['topleft']['y']-5,value['bottomright']['x']-value['topleft']['x']-5,value['bottomright']['y']-value['topleft']['y']-5]

            a[bounding_box[1]:bounding_box[1] + bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]] = 1

    return a

def getDensity(frame,tfnet):
    ans = getdensity(frame,tfnet)
    ans = ans*255
    hist,bins = np.histogram(ans,256,[0,255])
    den_ans = hist[255]/(hist[0]+hist[255])

    return den_ans
