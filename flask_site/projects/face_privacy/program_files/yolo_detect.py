##############################################################################
# yolo_detect.py - YOLO cascades method for detecting faces and applying
#                  a blur.
#
# Copyright (C) 2019   Humza Syed
#
# This is free software so please use it however you'd like! :)
##############################################################################

import os
import cv2
import numpy as np
from imutils.video import FileVideoStream

"""
##############################################################################
# YOLOv3 Face detection
##############################################################################
"""


def yolo_face_detection(imgsPath, yolo_path, weights_file, classes_file, save_path):
    """
    Detects faces in images and draws a bounding box around the faces using yolo method.
    Also added the ability to blur faces in mp4 videos.

    :param imgsPath:    Path to the input images directory
    :param yolo_path:   Path to the yolo algorithm's config file
    :param weights_file:Pre-trained face weights for yolo algorithm
    :param classes_file:Classes text file for yolo algorithm
    :param save_path : Path to where output image will be saved

    :returns:

    (Doesn't return anything except outputted images to the directory 'output_images')
    """
    # keep track of how many images processed on
    image_counter = 0
    video_counter = 0

    for image_file in (os.listdir(imgsPath)):

        # image path
        image_path = os.path.join(imgsPath, image_file)

        # check file type
        file_type = image_path.split('.')[-1].lower()

        # read pre-trained model and config file to create network
        net = cv2.dnn.readNet(weights_file, yolo_path)

        # if image file then do the following processing
        if(file_type == 'png' or file_type == 'jpg' or file_type == 'jpeg'):
            # read input image
            image = cv2.imread(image_path)

            # scales values for blob from image
            scale = 0.00392

            # get class names
            with open(classes_file, 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            # we just have 1 class in this case, which is a face
            colors_list = [(0, 255, 0)]

            # Prepare image to run through network
            # create input blob
            blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

            # set input blob for the network
            net.setInput(blob)

            # run inference
            predictions = net.forward(get_output_layers(net))

            # obtain the confidences and apply blur to images
            get_confidences(image, predictions)

            # strip file extension of original image so we can write similar output image
            # i.e.) people.png --> people_output.png
            image_file = os.path.splitext(image_file)[0]
            #cv2.imwrite(os.path.join(os.getcwd(), 'out_images_yolo', (image_file + '_output.png')), image)
            cv2.imwrite(os.path.join(save_path, image_file + '_yolo_output.png'), image)
            cv2.destroyAllWindows()

            #print('Image {} was completed!'.format(image_counter))
            image_counter += 1

        # else if it's an mp4 video process the video
        elif(file_type == 'mp4'):

            # yes I know it's technically not an image (referring to image_path variable),
            # but videos are just a lot of images realistically
            video_stream = FileVideoStream(image_path).start()
            cam = cv2.VideoCapture(image_path)
            fps = cam.get(cv2.CAP_PROP_FPS)
            cam.release()

            # strip file extension of original image so we can write similar output image
            # i.e.) people.mp4 --> people_output.mp4
            video_file_name = os.path.splitext(image_file)[0]

            # checking if first time in the while loop
            first_time = True

            # scales values for blob from image
            scale = 0.00392

            # loops through the frames of the video stream
            while(True):
                # get the current frame and resize it to decrease processing
                frame = video_stream.read()

                # check if end of stream
                if(video_stream.more() != True):
                    break

                # create input blob
                blob = cv2.dnn.blobFromImage(frame,  scale, (416, 416), (0, 0, 0), True, crop=False)

                # set input blob for the network
                net.setInput(blob)

                # run inference
                predictions = net.forward(get_output_layers(net))

                # obtain the confidences and apply blur to frames
                frame = get_confidences(frame, predictions)

                if(first_time == True):
                    # we need the height and width during the first loop then we can start making the video
                    (height, width) = frame.shape[:2]

                    # save output video in mp4 format with 30fps
                    out_video = cv2.VideoWriter(
                        #os.path.join(os.getcwd(), 'out_images_yolo', video_file_name + '_output.avi'),
                        os.path.join(save_path, video_file_name + '_yolo_output_video.avi'),
                        cv2.VideoWriter_fourcc(*'MPEG'),
                        fps,
                        (width, height))
                    first_time = False

                # save frame to form the video
                out_video.write(frame)

            cv2.destroyAllWindows()
            out_video.release()

            #print('Video {} was completed!'.format(video_counter))
            video_counter += 1

    #print('Processed all {} images! :D'.format(image_counter))
    #print('Processed all {} videos! :D'.format(video_counter))


def get_output_layers(net):
    """
    Obtain output layer names in the architecture

    :param   net: yolo network

    :return  output_layers: output layers used in the net
    """

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def get_confidences(image, predictions):
    """
    Function meant to detect the faces in an image then calls
    the blurring function to blur these faces

    :param image: input image with faces
    :param predictions: predictions from the network used
    :return: blurred image
    """

    # initializations for detection
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.35  # 0.5
    nms_threshold = 0.4
    (height, width) = image.shape[:2]

    # get confidences, bounding box params, class_ids for each detection
    # ignore weak detections (under 0.5 confidence)
    for pred in predictions:
        for detection in pred:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if (confidence > 0.35):  # 0.5):
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # apply non-max suppresion
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # detections after nms
    for ind in indices:
        ind = ind[0]
        box = boxes[ind]
        x = max(0, round(box[0]))
        y = max(0, round(box[1]))
        w = max(0, round(box[2]))
        h = max(0, round(box[3]))

        # draw the bounding box - commented out because I don't want a green box
        # around the faces, but left here if the user wants to add this in
        # draw_bounding_box(image, classes, class_ids[ind], colors_list, x, y, w, h)

        # draw the blurred bounding box
        blur_detected_object(image, x, y, w, h)

    return image


def draw_bounding_box(image, classes, class_id, colors_list, x, y, w, h):
    """
    Draw bounding boxes in image based off object detected and apply a blur to the inside of the box

    :param  image:      read in image using opencv
    :param  classes:    list of classes
    :param  class_id:   specific class id
    :param  colors:     colors used for bounding box
    :param  x, y, w, h: dimensions of image

    :return (the class label and colored bounding box on the image)

    """

    # get label and color for class
    label = str(classes[class_id])
    color = colors_list[class_id]

    # draw bounding box with text over it
    cv2.rectangle(image, (x, y), ((x + w), (y + h)), color, 2)
    cv2.putText(image, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def blur_detected_object(image, x, y, w, h):
    """
    Apply a blur to the detected objects in the image

    :param  image:      read in image using opencv
    :param  x, y, w, h: dimensions of image

    :return (the blurred bounding box on the image)

    """
    # apply gaussian blur on faces
    face = image[y:y + h, x:x + w]
    face = cv2.GaussianBlur(face, (25, 25), 30)

    # put blurred face on new image
    face_y = face.shape[0]
    face_x = face.shape[1]

    image[y:y + face_y, x:x + face_x] = face