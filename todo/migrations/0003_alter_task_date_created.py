# Generated by Django 5.0.6 on 2024-06-08 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_task_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
