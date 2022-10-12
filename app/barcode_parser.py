from datetime import datetime

import cv2

from barcode_detection import detect


class NotGS1BarException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def parse(_barcode) -> datetime:
    if _barcode.type != "I25":
        raise NotGS1BarException("Not a GS1 Barcode Type")

    barcode_data = _barcode.data.decode('utf-8')

    exp_data = barcode_data[13:]
    exp_type, exp_f, exp_s = tuple(map(int, (exp_data[0], exp_data[1:3], exp_data[3:])))

    datetime_now = datetime.now()
    year_now = datetime_now.year
    month_now = datetime_now.month

    if exp_type == 2:
        exp_month = exp_f
        exp_day = exp_s
        return datetime(year_now, exp_month, exp_day)
    elif exp_type == 4:
        exp_day = exp_f
        exp_hour = exp_s
        return datetime(year_now, month_now, exp_day, exp_hour)

    return datetime.now()


if __name__ == "__main__":
    img = cv2.imread("barcode1.jpeg")
    barcode = detect(img)
    try:
        print(parse(barcode))
    except NotGS1BarException as e:
        print(e)
