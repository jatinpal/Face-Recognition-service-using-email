
from __future__ import print_function
import click
import os
import re
import getpass
import face_recognition.api as face_recognition
import PIL.Image
import numpy as np
import gmail

user = "facereco1.0@gmail.com"
pwd = "Facereco123."
known_people_folder = "/media/jatin/Work/Work/FaceRecognition/db"

def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

        if len(encodings) == 0:
            click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings

def print_result(src, filename, name, distance, show_distance=False):
    
    gmail.reply(user, pwd, src, filename, name)
    
    if show_distance:
        print("{},{},{}".format(filename, name, distance))
    else:
        print("{},{}".format(filename, name))


def test_image(src, image_to_check, known_names, known_face_encodings, tolerance=0.6, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)

    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        if True in result:
            [print_result(src, image_to_check, name, distance, show_distance) for is_match, name, distance in zip(result, known_names, distances) if is_match]
        else:
            print_result(src, image_to_check, "unknown_person", None, show_distance)

    if not unknown_encodings:
        print_result(image_to_check, "no_persons_found", None, show_distance)


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def match(known_people_folder, image_to_check, src, tolerance = 0.5, show_distance = False):
    
    known_names, known_face_encodings = scan_known_people(known_people_folder)
    test_image(src, image_to_check, known_names, known_face_encodings, tolerance, show_distance)


if __name__ == "__main__":  
    user = input("Enter admin emailId:")
    pwd = getpass.getpass('Enter password: ')
    
    gmail.getImages(user, pwd)
    
    for src in gmail.fetched_imgs.keys():
        for img in gmail.fetched_imgs[src]:
            match(known_people_folder,img, src)
            
        
    
        
                    
    
    
