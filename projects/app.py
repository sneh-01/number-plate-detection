from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import easyocr
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'E:\\number plate\\projects\\static\\uploads'

# Load the EasyOCR model
reader = easyocr.Reader(['en'])

# Path to the pre-trained Haar cascade classifier for license plate detection
harcascade = "haarcascade_russian_plate_number.xml"

# Function to process the uploaded image
def process_image(image_path):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(harcascade)
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
    results = []
    for (x, y, w, h) in plates:
        area = w * h
        if area > 500:
            img_roi = img[y: y + h, x: x + w]
            result = reader.readtext(img_roi)
            results.append(result)
    return results

@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Construct the file path
        print("File path:", file_path)  # Debug print statement
        file.save(file_path)
        result = process_image(file_path)
        return render_template('result.html', result=result)


# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return 'No file part'

#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file'

#     if file:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         results = process_image(file_path)
#         return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
