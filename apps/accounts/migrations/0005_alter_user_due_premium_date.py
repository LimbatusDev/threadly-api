# Generated by Django 3.2.8 on 2021-10-30 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_due_premium_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='due_premium_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
