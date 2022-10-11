import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests


def barcode_detection(image):
    barcode = pyzbar.decode(image)

    # 바코드 인식 불가
    if not len(barcode):
        return None

    for _ in barcode:
        print('Type : ', _.type)
        print('Data : ', _.data, '\n')

    # 다중 인식 시 가장 긴 결과 반환하기 위해 정렬
    barcode.sort(key=lambda obj: len(obj.data), reverse=True)

    return barcode[0]


if __name__ == "__main__":
    img = cv2.imread("barcode1.jpeg")
    print(barcode_detection(img))

    img_url = "http://www.econovill.com/news/photo/201810/348705_226179_4737.JPG"
    img_nparr = np.asarray(bytearray(requests.get(img_url).content), dtype=np.uint8)
    web_img = cv2.imdecode(img_nparr, cv2.IMREAD_COLOR)
    print(barcode_detection(web_img))
