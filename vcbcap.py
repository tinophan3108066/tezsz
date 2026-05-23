import base64
import io
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from vietcombank_captcha import VietcombankCaptcha

# --- CẤU HÌNH FASTAPI ---
app = FastAPI(
    title="Vietcombank Captcha OCR",
    description="API captcha VCB from base64",
    version="1.0.0"
)

# --- KHỞI TẠO MODEL OCR 1 LẦN ---
ocr_model = VietcombankCaptcha()

# --- ĐỊNH NGHĨA BODY REQUEST ---
class CaptchaRequest(BaseModel):
    base64: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/api/captcha/vcb")
def solve_captcha(req: CaptchaRequest):
    b64_str = req.base64
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]

    try:
        img_bytes = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Base64 khong hop le")

    text = ocr_model.predict(img)
    return {
        "captcha": text,
        "status": "success"
    }
