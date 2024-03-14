from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import base64




def decode_image_from_base64(encoded_string):
            
            
                 encoded_string = encoded_string.split(',')[1]
    # رمزگشایی تصویر از رشته Base64
                 decoded_image = base64.b64decode(encoded_string)

    # تبدیل تصویر رمزگشایی شده به آرایه بایتی
                 image = Image.open(io.BytesIO(decoded_image))
                 
                 temp_image = io.BytesIO()
                 image.save(temp_image, format='JPEG')
                 temp_image.seek(0)

                 image_file = InMemoryUploadedFile(temp_image, None, 'temp.jpg', 'image/jpeg', temp_image.getbuffer().nbytes, None)  


                 return image_file