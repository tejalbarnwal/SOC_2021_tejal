import numpy as np 
import cv2
import math

img = cv2.imread("obama.png",1)
# print(type(img))

# print("image_shape", img.shape)
# image_shape (364, 238, 3)
img = cv2.resize(img,(720,720))
# img shape-> 360,240,3
# print(img.shape)
cv2.imshow("orginal_img",img)
# POOLING OPERATION

# making a np matrix filled with zeros of dim a,b,3
# h=360 , w = 240 , f= filter size , s=stride
# a = floor(h-f/s +1) , b=(w-f/s +1)

# parameters_defined
h = img.shape[0]
w = img.shape[1]
filter_size = 8 # 2x2 filter
stride = 8 # step size = 2
# size of output
a = math.floor((h-filter_size)/stride) + 1
b = math.floor((w-filter_size)/stride) + 1

output_img = np.zeros((a,b,3) , dtype="uint8") # float doubt

for row in range(0,h,stride):
  for col in range(0,w,stride):
    for i in range(3):

      # creating the filter for the patch
      hori_start = row
      hori_end = row + filter_size
      vert_start = col
      vert_end = col + filter_size

      a1 = math.floor((row-filter_size)/stride) + 1
      b1 = math.floor((col-filter_size)/stride) + 1

      output_img[a1,b1,i] = np.min(img[hori_start:hori_end , vert_start:vert_end , i ])
      # print(output_img)

output_img = cv2.resize(output_img, (360,360))
cv2.imshow("output_img",output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()








