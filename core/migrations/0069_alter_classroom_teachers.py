# Generated by Django 5.0.4 on 2024-05-24 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_alter_student_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='teachers',
            field=models.ManyToManyField(blank=True, null=True, related_name='classrooms', to='core.teacher'),
        ),
    ]
