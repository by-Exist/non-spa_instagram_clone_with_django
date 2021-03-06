# Generated by Django 3.1.2 on 2020-10-31 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instagram', '0002_auto_20201031_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at_dt', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('updated_at_dt', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('message', models.TextField(verbose_name='댓글')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='포스트')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instagram.post', verbose_name='작성자')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
