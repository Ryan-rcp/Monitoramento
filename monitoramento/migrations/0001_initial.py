# Generated by Django 4.2.2 on 2023-10-26 15:29

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao_social', models.CharField(max_length=50)),
                ('nome_fantasia', models.CharField(max_length=50)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('ramo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_expediente', models.CharField(max_length=100)),
                ('dia_da_semana', models.CharField(max_length=253)),
                ('entrada_1', models.TimeField()),
                ('saida_1', models.TimeField()),
                ('entrada_2', models.TimeField()),
                ('saida_2', models.TimeField()),
                ('horario_total', models.TimeField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Setores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_setor', models.CharField(max_length=15)),
                ('descricao_setor', models.CharField(max_length=100)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula_funcionario', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(regex='^\\d{6}$')])),
                ('nome_funcionario', models.CharField(max_length=25)),
                ('sobrenome_funcionario', models.CharField(max_length=25)),
                ('cpf_funcionario', models.CharField(max_length=11, unique=True)),
                ('cargo_funcionario', models.CharField(max_length=14)),
                ('data_nascimento_funcionario', models.DateField()),
                ('email_funcionario', models.EmailField(max_length=254, unique=True)),
                ('senha_funcionario', models.CharField(max_length=8)),
                ('telefone_funcionario', models.CharField(max_length=11)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('online', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.empresa')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.expediente')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.setores')),
            ],
        ),
        migrations.CreateModel(
            name='BlackListSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_site', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=100)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='BlackListApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_app', models.CharField(max_length=50)),
                ('executavel', models.CharField(max_length=50)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='Atividades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_atividade', models.CharField(max_length=100)),
                ('descricao_atividade', models.CharField(max_length=200)),
                ('status_atividade', models.CharField(choices=[('Não iniciado', 'Não iniciado'), ('Em progresso', 'Em progresso'), ('Concluído', 'Concluído'), ('Em espera', 'Em espera')], default='Não iniciado', max_length=200)),
                ('data_atividade', models.DateField()),
                ('tempo_entrega', models.TimeField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.empresa')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='Representante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nome_representante', models.CharField(max_length=25)),
                ('sobrenome_representante', models.CharField(max_length=25)),
                ('cpf_representante', models.CharField(max_length=11, unique=True)),
                ('cargo_representante', models.CharField(max_length=20)),
                ('data_nascimento_representante', models.DateField()),
                ('telefone_representante', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=8)),
                ('username', models.CharField(default='', max_length=150)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoramento.empresa')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]