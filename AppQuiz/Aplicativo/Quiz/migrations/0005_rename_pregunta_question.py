# Generated by Django 4.2.1 on 2023-05-29 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0004_alter_preguntasrespondidas_respuesa'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pregunta',
            new_name='Question',
        ),
    ]
