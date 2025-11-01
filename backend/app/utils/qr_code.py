import qrcode
from io import BytesIO
import base64
from typing import Optional
import json
import hashlib


def generate_qr_code_data(product_id: int, product_name: str, sku: str) -> str:
    """Generate QR code data string for a product"""
    data = {
        "product_id": product_id,
        "product_name": product_name,
        "sku": sku,
        "timestamp": str(product_id)  # Simple unique identifier
    }
    qr_string = json.dumps(data)
    # Create a hash for the QR code
    qr_hash = hashlib.sha256(qr_string.encode()).hexdigest()[:16]
    return f"PROD-{product_id}-{qr_hash}"


def create_qr_code_image(data: str) -> str:
    """Generate QR code image and return as base64 string"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def decode_qr_code(qr_data: str) -> Optional[dict]:
    """Decode QR code data to extract product information"""
    try:
        if qr_data.startswith("PROD-"):
            parts = qr_data.split("-")
            if len(parts) >= 3:
                return {
                    "product_id": int(parts[1]),
                    "hash": parts[2]
                }
        return None
    except Exception:
        return None
