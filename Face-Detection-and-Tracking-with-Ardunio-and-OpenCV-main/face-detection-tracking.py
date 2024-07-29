import cv2
import serial, time
#change the ..path !!!!!! 
face_cascade = cv2.CascadeClassifier(
    "C:\\..path\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
cap=cv2.VideoCapture(1)
#COM4 is Ardunio Port. Check it and change according to your port. it may be COM3, COM4, COM5
ArduinoSerial=serial.Serial('COM6',9600,timeout=0.1)
time.sleep(1)

while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1)  #mirror the image
    #print(frame.shape)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,6)  #detect the face
    for x,y,w,h in faces:
        #sending coordinates to Arduino
        string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))
        #plot the center of the face
        cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
        #plot the roi
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    #plot the squared region in the center of the screen
    cv2.rectangle(frame,(640//2-30,480//2-30),
                 (640//2+30,480//2+30),
                  (255,255,255),3)
    #out.write(frame)
    cv2.imshow('img',frame)
    #cv2.imwrite('output_img.jpg',frame)
    '''for testing purpose
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    time.sleep(0.05)
    print('data from arduino:'+read)
    '''
    # press q to Quit
    if cv2.waitKey(10)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
