import cv2
import os

def preprocess_image(image_path, output_path, mode="gray"):
    if not os.path.splitext(output_path)[1]:
        output_path += ".png"

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if mode == "gray":
        processed = gray

    elif mode == "adaptive":
        processed = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10
        )

    else:
        raise ValueError("Unsupported preprocess mode")

    cv2.imwrite(output_path, processed)
    return output_path
