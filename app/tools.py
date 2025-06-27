from PIL import Image
import base64
from io import BytesIO

def process_image(image_path):
    img=Image.open(image_path).convert('RGB')
    if img is Image:
        print("确实是图片")
    buffered=BytesIO()
    img.save(buffered,format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

