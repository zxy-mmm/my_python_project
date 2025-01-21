import requests
from PIL import Image, ImageFilter
from io import BytesIO
import pytesseract

# 下载验证码图片
url = 'https://fj.tzxm.gov.cn/eap/credit.getVerifyImg'
response = requests.get(url)

print(response)
# 确保请求成功
if response.status_code == 200:
    # 将图片内容读入内存
    img_data = BytesIO(response.content)
    # 使用Pillow库打开图片
    img = Image.open(img_data)
    
    # 图像预处理
    # 灰度化
    img = img.convert('L')
    # 二值化
    threshold = 128
    img = img.point(lambda p: p > threshold and 255)
    # 去噪
    img = img.filter(ImageFilter.MedianFilter())
    
    # 保存验证码图片以检查
    img.save('captcha.png')
    
    # 使用自定义字符集
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(img, config=custom_config)
    
    # 打印识别结果
    print(f"识别出的验证码内容: {text}")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")