# AUTOMATIC LICENSE PLATE RECOGNITION USING PYTHON AND RASPBERRY PI

![github1](https://user-images.githubusercontent.com/73076057/130198019-782b3b50-0049-408d-9244-cceee79ca85b.png)
![GitHub all releases](https://img.shields.io/github/downloads/Othm01100001n/License-Plate-Recognition-Garage-Guardian-/total)                                                                         ![Twitter Follow](https://img.shields.io/twitter/follow/othmanali02?style=social)                                                                  ![GitHub last commit](https://img.shields.io/github/last-commit/Othm01100001n/License-Plate-Recognition-Garage-Guardian-)

## About Project
Let's say you own a big company with a very large parking lot (presumably) and you would like to identify employee vehicles entering both in and out of the garage. 
The first thing that should come to mind is using a *camera* to capture footage of these cars going through the gate, or you could choose the intellectual option, ehm... and purchase a License Plate detection Camera, which is unsurprisingly, the best possible solution for this problem.

                                    
Now, machine learning in python has allowed me to make a device that can sense when a car is near and turn on a camera, which processes the captured image (of the
vehicle at a certain angle) and sends an email to the client with the taken image of the car, a text with the license plate number, and a cropped image of the license plate. 


## 🧬 Material
- Raspberry PI 3 B+
- PI-Camera(or any good quality camera)
- Python 3.7.3
- a good old Breadboard
- Ultra-sonic sensor
- Jumper Wires
- One 1.5k ohm Resistor
- One 1k ohm Resistor                
                  
## ⚙️ Installation
The installation process goes the same for both PC and Raspberry PI, with a few modifications on the PI for the Easyocr library...
- Download and install python from the official website, preferably python 3.7 or later https://www.python.org/downloads/release/python-370/
- Install OpenCV using terminal `python3 -m pip install opencv-python`
- Install Numpy using terminal`python3 -m pip install numpy`
- On your PC, you can download and install Pytorch https://pytorch.org/get-started/locally/
- On your Raspberry PI, you can install Pytorch by following this simple Youtube tutorial https://youtu.be/weHvI6j4OT8
- Install the EasyOcr library `python3 -m pip install easyocr`
  
## 💡 Setup
**Connect the pins as such**![Distance-Sensor-Fritz](https://user-images.githubusercontent.com/73076057/130138629-15da5e84-b81e-402f-988d-feedf4035a4e.png)
![IMG_8360](https://user-images.githubusercontent.com/73076057/130138787-7685f5ff-9496-4cf4-a432-13eb5bad516c.jpg)
The camera should be set on a 60 degree angle above the wall for proper reading results. *image attached below*
![Camera](https://user-images.githubusercontent.com/73076057/130151109-495c0751-7d25-47fe-9fb6-b9621f553992.jpg)


## 👨‍💻 Programming
Attached to this Repo: you can find the file **Trigger.py**, which is the backbone of this device, considering it measures the distance using the distance sensor
and based on the output, executes **PlateRecognition.py** as shown below
![triggerifstatement](https://user-images.githubusercontent.com/73076057/130140573-c2b3a007-181d-40c6-80ff-2f08674e7ee2.png)
Running **Trigger.py** from the RaspberryPI terminal should look like this:![PIdetection](https://user-images.githubusercontent.com/73076057/130140927-12cc661b-a312-4345-8b51-9d3287d1c5b6.png)
Since the Distance is less than 50 centimeters(which is for testing purposes ofcourse), **Trigger.py** executes **PlateDetection.py**.
## 🐍 PlateRecognition.py
I split the explanation of this code into **FIVE** simple parts...
- **Image Capture**:
The camera runs, and the first frame is stored in the variable "img" which is later proccessed.
```python
pic = cv2.VideoCapture(0)
ret,img = pic.read()
#stores image in variable img
while(True):
    cv2.imwrite('image.jpg', img)
    break
pic.release()
cv2.destroyAllWindows()
```
- **image proccessing**: This bit is explained in the code as comments, but it basically modifys the captured image, refines edges and adds contours preparing it for edge detecting, or rectangular shape detection that suspiciously happens to be the shape of License plates 😳.
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
.
.
.
.
new_image = cv2.drawContours(mask, [location], 0,255,-1)
new_image = cv2.bitwise_and(img,img, mask=mask)
```
- **cropped image**: This bit of code looks for the mentioned rectangular shaped after refining edges
```python
(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1 : x2 + 1 , y1 : y2 + 1]
plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
cv2.imwrite('cropped_image.jpg', cropped_image)
```
- **Convert Cropped Image to Text**: Using Easyocr literally makes this step a piece of cake, it takes the cropped image AKA the license plate as input, and converts it to text! although it is worth mentioning that there is a significantly low percentage of error, that could be for reasons such that the numbers have dirt on them, or the quality of the 
camera isn't good enough.
```python
reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)
result = reader.readtext(cropped_image, detail=0)
separator = ", "
result = separator.join(result)
print(result)
```
- **Email the Result**: After making a special Email for the project and activating less secure apps on gmail.
```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 #don't change this number
#Gmail username and password for the Email account you choose to be associated with your project, you have to enable less secure apps in order for it to work
GMAIL_USERNAME = 'yourprojectsemail@gmail.com'
GMAIL_PASSWORD = 'yourprojects'email'ssecretpassword'
```
![Screenshot 2021-08git104935](https://user-images.githubusercontent.com/73076057/130200074-73373ed3-7d08-4010-b832-35ae88c58e53.png)

## Support
This project is **FREE** and completely open source, I hope you found this useful and helpful. 
If you would like to support me for my future projects or chat, you can buy me a coffee here https://www.buymeacoffee.com/othmanali02
![infinite](https://user-images.githubusercontent.com/73076057/130128647-5599ebfe-bea6-4b64-a501-c7fa32128bbd.png)

