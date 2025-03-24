# Generated by Django 2.1.4 on 2022-07-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_siteparameters_header_injection'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteparameters',
            name='footer_injection',
            field=models.TextField(blank=True, help_text='html code which will be inserted in every page at the end of the <body> section. Pay attention: insecure code might disrupt the server funcionality.'),
        ),
    ]
