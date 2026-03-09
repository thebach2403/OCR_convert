import fitz  # PyMuPDF
import os
from pathlib import Path
import cv2

def pdf_to_images(pdf_path, output_dir, dpi=300):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)# Mở file PDF, doc là một document object, chứa toàn bộ các trang PDF
    image_paths = [] # Danh sách lưu đường dẫn các ảnh đã render
    # PDF mặc định render ở 72 DPI
    # Tính hệ số zoom để đạt DPI mong muốn
    zoom = dpi / 72
    # Tạo ma trận scale cho việc render (phóng to ảnh)
    # zoom x, zoom y
    mat = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat)# Render trang PDF thành ảnh raster (pixmap), matrix=mat để tăng độ phân giải ảnh
        img_path = os.path.join(output_dir, f"page_{i+1}.png")
        pix.save(img_path)
        image_paths.append(img_path)

    return image_paths



def preprocess_image(image_path: Path, output_dir: Path):
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