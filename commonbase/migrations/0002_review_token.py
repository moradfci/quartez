# Generated by Django 5.0.6 on 2024-08-27 18:06

import commonbase.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("commonbase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="token",
            field=commonbase.fields.EncryptedField(blank=True, null=True),
        ),
    ]
