from celery import shared_task
from .models import Post
from django.contrib.auth.models import User
import datetime

@shared_task
def generate_blog_post():
    # Define the AI generation process and parameters here
    user = User.objects.first()  # Example: assign the first user as the author
    title = f"Daily Blog Post - {datetime.datetime.now().strftime('%Y-%m-%d')}"
    content = "This is an AI-generated blog post."  # Replace with AI-generated content

    Post.objects.create(title=title, content=content, author=user, local_body='Generated body', local_name='Generated place')
