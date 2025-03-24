import base64
import hashlib
from functools import wraps
import os

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

def generate_code_verifier():
    """Generate a code verifier for PKCE."""
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')


def generate_code_challenge(verifier):
    """Generate a code challenge from a code verifier using SHA256."""
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')

def create_parameters(mapping):
    params = {}
    for item in mapping:
        if item[0]:
            if isinstance(item[0], str):
                params[item[1]] = item[0]
            elif isinstance(item[0], dict):
                for k, v in item[0].items():
                    params[f'{item[1]}.{k}'] = v
    return params


class ApiProgress:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with Progress(SpinnerColumn(), BarColumn(),
                          TextColumn("[progress.description]{task.description}")) as prog:
                prog.add_task(self.message, total=None)  # Total unknown initially
                return fn(*args, **kwargs)
        return wrapper

progress = ApiProgress
