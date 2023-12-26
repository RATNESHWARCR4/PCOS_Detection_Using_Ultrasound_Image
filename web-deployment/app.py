from flask import Flask, request, render_template
import os
from ultralytics import YOLO
import io
from PIL import Image
import cv2
import shutil
import os
from PIL import Image
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rat@1192'
# Specify the upload directory
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print("input file path",file_path)
        global imgpath
        upload_file.imgpath = file.filename
        image = cv2.imread(file_path)        
        model=YOLO("C:/ratneshwar/E/Vit college/sem7/MIA/Jcomp/pcos/best.pt")
        detect = model(file_path, save=True)
        lastest_folder, lastest_files, fileDir = give_file_path(file.filename)
        # C:\ratneshwar\E\Vit college\sem7\MIA\Jcomp\pcos\runs\segment\predict25\img_0_74.jpg
        predicted_image_path = "C:/ratneshwar/E/Vit college/sem7/MIA/Jcomp/pcos/runs/segment/"+lastest_folder+"/"+lastest_files
        predict_img = copy_img_to_static(predicted_image_path)
        cwd = os.getcwd()
        uploaded_image_path = os.path.join(cwd, 'uploads')
        uploaded_image_path = os.path.join(uploaded_image_path, upload_file.imgpath)
        
        final_predicted_img_path="predict/"+predict_img

        # return display_img()
        return render_template('result.html', uploaded_image=upload_file.imgpath, predicted_image=final_predicted_img_path)

        # return display(file.filename)


def give_file_path(filename):
    cwd = os.getcwd()
    folder_path = os.path.join(cwd,'runs')
    folder_path = os.path.join(folder_path,'segment')   

    subfolders = [f for f in os.listdir(
        folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_folder = max(subfolders, key=lambda x: os.path.getctime(
        os.path.join(folder_path, x)))
    directory = os.path.join(folder_path, latest_folder)
    files = os.listdir(directory)
    latest_files = files[0]
    # print(latest_files)
    # filename = os.path.join(folder_path, latest_folder, latest_files)
    # latest_folder = "runs/segment/"+latest_folder
    print("give_path", latest_folder, latest_files)
    fileDir = os.path.join(directory, latest_files)
    return latest_folder, latest_files, fileDir


@app.route('/')
def home():
    return render_template('index.html')


def copy_img_to_static(so):

    print("copy function")
    # Source and destination paths
    source_path = so  # Update with the actual source path
    destination_path = 'static/predict'  # Update with the actual destination path

    # Check if the source file exists
    if os.path.exists(source_path):
        # Extract the filename from the source path
        filename = os.path.basename(source_path)
        print(filename)
        
        # Construct the complete destination path
        destination_file_path = os.path.join(destination_path, filename)

        # Copy the file to the destination path
        try:
            shutil.copy(source_path, destination_file_path)
            print(f"Successfully copied {source_path} to {destination_file_path}")
        except shutil.SameFileError:
            print(f"Source and destination represent the same file: {source_path}")
        except IsADirectoryError:
            print(f"Destination {destination_file_path} is a directory.")
        except PermissionError:
            print(f"Permission denied.")
        except FileNotFoundError:
            print(f"Source {source_path} or destination {destination_path} not found.")
        except Exception as e:
            print(f"Error occurred: {e}")
    else:
        print(f"Source {source_path} not found.")
    return filename
    

if __name__ == '_main_':
    app.run(debug=True)