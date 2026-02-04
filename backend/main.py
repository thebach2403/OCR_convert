"""
Main pipeline - Enhanced version
- Convert PDF → Images
- Preprocess all images
- OCR all pages
- Save to Word + JSON
"""

import os
from pathlib import Path
from tqdm import tqdm
from support_lib.PDF_to_images import pdf_to_images
from support_lib.preprocess import preprocess_image
from support_lib.loading import Spinner
from support_lib.ocr_export import save_ocr_word, save_ocr_json
from core.OCR.ocr_engine import image_to_ocr_data
from core.OCR.layout_analyzer import LayoutAnalyzer


def main():
    # ---------- INPUT ----------
    input_pdf = Path(
        input("Enter input PDF file path: ").strip().strip("'").strip('"')
    )

    if not input_pdf.exists():
        raise FileNotFoundError(f"PDF file not found: {input_pdf}")

    # ---------- OUTPUT FOLDERS ----------
    BASE_DIR = Path(__file__).resolve().parent
    OUTPUT_FOLDER = BASE_DIR / "output"

    output_raw_images = OUTPUT_FOLDER / "raw_images"
    output_preprocessed_images = OUTPUT_FOLDER / "preprocessed_images"
    output_json_dir = OUTPUT_FOLDER / "ocr_json"
    output_word_dir = OUTPUT_FOLDER / "ocr_word"

    for folder in [
        OUTPUT_FOLDER,
        output_raw_images,
        output_preprocessed_images,
        output_json_dir,
        output_word_dir,
    ]:
        folder.mkdir(parents=True, exist_ok=True)

    print("Input PDF:", input_pdf)
    print("Output folder:", OUTPUT_FOLDER)

    # ---------- PDF → IMAGES ----------
    spinner = Spinner("Converting PDF to images")
    spinner.start()
    pdf_to_images(
        pdf_path=input_pdf,
        output_dir=output_raw_images,
        dpi=300
    )
    spinner.stop()

    # ---------- PREPROCESS ----------
    spinner = Spinner("Preprocessing images")
    spinner.start()
    for image_path in output_raw_images.glob("*.png"):
        preprocess_image(
            image_path=image_path,
            output_dir=output_preprocessed_images
        )
    spinner.stop()

    # ---------- OCR + EXPORT ----------
    images = list(output_preprocessed_images.glob("*.png"))
    print(f"Found {len(images)} images for OCR")    

    for image_path in tqdm(
        images,
        desc="Running OCR",
        unit="page",
        ncols=100
    ):
        ocr_data = image_to_ocr_data(image_path=image_path)

        save_ocr_json(
            ocr_data,
            output_json_dir / f"{image_path.stem}.json"
        )

        save_ocr_word(
            ocr_data,
            output_word_dir / f"{image_path.stem}.docx"
        )

    print("✅ OCR pipeline completed successfully!")


if __name__ == "__main__":
    main()
