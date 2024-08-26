# Generated by Django 5.1 on 2024-08-26 13:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_comment_changed_by_alter_comment_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='changed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_create_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
