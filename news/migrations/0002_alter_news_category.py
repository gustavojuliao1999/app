# Generated by Django 4.1.5 on 2023-10-26 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.CharField(choices=[('politics', 'Politics'), ('sports', 'Sports'), ('entertainment', 'Entertainment'), ('technology', 'Technology')], max_length=50, null=True),
        ),
    ]
