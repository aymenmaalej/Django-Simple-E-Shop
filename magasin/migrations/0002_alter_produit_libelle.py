# Generated by Django 5.0.2 on 2024-02-19 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='libelle',
            field=models.CharField(max_length=100),
        ),
    ]
