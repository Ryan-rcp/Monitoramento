# Generated by Django 4.2.2 on 2023-12-04 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoramento', '0013_alter_funcionario_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='setor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoramento.setores'),
        ),
    ]
