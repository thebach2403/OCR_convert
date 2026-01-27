from pdf_to_image import pdf_to_images
from ocr_runner import image_to_text
from preprocess import preprocess_image
import os

def main():
    pdf_path = r"C:\Users\bachnt8\Projects_Management\OCR_Convert\OCR_convert\input_test.pdf"
    output_dir = r"./test_output"
    preprocess_dir = r"./test_output/preprocess"

    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(preprocess_dir, exist_ok=True)

    # 1. Convert PDF → images
    images = pdf_to_images(pdf_path, output_dir)

    # 2. Preprocess trang đầu tiên (DEBUG trước)
    preprocess_path = os.path.join(preprocess_dir, "page_1_prep.png")
    processed_img = preprocess_image(images[2], preprocess_path)

    # 3. OCR ảnh đã preprocess
    text = image_to_text(processed_img)
    print(text)

if __name__ == "__main__":
    main()
