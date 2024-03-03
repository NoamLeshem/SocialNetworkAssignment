from abc import ABC
from collections import defaultdict
import matplotlib.pyplot as plt
from PIL import Image


class PostFactory:
    @staticmethod
    def create_post(user, post_type, *args):
        if post_type == "Text":
            return TextPost(user, *args)
        if post_type == "Image":
            return ImagePost(user, *args)
        if post_type == "Sale":
            return SalePost(user, *args)


class Post(ABC):
    def __init__(self, post_type):
        self.post_type = post_type
        self.likes = []
        self.comments = defaultdict(list)
        self.creator = None

    def __str__(self):
        pass

    def like(self, user):
        if not user.online:
            print(f"{user.username} is not connected")
            return
        if user in self.likes:
            print(f"{user.username} already liked this post")
            return
        self.likes.append(user)
        if user != self.creator:
            print(f"notification to {self.creator.username}: {user.username} liked your post")
            self.creator.notifications.append(f"{user.username} liked your post")

    def comment(self, user, text):
        if not user.online:
            print(f"{user.username} is not connected")
            return
        self.comments[user].append(text)
        if user != self.creator:
            print(f"notification to {self.creator.username}: {user.username} commented on your post: {text}")
            self.creator.notifications.append(f"{user.username} commented on your post")


class TextPost(Post):
    def __init__(self, creator, text):
        super().__init__("Text")
        self.text = text
        self.creator = creator
        creator.posts.append(self)
        for follower in creator.followers:
            follower.notifications.append(f"{self.creator.username} has a new post")
        print(self)

    def __str__(self):
        return f"{self.creator.username} published a post:\n\"{self.text}\"\n"


class ImagePost(Post):
    def __init__(self, creator, path):
        super().__init__("Image")
        self.image_name = path
        self.creator = creator
        creator.posts.append(self)
        for follower in creator.followers:
            follower.notifications.append(self.__str__())
        print(self)

    def __str__(self):
        return f"{self.creator.username} posted a picture\n"

    def display(self):
        print("Shows picture")

        # img_matplotlib = plt.imread(self.image_path)
        # plt.imshow(img_matplotlib)
        # plt.axis('off')
        # plt.show()
        #
        # # Using Pillow to display the image (optional)
        # img_pillow = Image.open(self.image_path)
        # img_pillow.show()


class SalePost(Post):
    def __init__(self, creator, name, price, location):
        super().__init__("Sale")
        self.name = name
        self.price = price
        self.creator = creator
        self.location = location
        self.in_stock = True
        creator.posts.append(self)
        for follower in creator.followers:
            follower.notifications.append(f"{self.creator.username} has a new post")
        print(self)

    def __str__(self):
        return f"{self.creator.username} posted a product for sale:\n{'For sale!' if self.in_stock else 'Sold!'} {self.name}, price: {self.price}, pickup from: {self.location}\n"

    def discount(self, percentage, password):
        if password != self.creator.password:
            print("Wrong password")
            return
        if not self.in_stock:
            print("Product is sold out!")
            return
        self.price *= (100 - percentage) / 100
        print(f"Discount on {self.creator.username} product! the new price is: {self.price}")

    def sold(self, password):
        if password != self.creator.password:
            print("Wrong password")
            return
        self.in_stock = False
        print(f"{self.creator.username}'s product is sold")
