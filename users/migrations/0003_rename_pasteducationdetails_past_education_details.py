# Generated by Django 4.1.4 on 2023-01-14 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_current_education_details_pasteducationdetails_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PastEducationDetails',
            new_name='Past_Education_Details',
        ),
    ]
