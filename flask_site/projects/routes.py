import os
from flask import current_app, render_template, url_for, flash, redirect, request, Blueprint

# Face Privacy
from flask_site.projects.face_privacy.forms import BlurInputFace
from flask_site.projects.face_privacy.utils import save_face_picture, cleanup
from flask_site.projects.face_privacy.program_files.yolo_detect import yolo_face_detection
from flask_site.projects.face_privacy.program_files.haar_detect import haar_face_detection

# Anime Recommendation System
from flask_site.projects.anime_rec.forms import AnimeRec
from flask_site.projects.anime_rec.program_files.recommender import content_based

projects = Blueprint('projects', __name__)


# projects page
@projects.route("/projects")
def projects_main():
    return render_template('projects_html/face_privacy.html', title='Face Privacy')


@projects.route("/projects/face_privacy", methods=['GET', 'POST'])
def face_privacy():
    image_file = url_for('static', filename='project_showcase_pics/index.png')
    yolo_image_out = url_for('static', filename='project_showcase_pics/index_haar_output.png')
    haar_image_out = url_for('static', filename='project_showcase_pics/index_yolo_output.png')
    form = BlurInputFace()
    if form.validate_on_submit():
        if form.picture.data:  # blur the input picture if it has a face

            # empty directory of face images so we can process on just the new input image for face privacy
            path_to_faces = (os.path.join(current_app.root_path, 'static/face_image/'))
            cleanup(path_to_faces)
            image_name = save_face_picture(form.picture.data)
            image_no_ext = os.path.splitext(image_name)[0]
            image_file = url_for('static', filename='face_image/' + image_name)

            # now run face privacy and display to screen
            image_file_path = (os.path.join(current_app.root_path, 'static/face_image/' + image_name))

            # YOLO
            yolo_model = (os.path.join(current_app.root_path,
                                       'projects/face_privacy/program_files/yolov3-face.cfg'))
            yolo_weights = (os.path.join(current_app.root_path,
                                         'projects/face_privacy/program_files/yolov3-wider_16000.weights'))
            yolo_classes = (os.path.join(current_app.root_path,
                                         'projects/face_privacy/program_files/yolov3_classes.txt'))
            yolo_face_detection(image_file_path, yolo_model, yolo_weights, yolo_classes, path_to_faces)
            yolo_image_out = url_for('static', filename='face_image/' + image_no_ext + '_yolo_output.png')

            # HAAR
            xmlPath = (os.path.join(current_app.root_path,
                                    'projects/face_privacy/program_files/haarcascade_frontalface_default.xml'))
            scaling = 1.1
            size = 10
            haar_face_detection(image_file_path, xmlPath, scaling, size, path_to_faces)
            haar_image_out = url_for('static', filename='face_image/' + image_no_ext + '_haar_output.png')

            flash('If there was a face then it was ideally blurred! :D', 'success')

    return render_template('projects_html/face_privacy.html',
                           title='Face Privacy',
                           image_file=image_file,
                           yolo_image_out=yolo_image_out,
                           haar_image_out=haar_image_out,
                           form=form)


@projects.route("/projects/anime_rec", methods=['GET', 'POST'])
def anime_rec():
    form = AnimeRec()
    if form.validate_on_submit():

        class Anime_Args:
            def __init__(self):
                self.dataset_path = os.path.join(current_app.root_path, 'projects/anime_rec/program_files/Anime.csv')
                self.username = form.username.data if form.username.data else None
                self.sel_anime = form.sel_anime.data
                self.watching_list = True if form.watching_list.data else False
                self.anime_images = 'anime_imgs'
                self.num_recs = 1

        args = Anime_Args()

        if form.num_recs.data <= 0:
            args.num_recs = 1
        elif form.num_recs.data >= 11:
            args.num_recs = 10
        else:
            args.num_recs = form.num_recs.data

        recommendations, image_urls, sel_anime = content_based(args)
        image_urls_path = [url_for('static', filename=url) for url in image_urls]

        flash('Here are some recommendations! :D', 'success')
        return render_template('projects_html/anime_rec_output.html',
                               title='Anime Recommendation System',
                               recs=zip(recommendations, image_urls_path),
                               anime_name=sel_anime,
                               form=form)

    return render_template('projects_html/anime_rec.html',
                           title='Anime Recommendation System',
                           form=form)
