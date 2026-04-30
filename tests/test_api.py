import requests
import io
from PIL import Image

# Create a small dummy image
img = Image.new('RGB', (10, 10), color='green')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='JPEG')
img_byte_arr = img_byte_arr.getvalue()

try:
    files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
    # Make sure we hit port 8080 which start.bat uses
    response = requests.post('http://127.0.0.1:8080/predict', files=files)
    print("Status:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Failed to connect:", e)
