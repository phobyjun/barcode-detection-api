from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.barcode_detection import image_from_url, detect
from app.barcode_parser import parse, NotGS1BarException

app = FastAPI()


@app.get("/health-check", status_code=200)
async def health_check():
    return {"status": "success"}


default_s3_route = ""


@app.get("/barcode/{image_url}")
async def barcode_detection_api(image_url: str):
    image = image_from_url(default_s3_route + image_url)
    barcode = detect(image)
    try:
        expiration_date = parse(barcode)
        return {
            "image_url": image_url,
            "expiration_date": expiration_date
        }
    except NotGS1BarException as error:
        raise HTTPException(status_code=404, detail=error.__str__())


handler = Mangum(app)
