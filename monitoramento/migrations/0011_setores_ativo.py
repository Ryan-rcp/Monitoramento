# Generated by Django 4.2.2 on 2023-12-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoramento', '0010_alter_funcionario_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='setores',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
