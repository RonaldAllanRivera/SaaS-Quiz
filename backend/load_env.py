import os
from pathlib import Path
import environ

def load_backend_env():
    """
    Loads environment variables from backend/.env if not already loaded.
    Usage: from load_env import load_backend_env; load_backend_env()
    """
    backend_dir = Path(__file__).resolve().parent
    env_path = backend_dir / ".env"
    if env_path.exists():
        environ.Env.read_env(str(env_path))

if __name__ == "__main__":
    load_backend_env()
    print("Loaded environment variables from backend/.env")
