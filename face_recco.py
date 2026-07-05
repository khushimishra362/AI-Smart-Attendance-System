"""import face_recognition
import cv2
import numpy as np 
import csv
import os
from datetime import datetime
import time

video_capture=cv2.VideoCapture(0)
abhishek_image=face_recognition.load_image_file("photos/abhishekface.jpeg")


abhilasha_image=face_recognition.load_image_file("photos/WIN_20260220_23_47_55_Pro.jpg")


khushi_image=face_recognition.load_image_file("photos/portfolio img.jpg")


archana_image=face_recognition.load_image_file("photos/mummy.jpeg")


abhishek_encoding=face_recognition.face_encodings(abhishek_image)[0]
abhilasha_encoding=face_recognition.face_encodings(abhilasha_image)[0]
khushi_encoding=face_recognition.face_encodings(khushi_image)[0]
archana_encoding=face_recognition.face_encodings(archana_image)[0]


known_faces_encoding=[
    abhishek_encoding,
    abhilasha_encoding,
    khushi_encoding,
    archana_encoding
]

known_faces_names=[
    "Abhishek Mishra",
    "Abhilasha Mishra",
    "Khushi Mishra",
    "Archana Mishra"
]

students=known_faces_names.copy()


face_locations=[] #THIS PART WAS ALREADY IN TRIPLE COMMA MEANS COMMENTED
face_encodings=[]
face_names=[]
s=True #TILL HERE

now=datetime.now()
current_date=now.strftime("%Y-%m-%d")
csv_file=f"{current_date}.csv"
file_exists=os.path.isfile(csv_file)

f=open(csv_file,"a",newline="")
Inwriter=csv.writer(f)
if not file_exists:
   Inwriter.writerow(["Name","Date","Time"])
marked_today=set()
print("camera is opening.Please press the (q) to close the camera")



while True:
    ret,frame=video_capture.read()
    if not ret:
        break                                                                                                                                                                                                                           
    small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    
    if len(face_locations)>0:
     print(f"face found:{len(face_locations)}",end="\r")
    if len(face_locations) >0: 
        face_encodings=face_recognition.face_encodings(rgb_small_frame,face_locations)
    else:
        face_encodings=[]
        face_names=[] 
    for face_encoding in face_encodings:
            matches=face_recognition.compare_faces(known_faces_encoding,face_encoding) 
            face_distance=face_recognition.face_distance(known_faces_encoding,face_encoding)
            best_matces_index=np.argmin(face_distance)
            name="unknown"
            if matches[best_matces_index]:
                name=known_faces_names[best_matces_index]
                face_names.append (name)
                if name in know_face_names: #THIS PART WAS ALREADY IN TRIPLE COMMA MEANS COMMENTED
                    if name in students:
                        students.remove(name)
                        print(students) #TILL THIS
            current_time=datetime.now().strftime("%H-%M-%S")
            today_date=datetime.now().strftime("%Y-%m-%d")
            if name !="unknown":
               if name not in marked_today:
                   Inwriter.writerow([name,current_time])
                   f.flush()
                   marked_today.add(name)
                   print(f"\n ATTENDANCE MARKED:{name}at{current_time}")
            else:
             print(f"\n{name}-Already marked today",end="\r")
    else:
        print(f"\n ? unknown face detected ",end="\r")
    for (top,right,bottom,left)in face_locations:
        top*=4
        right*=4
        bottom*=4
        left*=4

#green box
        cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)   
        cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,255,0),cv2.FILLED)
        if name=="unknown":
                    cv2.putText(frame,name,(left+6,bottom-6))  
        cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,255),2
    else:
               cv2.putText(frame,name,(left+6,bottom-6),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,0),2)
               cv2.imshow("attendance system",frame)
    cv2.imshow("attendance system",frame)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
 
 
video_capture.release()
cv2.destroyAllWindows()
f.close()
print(f"\n Camera is off ")
print(f"Attendance saved in:{csv_file}")
print(f"Today's Attendance:{marked_today}")"""


            
           

        

    
        
        
        








