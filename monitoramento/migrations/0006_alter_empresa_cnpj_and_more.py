# Generated by Django 4.2.2 on 2023-11-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoramento', '0005_alter_funcionario_senha_funcionario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.CharField(max_length=18, unique=True),
        ),
        migrations.AlterField(
            model_name='representante',
            name='cpf_representante',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
