# Generated by Django 5.0.4 on 2024-05-24 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_alter_student_options_alter_teacher_options_parent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ParentChildRelationship',
        ),
    ]
