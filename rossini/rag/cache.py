import hashlib
import os
import shutil

class AssetCache:
    def __init__(self, cache_dir: str = "assets/cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _hash_query(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode()).hexdigest()

    def get(self, query: str, extension: str = ".mp4") -> str | None:
        cached_path = os.path.join(self.cache_dir, f"{self._hash_query(query)}{extension}")
        return cached_path if os.path.exists(cached_path) else None

    def save(self, query: str, file_path: str, extension: str = ".mp4") -> str:
        target_path = os.path.join(self.cache_dir, f"{self._hash_query(query)}{extension}")
        shutil.copy(file_path, target_path)
        return target_path