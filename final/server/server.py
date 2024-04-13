from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import easyocr

app = Flask(__name__, template_folder='E:/number plate/final/templates')

# Path to the pre-trained Haar cascade classifier for license plate detection
harcascade = "E:/number plate/model/haarcascade_russian_plate_number.xml"

# Create an EasyOCR reader instance
reader = easyocr.Reader(['en'])

# Function to process the uploaded image
def process_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        return None

    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform license plate detection
    plate_cascade = cv2.CascadeClassifier(harcascade)
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    results = []
    # Iterate over detected license plates
    for (x, y, w, h) in plates:
        area = w * h
        if area > 500:  # Adjust this threshold according to your needs
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number plate", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y + h, x: x + w]

            # Read text using EasyOCR
            result = reader.readtext(img_roi)
            results.append(result)
    
    return results

# Route to render the HTML page with the upload form
@app.route('/')
def upload_file():
    return render_template('index.html')

# Route to handle the file upload and process the image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        file_path = 'uploads/' + filename
        file.save(file_path)
        result = process_image(file_path)
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
