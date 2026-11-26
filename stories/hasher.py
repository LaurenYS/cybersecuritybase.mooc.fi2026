from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare

class PlaintextPasswordHasher(BasePasswordHasher):
    algorithm = "plaintext"

    def salt(self) -> str:
        return ""

    def encode(self, password, salt=None):
        return f"{self.algorithm}$${password}"

    def verify(self, password, encoded):
        _, _, stored = encoded.split("$", 2)
        return constant_time_compare(password, stored)

    def safe_summary(self, encoded):
        _, _, stored = encoded.split("$", 2)
        return {"algorithm": self.algorithm, "password": stored}

    def must_update(self, encoded):
        return False

    def harden_runtime(self, password, encoded):
        pass
