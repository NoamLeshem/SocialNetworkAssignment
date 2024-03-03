from Post import PostFactory


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.online = True
        self.followers = set()
        self.following = set()
        self.notifications = []
        self.posts = []

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers) or ' '}"

    def disconnect(self):
        self.online = False

    def connect(self):
        self.online = True

    def follow(self, user):
        if not self.online:
            print(f"{self.username} is not connected")
            return
        if user.username in self.following:
            print(f"Already following {user.username}")
            return
        self.following.add(user)
        user.followers.add(self)
        print(f"{self.username} started following {user.username}")

    def unfollow(self, user):
        if not self.online:
            print(f"{self.username} is not connected")
            return
        if user not in self.following:
            # print(f"Not following {user.username}")
            # print(f"{self.username} unfollowed {user.username}")
            return
        self.following.remove(user)
        user.followers.remove(self)
        print(f"{self.username} unfollowed {user.username}")

    def publish_post(self, post_type, *args):
        if not self.online:
            print(f"{self.username} is not connected")
            return
        return PostFactory.create_post(self, post_type,  *args)

    def print_notifications(self):
        if not self.online:
            print(f"{self.username} is not connected")
            return
        print(f"{self.username}'s notifications:")
        print("\n".join(self.notifications))
