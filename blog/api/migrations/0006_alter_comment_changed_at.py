# Generated by Django 5.1 on 2024-08-25 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_post_changed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='changed_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
