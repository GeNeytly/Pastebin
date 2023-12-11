from django.utils import timezone


class FakeRequest:
    def __init__(self, method):
        self.__method = method

    def get_method(self):
        return self.__method

    def set_method(self, method):
        self.__method = method

    method = property(get_method, set_method)


def create_user_data(type):
    """Retrieves the data type, and based on it
    returns the data necessary to create a user."""
    user_data = {
        'username': f'Username{type}',
        'password': f'password{type}'
    }
    return user_data


def create_post_data(type, author):
    """Retrieves the data type, and based on it
    returns the data necessary to create a post."""
    post_data = {
        'title': f'Title of {type} post',
        'text': f'Text of {type} post',
        'created_at': timezone.now(),
        'author': author
    }
    return post_data


def create_report_data(post, expire_after):
    report_data = {
        'post': post,
        'expire_time': timezone.now() + expire_after
    }
    return report_data


def create_tag_data(type):
    """Retrieves the data type, and based on it
    returns the data necessary to create a tag."""
    tag_data = {
        'name': f'Name of {type} tag',
        'description': f'Description of {type} tag'
    }
    return tag_data