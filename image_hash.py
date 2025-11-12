# utils/image_hash.py
from PIL import Image
import imagehash

def phash_hex(path: str) -> str:
    """Robust perceptual hash as hex string (256-bit)."""
    with Image.open(path) as img:
        img = img.convert("RGB")  # normalize mode
        return str(imagehash.phash(img, hash_size=16))
