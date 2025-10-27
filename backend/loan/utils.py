import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def generate_credit_summary(dsr, parsed_data):
    if not dsr:
        return "Insufficient data to evaluate creditworthiness."
    if dsr < 30:
        return f"Excellent creditworthiness. Low DSR of {dsr}%."
    elif dsr < 40:
        return f"Good creditworthiness. Moderate DSR of {dsr}%."
    else:
        return f"High DSR of {dsr}%, potential financial risk."


def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text


def calculate_dsr(income, total_debt):
    if not income or income == 0:
        return None
    return round((total_debt / income) * 100, 2)


def parse_salary_info(text):
    salary = None
    match = re.search(r"(\d{4,6})[\s]*[Tk$]", text)
    if match:
        salary = int(match.group(1))
    return {"monthly_salary": salary}

