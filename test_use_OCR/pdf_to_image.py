import pypdfium2 as pdfium
import os

def pdf_to_images(pdf_path, output_dir, dpi=300):
    os.makedirs(output_dir, exist_ok=True)

    pdf = pdfium.PdfDocument(pdf_path)
    page_indices = list(range(len(pdf)))

    renderer = pdf.render_to(
        pdfium.BitmapConv.pil_image,
        page_indices=page_indices,
        scale=dpi / 72  # PDF default = 72 DPI
    )

    image_paths = []
    for i, image in zip(page_indices, renderer):
        path = os.path.join(output_dir, f"page_{i+1}.png")
        image.save(path)
        image_paths.append(path)

    return image_paths
