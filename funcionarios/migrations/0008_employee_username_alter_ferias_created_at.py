# Generated by Django 4.2 on 2023-05-31 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("funcionarios", "0007_ferias_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="username",
            field=models.CharField(
                default=models.CharField(max_length=255), max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="ferias",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
