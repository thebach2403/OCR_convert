from pathlib import Path
import cv2


def preprocess_image(image_path: Path, output_dir: Path):
    """
    Preprocess ONE image and save to output_dir
    """

    image_path = Path(image_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Read image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    # === Example preprocess ===
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Build output path (KEEP filename)
    output_path = output_dir / image_path.name

    cv2.imwrite(str(output_path), gray)

    return output_path
