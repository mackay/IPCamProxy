import random
import string
from passlib.hash import sha256_crypt


class UserRegistryEntry(object):
    def __init__(self, username, salt, hashed_password):
        self.username = username
        self.salt = salt
        self.hash = hashed_password


class UserRegistry(object):
    def __init__(self):
        self.users = [ ]

    def add(self, username, password, salt=None):
        user = self.get_user(username)

        if salt is None:
            salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        hash = sha256_crypt.encrypt(salt + password)

        if user is None:
            entry = UserRegistryEntry(username, salt, hash)
            self.users.append(entry)
        else:
            user.salt = salt
            user.hash = hash

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user

        return None


USER_REGISTRY = UserRegistry()
USER_REGISTRY.add("cam", "foo")


def check_pass(username, password):
    user = USER_REGISTRY.get_user(username)

    if user:
        return sha256_crypt.verify(user.salt + password, user.hash)

    return False
