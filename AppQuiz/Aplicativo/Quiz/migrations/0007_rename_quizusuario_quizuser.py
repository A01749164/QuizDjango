# Generated by Django 4.2.1 on 2023-05-29 15:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Quiz', '0006_rename_elegirrespuesta_chooseanswer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuizUsuario',
            new_name='QuizUser',
        ),
    ]
