from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import tensorflow as tf
import numpy as np
from io import BytesIO

import json

model = tf.keras.models.load_model('app/plant_disease_model.h5')
class_names = json.load(open('app/class_indices.json'))

description = """
PlantDiseaseHD API is an application that employs a custom machine learning model, utilizing a simple Convolutional Neural Network (CNN), to identify plant diseases through images. 
The model has been trained with a public dataset from Kaggle
"""
tags_metadata = [
    {
        "name": "predict",
        "description": 'This endpoint receives an image and predicts one of the following classes: \n ["Apple-Apple scab", "Apple-Black rot", "Apple-Cedar apple rust", "Apple-healthy", "Blueberry-healthy", "Cherry (including sour)-Powdery mildew", "Cherry (including sour)-healthy", "Corn (maize)-Cercospora leaf spot Gray leaf spot", "Corn (maize)-Common rust ", "Corn (maize)-Northern Leaf Blight", "Corn (maize)-healthy", "Grape-Black rot", "Grape-Esca (Black Measles)", "Grape-Leaf blight (Isariopsis Leaf Spot)", "Grape-healthy", "Orange-Haunglongbing (Citrus greening)", "Peach-Bacterial spot", "Peach-healthy", "Pepper, bell-Bacterial spot", "Pepper, bell-healthy", "Potato-Early blight", "Potato-Late blight", "Potato-healthy", "Raspberry-healthy", "Soybean-healthy", "Squash-Powdery mildew", "Strawberry-Leaf scorch", "Strawberry-healthy", "Tomato-Bacterial spot", "Tomato-Early blight", "Tomato-Late blight", "Tomato-Leaf Mold", "Tomato-Septoria leaf spot", "Tomato-Spider mites Two-spotted spider mite", "Tomato-Target Spot", "Tomato-Tomato Yellow Leaf Curl Virus", "Tomato-Tomato mosaic virus", "Tomato-healthy"]',
    }
]

app = FastAPI(
    title="PlantDiseaseHD",
    description=description,
    summary="Detect commom plant diseases",
    version="0.0.1",
    contact={
        "name": "Hari Dasa",
        "url": "https://www.linkedin.com/in/hari-dasa/",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi=tags_metadata
)


def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

# And in order to interact with our model, we need a post method, which will 
# receive the data, predict with the model and return the prediction result.
# So just like above `@app.predict("/predict/")` tells FastAPI that the 
# function right below is in charge of handling requests that go to this 
# path (’/predict/’).
# This means that we are creating another API path called /predict/ which 
# should be used to pass the data to the model and this incoming data will be 
# handled by the predict function
@app.post('/predict')
async def predict(img: UploadFile=File(...), tags=['predict']):
    """
    Predicts the class of a given set of features.

    Args:
        data (UploadFile): A image file of plant leaf.
    Returns:
        dict: A dictionary containing the predicted leaf class.
    """   
    img= load_image_into_numpy_array(await img.read())   
    # img = tf.keras.preprocessing.image.load_img(data.file_name, target_size=(256, 256))
    offset = tf.constant(255.0)
    # Convert data-type to Float and Expand dimensionsc
    tensor_img = tf.image.resize(tf.expand_dims(tf.image.convert_image_dtype(img, dtype=tf.float32), 0), [256, 256], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

    # Re-scaling the image (Dividing by 255.0)
    tensor_img_scaled = tf.divide(tensor_img, offset)
    # img_arr = tf.keras.preprocessing.image.img_to_array(img)

    prediction = model.predict(tensor_img_scaled)
    print(prediction)
    class_name = class_names[
        np.argmax(prediction)
    ]
    return {'predicted_class': class_name}

