from fastapi import APIRouter, File, UploadFile
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch
import io

router = APIRouter()

# Load model and processor
# This part runs when the module is imported, which happens once on server startup.
model_name = "wambugu71/crop_leaf_diseases_vit"
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

# Treatment recommendations dictionary
treatment_recommendations = {
    "Corn___Common_Rust": "Apply fungicides like mancozeb or propiconazole. Plant resistant hybrids.",
    "Corn___Gray_Leaf_Spot": "Use fungicides and practice crop rotation. Resistant hybrids are recommended.",
    "Corn___healthy": "Your corn plant is healthy. Continue with good agricultural practices.",
    "Corn___Leaf_Blight": "Apply foliar fungicides. Ensure good field drainage and crop rotation.",
    "Potato___Early_Blight": "Apply fungicides containing chlorothalonil or mancozeb. Remove and destroy infected leaves.",
    "Potato___Healthy": "Your potato plant is healthy. Keep up the good work.",
    "Potato___Late_Blight": "Use fungicides like metalaxyl or chlorothalonil. Destroy infected plants to prevent spread.",
    "Rice___Brown_Spot": "Apply fungicides and ensure balanced nutrition. Use resistant varieties.",
    "Rice___Healthy": "Your rice plant is healthy. Maintain proper water and nutrient management.",
    "Rice___Leaf_Blast": "Use fungicides and resistant varieties. Avoid excessive nitrogen fertilization.",
    "Wheat___Brown_Rust": "Apply fungicides and plant resistant varieties. Remove volunteer wheat plants.",
    "Wheat___Healthy": "Your wheat plant is healthy. Monitor for any signs of pests or diseases.",
    "Wheat___Yellow_Rust": "Use fungicides and resistant varieties. Early detection and spraying are crucial.",
    "Invalid": "The image could not be classified. Please try again with a clearer image of a plant leaf.",
}

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Accepts an image file, and returns the predicted disease and treatment recommendation.
    """
    # Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Make a prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Get the predicted class
    predicted_class_idx = logits.argmax(-1).item()
    predicted_class = model.config.id2label[predicted_class_idx]

    # Get treatment recommendation
    treatment = treatment_recommendations.get(predicted_class, "No specific treatment recommendation available.")

    return {
        "disease": predicted_class.replace("___", " "),
        "confidence": torch.nn.functional.softmax(logits, dim=-1)[0][predicted_class_idx].item(),
        "treatment": treatment,
        "severity": "medium" # Placeholder, this can be improved with more advanced logic
    }
