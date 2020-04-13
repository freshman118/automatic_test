# import cv2
# from pytesseract import pytesseract
#
# img = cv2.cvtColor(cv2.imread(r'../../static/image/example_02.png'), cv2.COLOR_BGR2RGB)
# img2 = cv2.cvtColor(cv2.imread(r'../../static/image/Screenshot (11).png'), cv2.COLOR_BGR2RGB)
#
# def ocr_char(image, **kwargs):
#     tesseract_cmd = kwargs.get('tesseract_cmd', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
#     config = kwargs.get('config', r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --oem 3 --psm 6')
#
#     pil_image = cv.get_pil_image(image)
#     pytesseract.tesseract_cmd = tesseract_cmd
#     str = pytesseract.image_to_string(pil_image, config=config)
#     print('str:', str)
#     return str