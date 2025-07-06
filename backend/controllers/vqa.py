import io
from PIL import Image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl", torch_dtype=torch.float16).to("cuda")

def answer_image_question_blip2(img_bytes: bytes, question: str):
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    inputs = processor(image, question, return_tensors="pt").to("cuda")
    out = model.generate(**inputs, max_new_tokens=64)
    return processor.decode(out[0], skip_special_tokens=True)
