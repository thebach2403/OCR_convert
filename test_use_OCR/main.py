from pdf_to_image import pdf_to_images
from preprocess import preprocess_image
from ocr_runner import ocr_image
import os

def main():
    pdf_path = r"C:\Users\bachnt8\Projects_Management\OCR_Convert\OCR_convert\input_test.pdf"
    img_dir = "./images"
    txt_dir = "./text"

    os.makedirs(txt_dir, exist_ok=True)

    images = pdf_to_images(pdf_path, img_dir)

    all_text = []

    for img_path in images:
        img = preprocess_image(img_path)
        text = ocr_image(img)

        txt_path = os.path.join(
            txt_dir,
            os.path.basename(img_path).replace(".png", ".txt")
        )
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        all_text.append(text)

    with open("output/full_text.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))


if __name__ == "__main__":
    main()