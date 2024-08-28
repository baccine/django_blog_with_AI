from django.test import TestCase
from .models import Post

class PostModelTests(TestCase):
    def test_create_post(self):
        post = Post.objects.create(title="Test Post", content="This is a test.")
        self.assertEqual(post.title, "Test Post")
