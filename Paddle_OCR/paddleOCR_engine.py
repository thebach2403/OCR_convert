# ocr_engine.py

from paddleocr import PaddleOCR
from pathlib import Path


class OCREngine:
    def __init__(self):
        # Hỗ trợ tiếng Anh + tiếng Việt
        self.reader = PaddleOCR(
            use_angle_cls=True,
            lang="ch",  # tốt cho EN + VI
            show_log=False
        )

    def read_image(self, image_path: Path):
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        result = self.reader.ocr(str(image_path), cls=True)

        # Không có kết quả hoặc trang không detect được gì
        if not result or result[0] is None:
            return []

        items = []

        for line in result[0]:
            if line is None:
                continue

            bbox = line[0]
            text = line[1][0]
            conf = float(line[1][1])

            items.append({
                "text": text,
                "confidence": conf,
                "bbox": bbox
            })

        return items