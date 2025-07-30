import hashlib
import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings

def download_and_save_image(image_url, keyword, page_order):
    """
    Downloads an image from the given URL and saves it to the media folder with deduplication.
    Returns the relative path to the saved image.
    """
    if not image_url:
        print(f"[DEBUG] No image_url provided to download_and_save_image.")
        return None
    try:
        print(f"[DEBUG] Attempting to download image: {image_url}")
        url_hash = hashlib.md5(image_url.encode('utf-8')).hexdigest()
        ext = image_url.split('.')[-1].split('?')[0]
        filename = f"{keyword}_{page_order}_{url_hash[:8]}.{ext}"
        media_root = getattr(settings, 'MEDIA_ROOT', 'media')
        save_path = os.path.join(media_root, 'book_images', filename)
        print(f"[DEBUG] Image save path: {save_path}")
        if not os.path.exists(save_path):
            resp = requests.get(image_url)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(resp.content)
                print(f"[DEBUG] Image downloaded and saved: {save_path}")
            else:
                print(f"[DEBUG] Failed to download image, status code: {resp.status_code}")
        else:
            print(f"[DEBUG] Image already exists, skipping download: {save_path}")
        rel_path = os.path.join('book_images', filename)
        return rel_path
    except Exception as e:
        print(f"[DEBUG] Exception in download_and_save_image: {e}")
        return None
