import os
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO

DEFAULT_WIDTH = getattr(settings, "IMAGE_OPTIMIZER_WIDTH", 800)
DEFAULT_HEIGHT = getattr(settings, "IMAGE_OPTIMIZER_HEIGHT", None)
DEFAULT_QUALITY = getattr(settings, "IMAGE_OPTIMIZER_QUALITY", 80)


class ImageOptimizationMiddleware:
    """Middleware to optimize uploaded images before they are saved."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["POST", "PUT", "PATCH"] and request.FILES:
            width = request.META.get("IMAGE_OPTIMIZER_WIDTH", DEFAULT_WIDTH)
            height = request.META.get("IMAGE_OPTIMIZER_HEIGHT", DEFAULT_HEIGHT)
            quality = request.META.get("IMAGE_OPTIMIZER_QUALITY", DEFAULT_QUALITY)

            for field_name, file in request.FILES.items():
                if file.content_type.startswith("image/"):  # Process only images
                    optimized_image = self.resize_and_optimize(
                        file, width, height, quality
                    )
                    optimized_file = InMemoryUploadedFile(
                        optimized_image,  # File content
                        field_name,  # Field name
                        os.path.splitext(file.name)[0] + ".webp",  # New filename
                        "image/webp",  # MIME type
                        optimized_image.tell(),  # File size
                        None,  # Encoding
                    )
                    request.FILES[field_name] = optimized_file  # Replace original file

        return self.get_response(request)

    def resize_and_optimize(self, image, width=None, height=None, quality=80):
        """Resize and optimize an image before saving."""
        with Image.open(image) as img:
            # Resize while maintaining aspect ratio if only one dimension is given
            if width and height:
                img = img.resize((width, height), Image.LANCZOS)
            elif width:
                height = int((width / img.width) * img.height)
                img = img.resize((width, height), Image.LANCZOS)
            elif height:
                width = int((height / img.height) * img.width)
                img = img.resize((width, height), Image.LANCZOS)

            # Convert to RGB (WebP does not support "P" mode)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Save to memory in WebP format
            output = BytesIO()
            img.save(output, format="WEBP", quality=quality, optimize=True)
            output.seek(0)

            return output
