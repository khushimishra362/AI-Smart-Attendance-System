import cv2
import os
import time
def capture_student_images(student_name):
    folder_path=os.path.join(
        "photos",
        student_name
    )
    os.makedirs(folder_path,exist_ok=True)
    camera=cv2.VideoCapture(0)
    image_count=0
    poses=["Look at camera"]
    while image_count<5:
        ret,frame=camera.read()
        if not ret:
            continue
        cv2.putText(
            frame,
            "Look at camera",
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )
        cv2.namedWindow("Capture Student Images",cv2.WINDOW_NORMAL)
        
        cv2.imshow(
            "Capture Student Images",
            frame
        )

        key=cv2.waitKey(7000)
        
        image_count+=1
        image_path=os.path.join(
            folder_path,
            f"{image_count}.jpg"
        )
        cv2.imwrite(
            image_path,
            frame
        )
        print(
            f"capture{image_count}/5"
        )
    camera.release()
    cv2.destroyAllWindows()
    return"student registered successfully"       
if __name__=="__main__":
    capture_student_images("Khushi")
