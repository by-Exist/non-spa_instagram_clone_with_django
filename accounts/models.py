from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.validators import RegexValidator
from django.db import models

# 인스타그램 프로필 수정
# 프로필 사진, 이름, id, 웹사이트, 소개, 이메일, 전화번호, 성별

# Django에서 사용할 User Model을 커스텀하기 위한 모델.
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example 참고
class User(AbstractUser):

    # CharField와 TextField는 null을 설정할 필요가 없다!

    GENDER = (
        ("M", "남성"),
        ("W", "여성"),
    )

    avatar = models.ImageField("아바타", upload_to="accounts/profile/%Y/%m/%d", blank=True, help_text="2mb 이하의 jpg 이미지만 사용 가능합니다.")
    name = models.CharField("실명", max_length=50, blank=True)
    nickname = models.CharField("닉네임", max_length=50)
    website_url = models.CharField("개인 사이트 주소", max_length=254, blank=True)
    bio = models.TextField("소개", blank=True)
    gender = models.CharField("성별", max_length=50, choices=GENDER, blank=True)
    phone_number = models.CharField("휴대폰 번호", validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}")], max_length=13)