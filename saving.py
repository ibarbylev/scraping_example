import os
from base64 import b64encode
from hashlib import sha256

from settings import OUT_DIR


B64_ALTCHARS = b'+-'


def get_save_path(filename: str) -> str:
    h = sha256()
    h.update(filename.encode())
    hashed_name = b64encode(h.digest(), altchars=B64_ALTCHARS).decode()
    return os.path.join(OUT_DIR, hashed_name + '.json')
