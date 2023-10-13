from django.db import models
from django.conf import settings

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField(null=True)

    def __str__(self):
        return self.title
    

#사용자와 블로그 사이 다대다 관계
#각각의 사용자와 블로그 사이에 찜 기능을 구현
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists', null=True)
    #user : settings.AUTH_USER_MODEL로 설정된 사용자 모델과 관계
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='wishlists')
    #post : Blog와의 관계
    #on_delete = models.CASCADE : 사용자가 삭제되면 해당 찜 목록도 삭제
    #foreignkey : 외래키로 다른 모델과 연결
    #related_name : 사용자 또는 게시글 객체에서 해당 사용자(또는 게시글)에 대한 찜 목록을 역참조할 수 있음(user.wishlists)
