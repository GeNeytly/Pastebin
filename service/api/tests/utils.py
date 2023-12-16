from datetime import timedelta

from django.utils import timezone


def create_user_data(type):
    """Retrieves the data type, and based on it
    returns the data necessary to create a user."""
    user_data = {
        'email': f'user{type}@email.com',
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


def create_report_data(post):
    """Retrieves the data type, and based on it returns
    the data necessary to create a report."""
    report_data = {
        'post': post,
        'expire_time': timezone.now() + timedelta(days=1)
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
