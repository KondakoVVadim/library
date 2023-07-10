# Generated by Django 4.1.4 on 2023-07-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_book_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ManyToManyField(to='catalog.language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]
