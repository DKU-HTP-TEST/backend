# Generated by Django 4.2.4 on 2023-11-07 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('htp_test', '0005_htp_user_id_alter_htp_created_date_alter_htp_home_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htp',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자아이디'),
        ),
    ]