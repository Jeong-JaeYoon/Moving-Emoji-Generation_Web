# <!-- base line code : https://github.com/ibrahimokdadov/upload_file_python -->

import os
import PIL
from PIL import Image
from uuid import uuid4

from flask import Flask, request, render_template, send_from_directory, send_file
import paramiko
from paramiko import SSHClient
import time

__author__ = 'ibininja'

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
file_name = None

# Main page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def index1():
    return render_template("upload.html")

@app.route("/intro")
def index2():
    return render_template("project_info.html")

@app.route("/member")
def index3():
    return render_template("member.html")

@app.route("/gallery")
def index4():
    return render_template("gallery.html")

# Save uploaded image from user in public folder
@app.route("/upload/uploader", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'public/')
  
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))

    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # Selected option from user 
    style_option = request.form.get('style') 
    emotion_option = request.form.get('emotion')
    type_option = request.form.get('type')
    model_option = request.form.get('model')
    frame_option = request.form.get('frame')

    # Convert image format to jpg & resize image
    new_filename = Image.open(destination)
    new_filename.save(destination.split('.')[0]+'.jpg') 
    width, height = new_filename.size
    if (width != 1024) or (height != 1204):        
        img_resize_lanczos = new_filename.resize((1024, 1024), PIL.Image.LANCZOS)
        img_resize_lanczos.save(destination.split('.')[0]+'.jpg') 
    new_filename.close()

    want = filename.split('.')[0]    
    global file_name
    file_name = want + "."+ type_option

    localpath1=f'/workspace/moving/upload_file_python/src/public/{want}.png' 
    remotepath1=f'/..../{want}.png' # server path