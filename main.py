from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.barcode_detection import image_from_url, detect, NotFoundBarcodeException
from app.barcode_parser import parse, NotGS1BarException

app = FastAPI()


@app.get("/health-check", status_code=200)
async def health_check():
    return {"status": "success"}


default_s3_route = "https://naeng-bu-test.s3.ap-northeast-2.amazonaws.com/"


@app.get("/barcode/{image_url}")
async def barcode_detection_api(image_url: str):
    try:
        image = image_from_url(default_s3_route + image_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())

    try:
        barcode = detect(image)
    except NotFoundBarcodeException as error:
        raise HTTPException(status_code=404, detail=error.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())

    try:
        expiration_date = parse(barcode)
        return {
            "image_url": image_url,
            "expiration_date": expiration_date
        }
    except NotGS1BarException as error:
        raise HTTPException(status_code=404, detail=error.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


handler = Mangum(app)
