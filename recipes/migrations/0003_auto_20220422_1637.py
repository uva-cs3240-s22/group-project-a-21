# Generated by Django 3.1.2 on 2022-04-22 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220422_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='forks',
        ),
        migrations.AddField(
            model_name='recipe',
            name='forkedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='original', to='recipes.recipe'),
        ),
    ]
