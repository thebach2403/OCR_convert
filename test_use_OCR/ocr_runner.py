import pytesseract

def ocr_image(image, lang="vie+eng"):
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(
        image, lang=lang, config=config
    )
    return text