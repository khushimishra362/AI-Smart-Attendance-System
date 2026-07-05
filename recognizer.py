import face_recognition
import cv2
import numpy as np
from Attendance import mark_attendance
import pickle
import os
from datetime import datetime

last_unknown_saved=None

video_capture = cv2.VideoCapture(0)

with open ("encodings.pkl","rb") as file :
    encoding_data=pickle.load(file)
    print("students in encodings")
    print(encoding_data.keys())
for name ,encodings in encoding_data.items():
    print(name)
    print(type(encodings))
    print(len(encodings))    
known_faces_encoding=[]
known_faces_names=[]
for name,encoding in encoding_data.items():
    for encoding in encoding:
        known_faces_encoding.append(encoding)
        known_faces_names.append(name)
print("Known faces loaded : ",known_faces_names)    
print(type(known_faces_encoding))
#print(type(known_faces_encoding[0]))
print(len(known_faces_encoding))
#print(known_faces_encoding[0].shape)

def start_recognition():

    print("camera is opening. Please press q to close")

    while True:

        ret, frame = video_capture.read()

        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)

        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            face_locations
        )

        for (top, right, bottom, left), face_encoding in zip(
            face_locations,
            face_encodings):
            if len(known_faces_encoding)==0:
               print("no encodings found") 
               return
            
            for i,enc in enumerate(known_faces_encoding):
                print(i,type(enc))
                try:
                    print(enc.shape)
                except:
                     print("no shape")
            matches = face_recognition.compare_faces(
                known_faces_encoding,
                face_encoding
            )
            face_distance = face_recognition.face_distance(known_faces_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            min_distance = face_distance[best_match_index]
            print("Distance:", min_distance)
            if min_distance < 0.55:
                name = known_faces_names[best_match_index]
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    (0, 255, 0),
                    2
                )
                cv2.putText(
                    frame,
                    name,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )
                cv2.imshow(
                    "Attendance System",
                     frame
                )
                cv2.waitKey(2000)
                message = mark_attendance(name)
                print(message)
                video_capture.release()
                cv2.destroyAllWindows()
                return
            else:
                print("Unknown Person")
                global last_unknown_saved
                current_time = datetime.now()
                if (
                    last_unknown_saved is None
                    or
                    (current_time - last_unknown_saved).seconds > 30
                ):

                    if not os.path.exists("unknown_faces"):
                        os.makedirs("unknown_faces")
                    filename = current_time.strftime(
                        "%Y%m%d_%H%M%S.jpg"
                    )

                    filepath = os.path.join(
                        "unknown_faces",
                        filename
                    )

                    cv2.imwrite(
                        filepath,
                        frame
                    )

                    print(f"Unknown face saved: {filepath}")

                    last_unknown_saved = current_time

        cv2.imshow("Attendance System", frame)
        key=cv2.waitKey(1)
        if key== ord("q") or key== ord("Q"):
            break
    video_capture.release()
    cv2.destroyAllWindows()

    
    
    
            

