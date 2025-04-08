# Generated by Django 5.1.7 on 2025-04-08 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-date_added',)},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='created_date',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='modified_date',
            new_name='last_modified',
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
