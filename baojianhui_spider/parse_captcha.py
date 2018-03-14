# -*-coding:utf-8-*-
from PIL import Image
import pytesseract

def captcha_recognition(img_name):
        img = Image.open(img_name)
        width, height = img.size
        box = (2, 2, width - 2, height - 2)
        new_img = img.crop(box)
        new_img = new_img.convert('L')
        gray_img = new_img.point(lambda i: 0 if i < 140 else 255)
        config = '-psm 7'  # 声明只有一行内容
        captcha = pytesseract.image_to_string(gray_img, config=config)
        return captcha