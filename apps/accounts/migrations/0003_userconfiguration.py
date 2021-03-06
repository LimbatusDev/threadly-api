# Generated by Django 3.2.8 on 2021-10-29 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211027_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_sends', models.IntegerField(default=0)),
                ('counter', models.CharField(choices=[('SLASH', 'SLASH'), ('GUION', 'GUION')], default='SLASH', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
