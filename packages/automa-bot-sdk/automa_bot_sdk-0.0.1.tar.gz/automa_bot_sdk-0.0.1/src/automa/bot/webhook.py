import hashlib
import hmac
import json


def verify_webhook(secret: str, signature: str, payload: object | str) -> bool:
    if (
        not secret
        or not isinstance(secret, str)
        or not signature
        or not isinstance(signature, str)
    ):
        return False

    generated_signature = generate_webhook_signature(secret, payload)

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(generated_signature, signature)


def generate_webhook_signature(secret: str, payload: object | str) -> str:
    if isinstance(payload, str):
        payload_str = payload
    else:
        payload_str = json.dumps(payload, separators=(",", ":"))

    return hmac.new(
        secret.encode("utf-8"), payload_str.encode("utf-8"), hashlib.sha256
    ).hexdigest()
