# Generated by Django 4.2.2 on 2023-11-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoramento', '0004_alter_representante_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='senha_funcionario',
            field=models.TextField(),
        ),
    ]
