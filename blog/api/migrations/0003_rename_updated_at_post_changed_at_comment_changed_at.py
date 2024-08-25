# Generated by Django 5.1 on 2024-08-25 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_comment_changed_by_comment_created_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='updated_at',
            new_name='changed_at',
        ),
        migrations.AddField(
            model_name='comment',
            name='changed_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
