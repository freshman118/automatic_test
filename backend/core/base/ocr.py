import cv2
import export as export
from pytesseract import pytesseract

img = cv2.cvtColor(cv2.imread(r'../../static/image/example_02.png'), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(r'../../static/image/Screenshot (11).png'), cv2.COLOR_BGR2RGB)
TESSDATA_PREFIX = r'E:\Git Repository\tesseract\tessdata'

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# custom_oem_psm_config = r'--oem 3 --psm 6'
config = r'--tessdata-dir "E:\Git Repository\tesseract\tessdata"'
print(pytesseract.image_to_string(img, config=config))
print('-' * 50)
# print(pytesseract.image_to_string(img2, config=custom_oem_psm_config))
