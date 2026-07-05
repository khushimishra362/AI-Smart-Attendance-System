import face_recognition
def generator_encoding(image_path):
    image=face_recognition.load_image_file(image_path)
    encodings=face_recognition.face_encodings(image)
    if len(encodings)==0:
        return None
    return encodings[0]
if __name__=="__main__":
    encodings=generator_encoding(
        "photos/Khushi/1.jpg"
    )
    print(type(encodings))
    print(len(encodings))


