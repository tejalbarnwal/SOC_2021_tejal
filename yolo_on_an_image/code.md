# Yolo_on_an_image

Based on the youtube tutorial:https://youtu.be/h56M5iUVgGs

```python

import cv2
import numpy as np

#load yolo
net=cv2.dnn.readNet("yolov3.weights","yolov3.cfg")
classes=[]
with open ("coco.names","r") as f:
    classes=[line.strip() for line in f.readlines()]
print("classes are:",classes)
print("no. of classes are:",len(classes))

layer_names=net.getLayerNames()
print("no. of layers are:",len(layer_names))
print("layer names are:",layer_names)
#print(layer_names[199])

for i in net.getUnconnectedOutLayers():
    print(i)
    print(i[0])

output_layers=[layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
print("output layers are:",output_layers)

colors=np.random.uniform(0,255,size=(len(classes),3))
#img=cv2.imread("phone_camera_cup.jpg",1)
img=cv2.imread("room_ser.jpg",1)
#cv2.imshow("win1",img)

img=cv2.resize(img,None,fx=0.3,fy=0.3)
height,width,channels=img.shape
#cv2.imshow("win2",img)


blob=cv2.dnn.blobFromImage(img,0.00392,(608,608),(0,0,0),True,crop=False)
#print(blob)
#print("b are")
#print(blob.shape)

for i in range(3):
    win_name="blob"+str(i)
    cv2.imshow(win_name,blob[0][i])


net.setInput(blob)
outs=net.forward(output_layers)
print("outs ka shape:",np.array(outs).shape)
#print("entire0")
#print(outs[0])
print("len of entir0: ",len(outs[0]))
print(np.array(outs[0].shape))
#print("0 ka part")
#print(outs[0][0])
print("len of 0 ka part: ",len(outs[0][0]))
print(np.array(outs[0][0]).shape)


class_id_img=[]
confidence_img=[]
box_img=[]

for out in outs:
    for detection in out:
        scores=detection[5:]
        class_id=np.argmax(scores)
        confidence=scores[class_id]

        if confidence > 0.5:
            #object detected
            center_x=int(detection[0]* width)
            center_y=int(detection[1]*height)
            w=int(detection[2]*width)
            h=int(detection[3]*height)

            #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)

            x_tl=int(center_x- w/2)
            y_tl=int(center_y- h/2)

            box_img.append([x_tl,y_tl,w,h])
            confidence_img.append(float(confidence*100))
            class_id_img.append(class_id)

            #cv2.rectangle(img,(x_tl,y_tl),(x_tl+w,y_tl+h),(0,255,0),2)


print(np.array(box_img).shape)

indexes=cv2.dnn.NMSBoxes(box_img,confidence_img,0.4,0.3)
print(indexes)
for i in range(len(box_img)):
    if i in indexes:
        x,y,w,h=box_img[i]
        label=str(classes[class_id_img[i]])
        color=colors[i]
        #print(label)
        cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
        cv2.putText(img,label,(int(x+ w/4),int(y+h/4)),cv2.FONT_HERSHEY_SIMPLEX,1,color,2)

cv2.imshow("win2",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

```
