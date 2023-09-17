# Generated by Django 4.2.5 on 2023-09-15 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=128, unique=True, verbose_name='아이디')),
                ('password', models.CharField(max_length=225, verbose_name='비밀번호')),
                ('username', models.CharField(max_length=128, verbose_name='이름')),
                ('useremail', models.EmailField(blank=True, max_length=128, null=True, verbose_name='이메일')),
                ('status', models.CharField(choices=[('일반', '일반'), ('탈퇴', '탈퇴'), ('휴면', '휴면')], default='일반', max_length=16)),
            ],
            options={
                'verbose_name': '회원',
                'verbose_name_plural': '회원',
            },
        ),
    ]