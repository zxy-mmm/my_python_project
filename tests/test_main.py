# from bs4 import BeautifulSoup
# import json

# url = 'https://fj.tzxm.gov.cn/eap/credit.showProjectInfo?vcodeh2=J6F7'
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Cookie': 'Hm_lvt_11c3f77be047ea95e3773e8f9eeb11e9=1737362667; HMACCOUNT=754EA451029538F0; JSESSIONID=0A27E0C57F12D756D4EC70268BAE6910; Hm_lpvt_11c3f77be047ea95e3773e8f9eeb11e9=1737440650',
#     'Host': 'fj.tzxm.gov.cn',
#     'Origin': 'https://fj.tzxm.gov.cn',
#     'Pragma': 'no-cache',
#     'Referer': 'https://fj.tzxm.gov.cn/eap/credit.showProjectInfo',
#     'Sec-CH-UA': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'Sec-CH-UA-Mobile': '?0',
#     'Sec-CH-UA-Platform': '"macOS"',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
# }
# response = requests.post(url, headers=headers)

# # 解析HTML内容
# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)

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