# Generated by Django 4.2.6 on 2023-10-13 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_project_primary_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='primary_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_image', to='base.projectimage'),
        ),
    ]
