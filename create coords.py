import cv2
import pytesseract
import numpy as np

# PDF ise önce PNG’ye çevir
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# -----------------------------
# 1. PDF veya PNG okuma
# -----------------------------
input_file = "2d_kat_plani.png"  # veya PDF: "2d kat plani.pdf"
images = []

if input_file.lower().endswith(".pdf"):
    # PDF -> image
    pil_images = convert_from_path(input_file)
    images = [cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR) for im in pil_images]
else:
    img = cv2.imread(input_file)
    images = [img]

# -----------------------------
# 2. OCR ve oda koordinatları
# -----------------------------
room_coords = {}

for img in images:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # threshold ile daha net
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # konturları bul
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        roi = gray[y:y+h, x:x+w]

        # OCR
        text = pytesseract.image_to_string(roi, config='--psm 6 digits')
        text = text.strip()
        if text.isdigit():  # oda numarası ise
            room_num = int(text)
            # merkez koordinatı
            cx = x + w//2
            cy = y + h//2
            room_coords[room_num] = (cx, cy)

# -----------------------------
# 3. Sonuç
# -----------------------------
print("Oda koordinatları:", room_coords)
