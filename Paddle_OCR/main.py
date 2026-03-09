# main.py

import json
from pathlib import Path
from paddleOCR_engine import OCREngine
from utils.support_libs import pdf_to_images, preprocess_image

def debug_page(document_pages, page_index: int):
    """
    page_index: x (x=0 là trang 1)
    """

    if page_index < 0 or page_index >= len(document_pages):
        print("Invalid page index!")
        return

    page_data = document_pages[page_index]

    print(f"\n===== DEBUG PAGE {page_index} (PDF page {page_data['page_number']}) =====")

    if not page_data["items"]:
        print("No text detected.")
    else:
        for item in page_data["items"]:
            print(item["text"])

    print("============================================")


def main():
    # ===== 1. Nhập file PDF =====
    pdf_path = Path(input("Enter PDF file path: ").strip())

    if not pdf_path.exists():
        print("File does not exist!")
        return

    if pdf_path.suffix.lower() != ".pdf":
        print("Input must be a PDF file!")
        return

    # ===== 2. Tạo output folder cùng cấp =====
    output_folder = pdf_path.parent / f"{pdf_path.stem}_output"
    output_folder.mkdir(exist_ok=True)

    print(f"\nOutput folder: {output_folder}")

    # ===== 3. Khởi tạo OCR engine =====
    engine = OCREngine()

    # Folder tạm
    image_folder = output_folder / "images"
    processed_folder = output_folder / "processed"

    # ===== 4. Convert PDF → images =====
    print("\nConverting PDF to images...")
    image_paths = pdf_to_images(pdf_path, image_folder)

    document_pages = []

    # ===== 5. Xử lý từng trang =====
    for idx, img_path in enumerate(image_paths, start=1):
        print(f"Processing page {idx}")

        # Preprocess
        processed_img = preprocess_image(Path(img_path), processed_folder)

        # OCR
        ocr_items = engine.read_image(processed_img)

        document_pages.append({
            "page_number": idx,
            "image": Path(img_path).name,
            "items": ocr_items
        })

    # ===== 6. Lưu JSON =====
    output_json_path = output_folder / f"{pdf_path.stem}.json"

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "document": pdf_path.name,
            "pages": document_pages
        }, f, indent=4, ensure_ascii=False)

    print(f"\nSaved result to: {output_json_path}")

    # ===== Debug 1 trang =====
    page_to_debug = int(input("\nEnter page index to debug (x=0 là trang 1): "))
    debug_page(document_pages, page_to_debug)

    print("\nDone!")


if __name__ == "__main__":
    main()