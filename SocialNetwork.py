from collections import defaultdict
from User import User


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SocialNetwork(metaclass=Singleton):
    def __init__(self, name: str):
        self.name = name
        self.users = defaultdict(lambda: User("Unknown", "Unknown"))
        print(f"The social network {name} was created!")

    def __str__(self):
        print(f"{self.name} social network:")
        print(self.user_info())
        return ""

    def user_info(self):
        return "\n".join([str(user) for user in self.users.values()])

    def sign_up(self, username: str, password: str) -> User | None:
        if username in self.users:
            print(f"Username {username} is already taken")
            return None
        if not 4 <= len(password) <= 8:
            print("Password should be between 4 and 8 characters long")
            return None
        user = User(username, password)
        self.users[username] = user
        return user

    def log_out(self, username: str) -> None:
        if username not in self.users:
            print(f"Username {username} does not exist")
            return
        if not self.users[username].online:
            print(f"{username} is already disconnected")
            return
        self.users[username].disconnect()
        print(f"{username} disconnected")

    def log_in(self, username: str, password: str) -> None:
        if username not in self.users:
            print(f"Username {username} does not exist")
            return
        if self.users[username].password != password:
            print("Wrong password")
            return
        if self.users[username].online:
            print(f"{username} is already connected")
            return
        self.users[username].connect()
        print(f"{username} connected")
