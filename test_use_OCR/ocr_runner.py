import easyocr

# Khởi tạo OCR reader (chỉ 1 lần)
reader = easyocr.Reader(['en'], gpu=False)

def image_to_text(image_path):
    """
    OCR 1 ảnh → text thô
    """
    texts = []
    results = reader.readtext(image_path)

    # results: [(bbox, text, confidence), ...]
    texts = [text for (_, text, _) in results]

    return "\n".join(texts)