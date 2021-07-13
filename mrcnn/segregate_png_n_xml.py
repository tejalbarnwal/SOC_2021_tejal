import os
import shutil

path = "/home/tejal/Mask-RCNN-TF2/carla/test"
txt_path = os.path.join(path, "xml")
png_path = os.path.join(path, "png")
pdf_path = os.path.join(path, "pdf")


if not os.path.isdir(txt_path):
    os.makedirs(txt_path)
    print("text folder created")
    
    
if not os.path.isdir(png_path):
    os.makedirs(png_path)
    print("png folder created")
    
    
if not os.path.isdir(pdf_path):
    os.makedirs(pdf_path)
    print("pdf folder created")
    
        

#files = ['a.png' , 'b.pdf', 'c.txt']

files = [f for f in os.listdir("/home/tejal/Mask-RCNN-TF2/carla/test")]


for file in files:
  file_path = os.path.join(path, file)
  
  if file_path.endswith('.xml')==True:
    print('move file to text folder')
    shutil.move(file_path, txt_path)
  
  if file_path.endswith('.png')==True:
    print('move file to png folder')
    shutil.move(file_path, png_path)
  
  if file_path.endswith('.pdf')==True:
    print('move file to pdf folder')
    shutil.move(file_path, pdf_path)
