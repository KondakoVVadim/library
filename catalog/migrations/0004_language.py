# Generated by Django 4.1.4 on 2023-02-10 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_author_options_alter_book_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
                        max_length=200,
                    ),
                ),
            ],
        ),
    ]