from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username="testuser", password="testpass")
        login_res = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login_res)

        self.post_data = {"title": "tadasd title", "content": "TESt Tesat tsasd"}
        url = reverse("post-list")
        response = self.client.post(url, self.post_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, self.post_data.get("title"))

    # def tearDown(self):
    #     pass

    def test_read(self):
        self.assertEqual(Post.objects.count(), 1)
        url = reverse("post-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in self.post_data.items():
            self.assertEqual(response.data[k], v)

    def test_update(self):
        post = Post.objects.first()
        updated_data = {"title": "Updated Title"}
        url = reverse("post-detail", kwargs={"pk": 1})
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated Title")

    def test_delete(self):
        url = reverse("post-detail", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
