import hashlib
import re


class Password:
    def __init__(self, password) -> None:
        self.password = password

    @property
    def is_valid(self):
        pattern = r'^(?=.*[A-Z])(?=.*\d.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$'
        if re.match(pattern, self.password):
            return True
        else:
            return False

    @property
    def hashPassword(self):
        f_hash = hashlib.sha1(self.password.encode("utf-8")).hexdigest()
        return f_hash
