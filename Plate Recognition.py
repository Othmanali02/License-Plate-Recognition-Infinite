import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import time
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#img = cv2.imread('IMG_7.jpg')

#turns on camera and processes the first frame

pic = cv2.VideoCapture(0)
ret,img = pic.read()

#stores image in variable img

while(True):
    cv2.imwrite('image.jpg', img)
    break
pic.release()
cv2.destroyAllWindows()

#modifying image and adding contours

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(bfilter, 30, 200)
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key = cv2.contourArea, reverse=True)[:10]
location = None
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.018 * peri , True)
    if len(approx) == 4:
        location = approx
        break

mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0,255,-1)
new_image = cv2.bitwise_and(img,img, mask=mask)

#cropping the image based on a rectangular shape similiar to a license plate 

(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1 : x2 + 1 , y1 : y2 + 1]
plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
cv2.imwrite('cropped_image.jpg', cropped_image)

#translating the cropped image AKA license plate into text
#VERY IMPORTANT NOTE -- Because the Raspberry PI proccessor isn't as good as your PC's, this part can be commented for the sake of faster processing.

reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)
result = reader.readtext(cropped_image, detail=0)
separator = ", "
result = separator.join(result)
print(result)

#this is a replacement value for result, depends on your boards GPU capabilities...
#result = 0

#reserving a server on gmail

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 #don't change this number

#Gmail username and password for the Email account you choose to be associated with your project, you have to enable less secure apps in order for it to work
GMAIL_USERNAME = 'yourprojectsemail@gmail.com'
GMAIL_PASSWORD = 'yourprojectemailpassword'

today = date.today()
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

class Emailer:
    def sendmail(self, recipient, subject, content, image1, image2):
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME
        emailData.attach(MIMEText(content))
        
        imageData1 = MIMEImage(open(image1, 'rb').read(), 'jpg')
        imageData1.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData1)

        imageData2 = MIMEImage(open(image2, 'rb').read(), 'jpg')
        imageData2.add_header('Content-Disposition', 'attachment; filename="cropped_image.jpg"')
        emailData.attach(imageData2)

        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
        session.quit

sender = Emailer()
image1 = 'image.jpg'
image2 = 'cropped_image.jpg'
sendTo = "othman90hijawi@gmail.com"
emailSubject = "Infinite Security Report"
emailContent = (f"{today}\n{current_time}\nThe Vehicle with the license plate:\n{result}\n\n*image attached below*\n\nis in front of the gate...\n\n\n- Engineered by Othman Ali")
sender.sendmail(sendTo, emailSubject, emailContent, image1, image2)
print("Email Sent")

#All rights go to my name and Repository
