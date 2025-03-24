# Generated by Django 2.1.5 on 2022-10-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_siteparameters_footer_injection'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteparameters',
            name='authorByContributionCount',
            field=models.IntegerField(default=20, help_text="number of people to be listed in the 'authors by contribution' page"),
        ),
    ]
