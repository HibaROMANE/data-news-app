# Generated by Django 4.2.1 on 2023-05-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('URL', models.CharField(max_length=500)),
                ('Paragraph', models.TextField()),
                ('Image_URL', models.CharField(max_length=500)),
                ('Date', models.CharField(max_length=200)),
            ],
        ),
    ]