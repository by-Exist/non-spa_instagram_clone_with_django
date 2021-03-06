import re
from django.conf import settings
from django.db import models
from django.urls import reverse


class BaseDateTimeModel(models.Model):

    created_at_dt = models.DateTimeField("작성일", auto_now_add=True)
    updated_at_dt = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        abstract = True


class Post(BaseDateTimeModel):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_post_set'
    )
    photo = models.ImageField(
        "사진", upload_to="instagram/post/%Y/%m/%d")  # TODO: 이미지 가공 후 저장하기
    caption = models.CharField("설명", max_length=500)
    tag_set = models.ManyToManyField("Tag", blank=True)
    location = models.CharField("지역", max_length=50, blank=True)

    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='like_post_set'
    )

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail", kwargs={"pk": self.pk})

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ['-id']


class Comment(BaseDateTimeModel):

    post = models.ForeignKey(
        "instagram.Post", verbose_name="작성자", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name="포스트", on_delete=models.CASCADE)
    message = models.TextField("댓글")

    class Meta:
        ordering = ["-id"]


class Tag(models.Model):

    name = models.CharField("태그", max_length=50, unique=True)

    def __str__(self):
        return self.name
