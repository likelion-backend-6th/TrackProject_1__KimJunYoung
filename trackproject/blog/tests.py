from rest_framework.test import APITestCase
from rest_framework import status
from django.http import HttpResponse

from .models import User


class PostTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = User.objects.create_superuser("superuser")
        cls.authorized_user1 = User.objects.create_user("authorized1")
        cls.authorized_user2 = User.objects.create_user("authorized2")
        cls.unauthorized_user = User.objects.create_user("unauthorized")
        cls.post_data = {
            "title": "test title",
            "body": "test body",
            "owner": cls.authorized_user1,
        }

    # 전체 사용자 목록에서 자신을 제외한 목록이 잘 나오는지 테스트
    def test_user_list_without_self(self):
        self.client.force_login(self.authorized_user1)
        res: HttpResponse = self.client.get("/users/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.authorized_user1, res.data)

    # 본인의 게시물만 수정, 삭제가 가능한지 테스트
    def test_permission_post_update_delete_self(self):
        self.client.force_login(self.authorized_user1)
        res: HttpResponse = self.client.post("/blog/post/", self.post_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        post_id = res.data["id"]
        self.post_data["title"] = "update title"

        # 다른 사용자일때 수정
        self.client.force_login(self.authorized_user2)
        res: HttpResponse = self.client.put(f"/blog/post/{post_id}/", self.post_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # 본인일때 수정
        self.client.force_login(self.authorized_user1)
        res: HttpResponse = self.client.put(f"/blog/post/{post_id}/", self.post_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "update title")

        # 다른 사용자일때 삭제
        self.client.force_login(self.authorized_user2)
        res: HttpResponse = self.client.delete(f"/blog/post/{post_id}/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # 본인일때 삭제
        self.client.force_login(self.authorized_user1)
        res: HttpResponse = self.client.delete(f"/blog/post/{post_id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # follow / unfollow 기능이 잘 작동하는지 테스트
    def test_follow_unfollow(self):
        self.client.force_login(self.authorized_user1)
        follow_data = {
            "following": self.authorized_user2.id,
        }
        res: HttpResponse = self.client.post("/follow/", follow_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res: HttpResponse = self.client.delete(
            f"/follow/unfollow/{self.authorized_user2}/"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # follow한 사람들이 올린 게시물을 잘 확인할 수 있는지 테스트
    def test_follow_post_list(self):
        self.client.force_login(self.authorized_user2)
        post_data = {
            "title": "test title_uesr2",
            "body": "test body_user2",
        }
        self.client.post("/blog/post/", post_data)

        self.client.force_login(self.authorized_user1)
        follow_data = {
            "following": self.authorized_user2.id,
        }
        post_data = {
            "title": "test title",
            "body": "test body111",
        }
        self.client.post("/follow/", follow_data)
        self.client.post("/blog/post/", post_data)

        res: HttpResponse = self.client.get("/blog/post/following_post/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["owner"], self.authorized_user2.id)
