##############################################################################
# haar_detect.py - Haar cascades method for detecting faces and applying
#                  a blur.
#
# Copyright (C) 2019   Humza Syed
#
# This is free software so please use it however you'd like! :)
##############################################################################

import os
import cv2

"""
##############################################################################
# Haar Face detection
##############################################################################
"""


def haar_face_detection(image_file_path, xmlPath, scaling, size, save_path):
    """
    Detects faces in images and draws a bounding box around the faces using haar cascading method

    :param image_file_path : Path to the input image
    :param xmlPath : Path to the xml file for detecting the front of people's faces
    :param scaling : Parameter for classifier to determine the tolerance of small/big faces in image
    :param size    : Parameter for classifier to know what the minimum sized face is
    :param save_path : Path to where output image will be saved

    :returns:

    (Doesn't return anything except outputted images to the directory 'output_images')
    """

    # keep track of how many images processed on
    counter = 0

    # check file type
    file_type = image_file_path.split('.')[-1].lower()

    # if image file then do the following processing
    if file_type == 'png' or file_type == 'jpg' or file_type == 'jpeg':

        # read input image
        image = cv2.imread(image_file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # face and eye detection classifiers using haar features
        face_classifier = cv2.CascadeClassifier(xmlPath)

        # detect faces
        faces = face_classifier.detectMultiScale(
            gray_image,
            scaleFactor=scaling,
            minNeighbors=10,
            minSize=(size, size),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # draw rectangles around faces
        for (x, y, w, h) in faces:
            # draw the bounding box - commented out because I don't want a green box
            # around the faces, but left here if the user wants to add this in
            # cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

            # apply gaussian blur on faces
            face = image[y:y + h, x:x + w]
            face = cv2.GaussianBlur(face, (23, 23), 30)

            # put blurred face on new image
            image[y:y + face.shape[0], x:x + face.shape[1]] = face

        # cv2.imshow('Faces found', image)

        # strip file extension of original image so we can write similar output image
        # i.e.) people.png --> people_output.png
        image_file = os.path.splitext(image_file_path)[0]
        # cv2.imwrite(os.path.join(os.getcwd(), 'out_images_haar', (image_file + '_output.png')), image)
        cv2.imwrite(os.path.join(save_path, (image_file + '_haar_output.png')), image)
        # cv2.waitKey(0)
        cv2.destroyAllWindows()

        # print('Image {} was completed!'.format(counter))
        counter += 1

    # print('Processed all {} images! :D'.format(counter))
