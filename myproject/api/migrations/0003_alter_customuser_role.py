# Generated by Django 5.1 on 2024-08-28 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('user', 'User'), ('block', 'Block')], default='user', max_length=10),
        ),
    ]
