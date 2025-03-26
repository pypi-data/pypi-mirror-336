from PIL import Image
from io import BytesIO
from django.conf import settings


def optimize_image(
    image,
    width=getattr(settings, "IMAGE_OPTIMIZER_WIDTH", 800),
    height=getattr(settings, "IMAGE_OPTIMIZER_HEIGHT", None),
    quality=getattr(settings, "IMAGE_OPTIMIZER_QUALITY", 80),
):
    """Resize and optimize an image before saving."""

    with Image.open(image) as img:
        if width and height:
            img = img.resize((width, height), Image.LANCZOS)
        elif width:
            height = int((width / img.width) * img.height)
            img = img.resize((width, height), Image.LANCZOS)
        elif height:
            width = int((height / img.height) * img.width)
            img = img.resize((width, height), Image.LANCZOS)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        output = BytesIO()
        img.save(output, format="WEBP", quality=quality, optimize=True)
        output.seek(0)

        return output
