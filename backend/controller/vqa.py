import io
from PIL import Image
from transformers import BlipProcessor,BlipForQuestionAnswering

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

def answer_image_question(img_bytes: bytes, question: str) -> str:
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    inputs = processor(image, question, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)