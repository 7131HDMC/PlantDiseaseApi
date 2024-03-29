from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import tensorflow as tf
import numpy as np
from io import BytesIO

import json

model = tf.keras.models.load_model('app/plant_disease_model.h5')
diseases = json.load(open('app/class_indices.json'))

description = """
Utilizing a Convolutional Neural Network (CNN), the Plant Disease API can identify plant diseases through images and generate text with OpenAI API to suggest treatments for the respective disease or similar condition.

## Predict

Predicts one of 38 features, being a disease or not, and return a dictionary with instruction about the plant disease/condition and how to treat it. The treatment text is generated by openai api.

The features are: \n `["Apple-Apple scab", "Apple-Black rot", "Apple-Cedar apple rust", "Apple-healthy", "Blueberry-healthy", "Cherry (including sour)-Powdery mildew", "Cherry (including sour)-healthy", "Corn (maize)-Cercospora leaf spot Gray leaf spot", "Corn (maize)-Common rust ", "Corn (maize)-Northern Leaf Blight", "Corn (maize)-healthy", "Grape-Black rot", "Grape-Esca (Black Measles)", "Grape-Leaf blight (Isariopsis Leaf Spot)", "Grape-healthy", "Orange-Haunglongbing (Citrus greening)", "Peach-Bacterial spot", "Peach-healthy", "Pepper, bell-Bacterial spot", "Pepper, bell-healthy", "Potato-Early blight", "Potato-Late blight", "Potato-healthy", "Raspberry-healthy", "Soybean-healthy", "Squash-Powdery mildew", "Strawberry-Leaf scorch", "Strawberry-healthy", "Tomato-Bacterial spot", "Tomato-Early blight", "Tomato-Late blight", "Tomato-Leaf Mold", "Tomato-Septoria leaf spot", "Tomato-Spider mites Two-spotted spider mite", "Tomato-Target Spot", "Tomato-Tomato Yellow Leaf Curl Virus", "Tomato-Tomato mosaic virus", "Tomato-healthy"]`

The model has been trained with a public dataset from [Kaggle](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset).
"""

app = FastAPI(
    title="Plant Disease",
    description=description,
    summary="",
    version="0.0.1",
    contact={
        "name": "Hari",
        "url": "https://www.linkedin.com/in/hari-dasa/",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

@app.post('/predict')
async def predict(img: UploadFile=File(...), tags=['predict']):
    """        
    #### Args: 
    \ndata (UploadFile): A image file of a plant leaf.
    #### Returns:
    \ndict: A dictionary containing the predicted class and the treatment text.
    """

    img = load_image_into_numpy_array(await img.read())
    offset = tf.constant(255.0)
    tensor_img = tf.image.resize(tf.expand_dims(tf.image.convert_image_dtype(img, dtype=tf.float32), 0), [256, 256], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

    tensor_img_scaled = tf.divide(tensor_img, offset)

    prediction = model.predict(tensor_img_scaled)

    class_names = list(diseases.keys())
    class_name = class_names[
        np.argmax(prediction)
    ]

    return { 'predicted_class': {
            class_name: diseases[class_name]
        }}

