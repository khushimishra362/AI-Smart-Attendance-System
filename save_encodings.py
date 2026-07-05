import os
import pickle 
from encoding_utils import generator_encoding
def save_all_encodings():

    encoding_data = {}
    photos_folder = "photos"

    for student_name in os.listdir(photos_folder):

        student_path = os.path.join(
            photos_folder,
            student_name
        )

        if os.path.isdir(student_path):

            for image_name in os.listdir(student_path):

                image_path = os.path.join(
                    student_path,
                    image_name
                )

                encoding = generator_encoding(
                    image_path
                )

                print("Checking :", image_path)

                if encoding is None:
                    print("Face not found")

                else:

                    print("Encoding generated")

                    if student_name not in encoding_data:
                        encoding_data[student_name] = []

                    encoding_data[student_name].append(
                        encoding
                    )

    with open("encodings.pkl", "wb") as file:
        pickle.dump(
            encoding_data,
            file
        )

    return "Encodings saved successfully"    
if __name__=="__main__":
    print(save_all_encodings())               
                   
               
    
            