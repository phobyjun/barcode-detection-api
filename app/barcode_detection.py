import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests


class NotFoundBarcodeException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def detect(image):
    barcode = pyzbar.decode(image)

    # 바코드 인식 불가
    if len(barcode) == 0:
        raise NotFoundBarcodeException("Barcode Not Found")

    for _ in barcode:
        print('Type : ', _.type)
        print('Data : ', _.data, '\n')

    # 다중 인식 시 가장 긴 결과 반환하기 위해 정렬
    barcode.sort(key=lambda obj: len(obj.data), reverse=True)

    return barcode[0]


def image_from_url(img_url):
    img_nparr = np.asarray(bytearray(requests.get(img_url).content), dtype=np.uint8)
    return cv2.imdecode(img_nparr, cv2.IMREAD_COLOR)


if __name__ == "__main__":
    img = cv2.imread("barcode1.jpeg")
    print(detect(img))

    web_img = image_from_url("https://naeng-bu-test.s3.ap-northeast-2.amazonaws.com/barcode1.jpeg")
    print(detect(web_img))
