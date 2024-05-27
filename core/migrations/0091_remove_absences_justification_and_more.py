# Generated by Django 5.0.4 on 2024-05-26 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0090_absences_trimester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absences',
            name='justification',
        ),
        migrations.AddField(
            model_name='absences',
            name='number_of_justitifed_absences',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='absences',
            name='number_of_unjustitifed_absences',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='absences',
            name='school_year',
            field=models.CharField(max_length=9, null=True),
        ),
    ]
