import easyocr
import torch
from pathlib import Path


def init_reader():
    """
    Initialize EasyOCR reader with auto GPU detection
    """
    use_gpu = torch.cuda.is_available()

    if use_gpu:
        gpu_name = torch.cuda.get_device_name(0)
        print(f"🚀 Using GPU for OCR: {gpu_name}")
    else:
        print("⚠️ No GPU detected → Using CPU for OCR")

    reader = easyocr.Reader(
        ['vi', 'en'],
        gpu=use_gpu
    )

    return reader


# Initialize reader only once
reader = init_reader()


def image_to_ocr_data(image_path: Path):
    """
    OCR 1 ảnh → structured data
    """
    results = reader.readtext(str(image_path))

    ocr_items = []

    for bbox, text, conf in results:
        ocr_items.append({
            "text": text,
            "confidence": float(conf),
            "bbox": bbox  # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        })

    return {
        "image": image_path.name,
        "items": ocr_items
    }
