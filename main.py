from fastapi import FastAPI, File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf



app = FastAPI()

MODEL = tf.keras.models.load_model("E:\Work force\BSc\Final Project\COCOBOT\Models\model_cocobot.h5")
CLASS_NAMES = ["CCI_Caterpillars","CCI_Leaflets","WCLWD_DryingofLeaflets","WCLWD_Flaccidity","WCLWD_Yellowing"]

@app.get("/ping")
async def ping():
    return "Hello world"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    
    image = read_file_as_image(await file.read())

    img_batch = np.expand_dims(image,0)

    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return{
        'class': predicted_class,
        'confidence': float(confidence)
    }



if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)