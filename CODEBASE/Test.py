# Import required packages 
import sys
import cv2 
import pytesseract 
import sqlite3


#name=input("Enter name of the parameter to find")
#length=int(input("Enter the length of parameter"))
  
# Mention the installed location of Tesseract-OCR in your system 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  
# Read image from which text needs to be extracted 
img = cv2.imread("../Dataset/s5.png") 
  
# Preprocessing the image starts 
  
# Convert the image to gray scale 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# Performing OTSU threshold 
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
  
# Specify structure shape and kernel size.  
# Kernel size increases or decreases the area  
# of the rectangle to be detected. 
# A smaller value like (10, 10) will detect  
# each word instead of a sentence. 
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
  
# Appplying dilation on the threshold image 
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
  
# Finding contours 
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                 cv2.CHAIN_APPROX_NONE) 
  
# Creating a copy of image 
im2 = img.copy()   
# Looping through the identified contours 
# Then rectangular part is cropped and passed on 
# to pytesseract for extracting text from it 


#id_name and length to be set as per the id card which you are using this model for
id_name='ID No'
length=10

for cnt in contours: 
    x, y, w, h = cv2.boundingRect(cnt) 
      
    # Drawing a rectangle on copied image 
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (255,0,0), 2) 
      
    # Cropping the text block for giving input to OCR 
    cropped = im2[y:y + h, x:x + w]   
    # Apply OCR on the cropped image 
    text = pytesseract.image_to_string(cropped) 
    print(text)
    nid=''
    for i in range(len(text)):
        
        if(text[i]==id_name[0]):
            compare=text[i:i+len(id_name)]
            i=i+len(id_name)+1
            if(compare==id_name):
                while text[i]==' ':
                    i=i+1
                nid=text[i:i+length]
    


conn = sqlite3.connect('../TestDB.db')  
c = conn.cursor() 
c.execute('''SELECT * FROM students where STUDENT_ID=?''',(nid,))
result=c.fetchone()
#print(result[0])
if result is None:
    print("STUDENT RECORD DOES NOT EXIST")
else:
    print("STUDENT RECORD EXISTS\nDETAILS:")
    print("REGISTRATION ID: " +result[0] + "\n" + "FATHER NAME: " + result[1] + "\n" + "MOTHER NAME: " + result[2] + "\n" + "Email: " + result[3] + "\n" + "CONTACT: "+ str(result[4]) )

   