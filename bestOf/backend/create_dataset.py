import identifyPeople
import cv2 as cv
from identifyPeople import crop_subjects_from_segmented_image as identify
from matplotlib import pyplot as plt
import os
import shutil


def make_set():
    unfound = 0

    print("Starting... ")

    new_set = 'bestOf/resources/identifiedFaces'
    directory = 'bestOf/resources/lfw'

    if os.path.isdir(new_set):
        shutil.rmtree(new_set)

    os.mkdir(new_set)

    for folder in os.listdir(directory):
        os.mkdir(new_set + '/' + folder + '_Identified')
        for img in os.listdir(os.path.join(directory, folder)):

            pik = cv.imread(os.path.join(directory, folder, img))
            image = cv.cvtColor(pik, cv.COLOR_BGR2RGB)

            faces, bounds = identify(image)
            if len(faces) == 0:
                unfound += 1

            for i, face in enumerate(faces):
                strings = img.split('.')
                name = ""
                if i > 0:
                    name = strings[0] + '_Identified' + str(i) + '.' + strings[1]
                else:
                    name = strings[0] + '_Identified' + '.' + strings[1]

                cv.imwrite(os.path.join(new_set, folder + '_Identified', name), face)


    print('Number of failed identifications: ', str(unfound))




crop_all_images():
    counter = 0
    counter_cropped = 0
    print('Starting to crop all images...')
    new_set = 'bestOf/resources/identifiedFacesCropped'
    directory = 'bestOf/resources/identifiedFaces'

    if os.path.isdir(new_set):
        shutil.rmtree(new_set)

    os.mkdir(new_set)

    for folder in os.listdir(directory):
        os.mkdir(new_set + '/' + folder + '_Cropped')
        print("Working on: " + folder)
        for i, img in enumerate(os.listdir(os.path.join(directory, folder))):
            counter += 1
            strings = img.split('.')
            name = strings[0] + str(i)

            cropped_list = crop_an_image(img, 0.15, 0.2)

            for pic in cropped_list:
                cv.imwrite(os.path.join(new_set, folder + '_Cropped', name), pic)
                counter_cropped += 1
        
        print("----Finished----\n")

    print("---------------------Done With Everything---------------------")
    print("Out of " + str(counter) + " images\n" + str(counter_cropped) + " cropped images were created")

def crop_an_image(image, x, y):
    height = int(image.shape[0] * y)
    length = int(image.shape[1] * x)

    left_cutoff = image[:, length:]
    top_cutoff = image[height:, :]
    right_cutoff = image[:, :length]
    bottom_cutoff = image[:height, :]

    return [left_cutoff, top_cutoff, right_cutoff, bottom_cutoff]

#make_set()
crop_all_images()