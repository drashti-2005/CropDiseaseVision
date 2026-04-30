from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
import traceback
from backend.services.inference import run_inference, get_model_status

router = APIRouter()

@router.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    if not get_model_status():
        raise HTTPException(status_code=500, detail="Model is not loaded. Ensure model/trained_model.h5 exists and server was restarted.")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        result = run_inference(image)
        return result
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
