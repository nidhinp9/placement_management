# Generated by Django 4.1.4 on 2023-01-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_pasteducationdetails_past_education_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='current_education_details',
            name='eighth_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='fifth_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='first_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='fourth_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='second_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='seventh_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='sixth_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_education_details',
            name='third_sem_sgpa',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
