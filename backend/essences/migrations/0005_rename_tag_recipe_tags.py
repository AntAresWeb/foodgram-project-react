# Generated by Django 3.2.16 on 2023-07-03 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essences', '0004_auto_20230703_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
    ]
