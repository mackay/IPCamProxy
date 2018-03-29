
class UserRegistryEntry(object):
    def __init__(self, username, salt, hashed_password):
        self.username = username
        self.salt = salt
        self.hash = hashed_password


class UserRegistry(object):
    def __init__(self):
        self.users = [ ]

    def add(self, username, salt, hash):
        user = self.get_user(username)

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
USER_REGISTRY.add("cam", "5367105448", "$5$rounds=110000$1ffk0eeSsvrU4kFL$xlS1NJFiD9wARrXcw.OBfnaDJdHeA.O/ripSlOZhjg1" )
