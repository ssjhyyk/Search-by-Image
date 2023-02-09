from flask import Flask, request, render_template
from PIL import Image
import requests
import json
import cv2

app = Flask(__name__, static_folder="D:\SBI\Emptyfolder")

@app.route('./', methods=['GET', 'POST'])
def search_by_image():
    if request.method == 'POST':
        # Get uploaded image
        image = request.files['image']
        image.save("image.jpg")

        # Load the classifier
        face_cascade = cv2.CascadeClassifier("C:\Users\purpl\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\cv2\data\haarcascade_frontalface_default.xml")

        # Detect faces in the image
        image_np = cv2.imread("image.jpg")
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image_np, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Save the image with the detected faces
        cv2.imwrite(app.static_folder + "/image.jpg", image_np)


        # Convert image to binary form
        with open("image.jpg", "rb") as image_file:
            image_binary = image_file.read()

        # Prepare the request data
        data = {'image': image_binary}
        headers = {
            'Content-type': 'application/json',
            'X-RapidAPI-Key': '6f16f470abmshe4922832311b127p172dd1jsn2ba450e8a3d8',
            'X-RapidAPI-Host': 'bing-image-search1.p.rapidapi.com'
        }
        url = 'https://bing-image-search1.p.rapidapi.com/images/search'
        
        # Send the image to the search API
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Handle the API response
        # Handle the API response
        if response.status_code == 200:
            # Parse the JSON response
            results = response.json()
            similar_images = [] 
            # process results to find the similar images
            for image in results['value']:
                similar_images.append(image['contentUrl'])
            return render_template('results.html', image_path=url_for('static', filename='image.jpg'), results=similar_images)

        else:
            # Handle error
            return 'An error occurred: {}'.format(response.status_code)

    else:
        # Render the search by image page
        return render_template('search_by_image.html')

if __name__ == '__main__':
    app.run(debug=True)
