# Generated by Django 5.1 on 2024-08-29 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beast', '0001_initial'),
        ('nest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='beast',
            name='nest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='beasts', to='nest.nest', verbose_name='Гнездо'),
        ),
        migrations.AddField(
            model_name='beast',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beasts', to=settings.AUTH_USER_MODEL, verbose_name='Хозяин'),
        ),
        migrations.AddConstraint(
            model_name='beast',
            constraint=models.UniqueConstraint(fields=('owner', 'name'), name='beast_name_owner_unique'),
        ),
    ]
