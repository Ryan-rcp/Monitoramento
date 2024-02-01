from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.utils import timezone
from .forms import Cadastro_blacklistApp, Cadastro_representante, Login, Cadastro_funcionario, Cadastro_setores, Cadastro_expediente, Cadastro_blacklistSite, Cadastro_atividade
from .models import BlackListApp, Empresa, Representante, Funcionario, Setores, Expediente, BlackListSite, Atividades
from datetime import datetime, date, time
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash


############### PAGINA DE LOGIN ###############
""" def login_view(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            # Verificar se o usuário existe com base no e-mail
            try:
                user = Representante.objects.get(email=email)
            except Representante.DoesNotExist:
                mensagem = "E-mail ou senha inválidos."
                return render(request, 'login.html', {'form': form, 'mensagem': mensagem})

            # Verificar a senha do usuário
            if user.password == senha:
                # Autenticar manualmente o usuário
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                # Redirecionar para a página após o login ser bem-sucedido
                # substitua 'pagina_inicial' pelo nome da sua página inicial
                return redirect('principal')
            else:
                mensagem = "E-mail ou senha inválidos."
                return render(request, 'login.html', {'form': form, 'mensagem': mensagem})
    else:
        form = Login()

    return render(request, 'login.html', {'form': form}) """
def login_view(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            # Autenticar o usuário
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                login(request, user)
                return redirect('principal')
            else:
                mensagem = "E-mail ou senha inválidos."
                return render(request, 'login.html', {'form': form, 'mensagem': mensagem})
    else:
        form = Login()

    return render(request, 'login.html', {'form': form})

############### LOGOUT ###############
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

############### RECUPERAÇÃO DE SENHA ###############
def recuperar_senha(request):
    return render(request, 'esqueciASenha.html')

def password_reset_done(request):
    return render(request, 'confirmacao_recuperacao.html')


##########################################################################
###################### CADASTRO REPRESENTANTE ############################
##########################################################################


def cadastro_representante(request):
    if request.method == 'POST':
        form = Cadastro_representante(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            cpf = form.cleaned_data['cpf_representante']
            senha = form.cleaned_data['password1']

            cnpj = form.cleaned_data['cnpj']
            empresa, created = Empresa.objects.get_or_create(cnpj=cnpj, defaults={
                'razao_social': form.cleaned_data['razao_social'],
                'nome_fantasia': form.cleaned_data['nome_fantasia'],
                'ramo': form.cleaned_data['ramo']
            })

            if Funcionario.objects.filter(email_funcionario=email).exists() or Representante.objects.filter(email=email).exists():
                form.add_error('Este e-mail já está cadastrado.')
            if Funcionario.objects.filter(cpf_funcionario=cpf).exists() or Representante.objects.filter(cpf_representante=cpf).exists():
                form.add_error('Este cpf já está cadastrado.')
                
            if not form.errors:
                # Criar a instância do representante
                representante = Representante(
                    empresa=empresa,
                    nome_representante=form.cleaned_data['nome_representante'],
                    sobrenome_representante=form.cleaned_data['sobrenome_representante'],
                    cpf_representante=cpf,
                    cargo_representante=form.cleaned_data['cargo_representante'],
                    data_nascimento_representante=form.cleaned_data['data_nascimento_representante'],
                    email=email,
                    telefone_representante=form.cleaned_data['telefone_representante']
                )
                representante.set_password(senha)
                representante.save()
                
                # Enviar email de confirmação
                mail_subject = 'Ative sua conta.'
                message = render_to_string('email.html', {
                    'user': representante,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(representante.pk)),
                    'token': default_token_generator.make_token(representante),
                })
                send_mail(mail_subject, message, 'tccsoftware.monitoramento@gmail.com', [email])

                return redirect('login')

        return render(request, 'cadastro_representante.html', {'form': form})
    else:
        form = Cadastro_representante()

    return render(request, 'cadastro_representante.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        representante = Representante.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Representante.DoesNotExist):
        representante = None

    if representante is not None and default_token_generator.check_token(representante, token):
        # Ative a conta do representante aqui
        representante.is_active = True
        representante.save()
        messages.success(request, 'Sua conta foi ativada com sucesso!')
        return redirect('login')
    else:
        return render(request, 'activation_invalid.html')

##########################################################################
###################### CADASTRO FUNCIONARIO ############################
##########################################################################
@login_required
def cadastro_funcionarios(request):
    if request.method == 'POST':
        form = Cadastro_funcionario(request.POST, request.FILES, empresa=request.user.empresa)


        if form.is_valid():
            empresa = request.user.empresa  # Obtém a empresa do representante logado
            matricula = form.cleaned_data['matricula_funcionario']
            cpf = form.cleaned_data['cpf_funcionario']
            email = form.cleaned_data['email_funcionario']
            setor= form.cleaned_data['nome_setor']
            

            # Verifica se a matrícula já está cadastrada para a empresa
            if Funcionario.objects.filter(empresa=empresa, matricula_funcionario=matricula).exists():
                form.add_error(
                    'matricula_funcionario', 'Esta matrícula já está cadastrada para esta empresa.')
            if Funcionario.objects.filter(email_funcionario=email).exists() or Representante.objects.filter(email=email).exists():
                form.add_error('email_funcionario',
                               'Este e-mail já está cadastrado.')
            if Funcionario.objects.filter(cpf_funcionario=cpf).exists() or Representante.objects.filter(cpf_representante=cpf).exists():
                form.add_error('cpf_funcionario',
                               'Este cpf já está cadastrado.')

            if not form.errors:
                # Cria uma instância do funcionário
                funcionario = Funcionario(
                    empresa=empresa,
                    setor = setor,
                    matricula_funcionario=matricula,
                    nome_funcionario=form.cleaned_data['nome_funcionario'],
                    sobrenome_funcionario=form.cleaned_data['sobrenome_funcionario'],
                    cpf_funcionario=cpf,
                    # Adiciona o horário selecionado pelo usuário
                    horario=form.cleaned_data['horario'],
                    cargo_funcionario=form.cleaned_data['cargo_funcionario'],
                    data_nascimento_funcionario=form.cleaned_data['data_nascimento_funcionario'],
                    email_funcionario=email,
                    senha_funcionario=form.cleaned_data['senha_funcionario'],
                    telefone_funcionario=form.cleaned_data['telefone_funcionario'],
                    avatar=form.cleaned_data['avatar']
                )
                
                funcionario.save()

                # Redireciona para a página de dashboard após o cadastro
                return redirect('lista_funcionarios')

    else:
        form = Cadastro_funcionario(empresa=request.user.empresa)

    return render(request, 'cadastro_funcionario.html', {'form': form})

##########################################################################
############################## CADASTRO SETOR ############################
##########################################################################

@login_required
def cadastro_setor(request):
    if request.method == 'POST':
        form = Cadastro_setores(request.POST)

        if form.is_valid():
            empresa = request.user.empresa  # Obtém a empresa do representante logado
            setor_nome = form.cleaned_data['nome_setor']

            if Setores.objects.filter(empresa=empresa, nome_setor=setor_nome).exists():
                form.add_error(
                    'nome_setor', 'Este setor já está cadastrado para esta empresa.')

            if not form.errors:
                setor = Setores(
                    empresa=empresa,
                    nome_setor=setor_nome,
                    descricao_setor=form.cleaned_data['descricao_setor']
                )
                setor.save()  # Redireciona para a página de dashboard após o cadastro
                return redirect('lista_setores')

    else:
        form = Cadastro_setores()

    return render(request, 'cadastro_setor.html', {'form': form})

##########################################################################
############################## CADASTRO Atividade ############################
##########################################################################
@login_required
def cadastro_atividade(request):
    if request.method == 'POST':
        form = Cadastro_atividade(request.POST, empresa=request.user.empresa)

        if form.is_valid():
            empresa = request.user.empresa  # Obtém a empresa do representante logado
            atividade = Atividades(
                empresa=empresa,
                nome_atividade=form.cleaned_data['nome_atividade'],
                descricao_atividade=form.cleaned_data['descricao_atividade'],
                data_atividade = datetime.now().date(),
                tempo_entrega=form.cleaned_data['tempo_entrega'],
                funcionario=form.cleaned_data['funcionario'],
            )
            atividade.save()  # Redireciona para a página de dashboard após o cadastro
            return redirect('lista_atividade')

    else:
        form = Cadastro_atividade(empresa=request.user.empresa)

    return render(request, 'cadastro_atividade.html', {'form': form})

##########################################################################
######################### CADASTRO EXPEDIENTE ############################
##########################################################################

@login_required
def cadastro_expediente(request):
    if request.method == 'POST':
        form = Cadastro_expediente(request.POST)

        if form.is_valid():
            empresa = request.user.empresa  # Obtém a empresa do representante logado
            dias_da_semana = form.cleaned_data['dias_da_semana']

            # Cria objetos datetime a partir dos valores dos campos TimeField
            entrada_1 = form.cleaned_data['entrada_1']
            saida_1 = form.cleaned_data['saida_1']
            entrada_2 = form.cleaned_data['entrada_2']
            saida_2 = form.cleaned_data['saida_2']
            entrada_1_datetime = datetime.combine(date.today(), entrada_1)
            saida_1_datetime = datetime.combine(date.today(), saida_1)
            entrada_2_datetime = datetime.combine(date.today(), entrada_2)
            saida_2_datetime = datetime.combine(date.today(), saida_2)

            # Calcula as diferenças entre as horas
            diferenca_1 = saida_1_datetime - entrada_1_datetime
            diferenca_2 = saida_2_datetime - entrada_2_datetime

            # Calcula a soma das diferenças
            total_seconds = int((diferenca_1 + diferenca_2).total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Cria uma instância do expediente
            expediente = Expediente(
                empresa=empresa,
                descricao_expediente=form.cleaned_data['descricao'],
                dia_da_semana=','.join(dias_da_semana),
                entrada_1=entrada_1,
                saida_1=saida_1,
                entrada_2=entrada_2,
                saida_2=saida_2,
                horario_total=time(hour=hours, minute=minutes, second=seconds),
            )
            expediente.save()

            # Redireciona para a página de dashboard após o cadastro
            return redirect('lista_expediente')

    else:
        form = Cadastro_expediente()

    return render(request, 'cadastro_expediente.html', {'form': form})

##########################################################################
############################## EDITAR REPRESENTANTE ########################
##########################################################################
@login_required
def editar_representante(request):
    representante = request.user

    if request.method == 'POST':
        form = Cadastro_representante(request.POST, request.FILES, instance=representante)
        # Verifica se o email ou cpf já existem para outro usuário
        email = form.data['email']
        cpf = form.data['cpf_representante']
        if Funcionario.objects.filter(email_funcionario=email).exists() or Representante.objects.exclude(pk=representante.pk).filter(email=email).exists():
            form.add_error('email',
                               'Este e-mail já está cadastrado.')
        if Funcionario.objects.filter(cpf_funcionario=cpf).exists() or Representante.objects.exclude(pk=representante.pk).filter(cpf_representante=cpf).exists():
            form.add_error('cpf_representante',
                            'Este cpf já está cadastrado.')
        else:
            representante.nome_representante = form.data['nome_representante']
            representante.sobrenome_representante = form.data['sobrenome_representante']
            representante.cpf_representante = cpf
            representante.email = email
            representante.cargo_representante = form.data['cargo_representante']
            representante.data_nascimento_representante = form.data['data_nascimento_representante']
            representante.telefone_representante = form.data['telefone_representante']
            senha = form.data['password1']
            representante.set_password(senha)
            representante.save()
            
            # Atualiza a sessão para manter o usuário logado após a alteração da senha
            update_session_auth_hash(request, representante)
            return redirect('principal')
    else:
        form = Cadastro_representante(instance=representante)

    return render(request, 'editar_representante.html', {'form': form})

##########################################################################
############################## EDITAR FUNCIONARIO ########################
##########################################################################
@login_required
def editar_funcionario(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
    empresa = request.user.empresa

    if request.method == 'POST':
        form = Cadastro_funcionario(request.POST, request.FILES, empresa=request.user.empresa)
        if form.is_valid():
            matricula = form.cleaned_data['matricula_funcionario']
            cpf = form.cleaned_data['cpf_funcionario']
            email = form.cleaned_data['email_funcionario']
            
            # Verifica se a matrícula já está cadastrada para a empresa
            if Funcionario.objects.exclude(pk=funcionario_id).filter(empresa=empresa, matricula_funcionario=matricula).exists():
                form.add_error(
                    'matricula_funcionario', 'Esta matrícula já está cadastrada para esta empresa.')

            if Funcionario.objects.exclude(pk=funcionario_id).filter(email_funcionario=email).exists() or Representante.objects.filter(email=email).exists():
                form.add_error('email_funcionario',
                               'Este e-mail já está cadastrado.')

            # Verifica se o CPF já está cadastrado e não pertence ao funcionário em edição
            if Funcionario.objects.exclude(pk=funcionario_id).filter(cpf_funcionario=cpf).exists() or Representante.objects.filter(cpf_representante=cpf).exists():
                form.add_error('cpf_funcionario',
                               'Este cpf já está cadastrado.')
            if not form.errors:   
                funcionario.matricula_funcionario = form.cleaned_data['matricula_funcionario']
                funcionario.nome_funcionario = form.cleaned_data['nome_funcionario']
                funcionario.sobrenome_funcionario = form.cleaned_data['sobrenome_funcionario']
                funcionario.cpf_funcionario = form.cleaned_data['cpf_funcionario']
                funcionario.cargo_funcionario = form.cleaned_data['cargo_funcionario']
                funcionario.setor = form.cleaned_data['nome_setor']  # Atualiza o setor do funcionário
                funcionario.horario = form.cleaned_data['horario']
                funcionario.data_nascimento_funcionario = form.cleaned_data[
                    'data_nascimento_funcionario']
                funcionario.email_funcionario = form.cleaned_data['email_funcionario']
                funcionario.senha_funcionario = form.cleaned_data['senha_funcionario']
                funcionario.telefone_funcionario = form.cleaned_data['telefone_funcionario']
                if form.cleaned_data['avatar']:
                    funcionario.avatar = form.cleaned_data['avatar']
                funcionario.ferias = form.cleaned_data['ferias']
                funcionario.ativo = form.cleaned_data['ativo']
                
                funcionario.save()
                return redirect('lista_funcionarios')
    else:
        form = Cadastro_funcionario(initial={  
            'matricula_funcionario': funcionario.matricula_funcionario,
            'nome_funcionario': funcionario.nome_funcionario,
            'sobrenome_funcionario': funcionario.sobrenome_funcionario,
            'cpf_funcionario': funcionario.cpf_funcionario,
            'cargo_funcionario': funcionario.cargo_funcionario,
            'nome_setor': funcionario.setor,
            'horario': funcionario.horario,
            'data_nascimento_funcionario': funcionario.data_nascimento_funcionario,
            'email_funcionario': funcionario.email_funcionario,
            'senha_funcionario': funcionario.senha_funcionario,
            'confirmar_senha_funcionario': funcionario.senha_funcionario,
            'telefone_funcionario': funcionario.telefone_funcionario,
            'avatar': funcionario.avatar,
            'ferias':funcionario.ferias,
            'ativo':funcionario.ativo
        }, empresa=empresa)

    return render(request, 'editar_funcionario.html', {'form': form, 'funcionario': funcionario})

##########################################################################
############################## EDITAR SETOR ############################
##########################################################################

@login_required
def editar_setor(request, setor_id):
    setor = get_object_or_404(Setores, pk=setor_id)
    if request.method == 'POST':
        form = Cadastro_setores(request.POST)

        if form.is_valid():

            setor.nome_setor = form.cleaned_data['nome_setor']
            setor.descricao_setor = form.cleaned_data['descricao_setor']
            setor.ativo = form.cleaned_data['ativo']
            setor.save()
            return redirect('lista_setores')
    else:
        form = Cadastro_setores(initial={
            'nome_setor': setor.nome_setor,
            'descricao_setor': setor.descricao_setor,
            'ativo' : setor.ativo
        })
    return render(request, 'editar_setor.html', {'form': form, 'setor': setor})

##########################################################################
############################## EDITAR EXPEDIENTE #########################
##########################################################################

@login_required
def editar_expediente(request, expediente_id):
    expediente = get_object_or_404(Expediente, pk=expediente_id)
    if request.method == 'POST':
        form = Cadastro_expediente(request.POST)

        if form.is_valid():
            expediente.descricao_expediente = form.cleaned_data['descricao']
            # remova a vírgula no final desta linha
            expediente.dia_da_semana = ','.join(
                form.cleaned_data['dias_da_semana'])
            expediente.entrada_1 = form.cleaned_data['entrada_1']
            expediente.saida_1 = form.cleaned_data['saida_1']
            expediente.entrada_2 = form.cleaned_data['entrada_2']
            expediente.saida_2 = form.cleaned_data['saida_2']
            expediente.save()
            return redirect('lista_expediente')
    else:
        dias_semana_selecionados = expediente.dia_da_semana.split(
            ',') if expediente.dia_da_semana else []

        form = Cadastro_expediente(initial={
            'descricao': expediente.descricao_expediente,
            'dias_da_semana': dias_semana_selecionados,
            'entrada_1': expediente.entrada_1,
            'saida_1': expediente.saida_1,
            'entrada_2': expediente.entrada_2,
            'saida_2': expediente.saida_2,

        })
    return render(request, 'editar_expediente.html', {'form': form, 'expediente': expediente})

##########################################################################
############################## EDITAR EXPEDIENTE #########################
##########################################################################

@login_required
def editar_atividade(request, atividade_id):
    atividade = get_object_or_404(Atividades, pk=atividade_id)
    empresa=request.user.empresa
    if request.method == 'POST':
        form = Cadastro_atividade(request.POST, empresa=empresa)

        if form.is_valid():
            atividade.nome_atividade = form.cleaned_data['nome_atividade']
            atividade.descricao_atividade = form.cleaned_data['descricao_atividade']
            atividade.tempo_entrega=form.cleaned_data['tempo_entrega']
            atividade.funcionario=form.cleaned_data['funcionario']
            atividade.save()
            return redirect('lista_atividade')
    else:
        form = Cadastro_atividade(initial={
            'nome_atividade': atividade.nome_atividade,
            'descricao_atividade': atividade.descricao_atividade,
            'tempo_entrega': atividade.tempo_entrega,
            'funcionario': atividade.funcionario,

        }, empresa=empresa)
    return render(request, 'editar_atividade.html', {'form': form, 'atividade': atividade})

##########################################################################
############################## LISTA FUNCIONARIO #########################
##########################################################################


@login_required
def lista_funcionarios(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    return render(request, 'lista_funcionario.html', {'funcionarios': funcionarios})

##########################################################################
############################## LISTA SETORES #########################
##########################################################################


@login_required
def lista_setores(request):
    empresa = request.user.empresa
    setores = Setores.objects.filter(empresa=empresa)
    return render(request, 'lista_setores.html', {'setores': setores})

##########################################################################
############################## LISTA EXPEDIENTE #########################
##########################################################################


@login_required
def lista_expediente(request):
    empresa = request.user.empresa
    expediente = Expediente.objects.filter(empresa=empresa)
    return render(request, 'lista_expediente.html', {'expediente': expediente})

##########################################################################
############################## LISTA ATIVIDADES #########################
##########################################################################


@login_required
def lista_atividade(request):
    empresa = request.user.empresa
    atividade = Atividades.objects.filter(empresa=empresa, status_atividade__in=['Não iniciado', 'Em progresso'], funcionario__ativo = True)
    return render(request, 'lista_atividade.html', {'atividade': atividade})

##########################################################################
############################## LISTA ACESSOS #########################
##########################################################################


@login_required
def lista_acessos(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    return render(request, 'lista_acessos.html', {'funcionarios': funcionarios})

##########################################################################
############################## LISTA PRODUTIVIDADE #########################
##########################################################################


@login_required
def lista_produtividade(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    return render(request, 'lista_produtividade.html', {'funcionarios': funcionarios})

##########################################################################
############################## LISTA PONTOS #########################
##########################################################################


@login_required
def lista_pontos(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    return render(request, 'lista_registroPonto.html', {'funcionarios': funcionarios})


##########################################################################
############################## EXCLUIR SETOR #########################
##########################################################################
@login_required
def excluir_setor(request, setor_id):
    setor = get_object_or_404(Setores, pk=setor_id)
    setor.delete()
    return redirect('lista_setores')


##########################################################################
############################## EXCLUIR FUNCIONARIO #########################
##########################################################################
@login_required
def excluir_funcionario(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
    funcionario.ativo = False
    funcionario.save()
    return redirect('lista_funcionarios')

##########################################################################
############################## LISTA EXPEDIENTE #########################
##########################################################################


def excluir_expediente(request, expediente_id):
    expediente = get_object_or_404(Expediente, pk=expediente_id)
    expediente.delete()
    return redirect('lista_expediente')

##########################################################################
############################## EXCLUIR ATIVIDADE #########################
##########################################################################


def excluir_atividade(request, atividade_id):
    atividade = get_object_or_404(Atividades, pk=atividade_id)
    atividade.delete()
    return redirect('lista_atividade')


@login_required
def acessos_funcionario(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)
    return render(request, 'acessos_funcionario.html', {'funcionario': funcionario})

@login_required
def produtividade_funcionario(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)
    return render(request, 'produtividade_funcionario.html', {'funcionario': funcionario})

@login_required
def pontos_funcionario(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)
    return render(request, 'pontos_funcionario.html', {'funcionario': funcionario})


##########################################################################
############################## GRAFICOS #########################
##########################################################################
def grf_acesso_site(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_inicial = data_final = datetime.now().date()
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT nome_site, COUNT(*) as total
            FROM monitoramento_capturasite
            WHERE funcionario_id = %s AND data_visita BETWEEN %s AND %s
            GROUP BY nome_site
            ORDER BY total DESC
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        sites = cursor.fetchall()

    data = {
        'labels': [site[0] for site in sites],
        'data': [site[1] for site in sites]
    }
    return JsonResponse(data)


def grf_acesso_aplicativo(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_inicial = data_final = datetime.now().date()
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT nome_app, SUM(TIME_TO_SEC(tempo_execucaoExp)) as total
            FROM monitoramento_capturaApp
            WHERE funcionario_id = %s AND data_execucao BETWEEN %s AND %s
            GROUP BY nome_app
            ORDER BY total DESC
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        apps = cursor.fetchall()

    data = {
        'labels': [app[0] for app in apps],
        'data': [app[1] for app in apps]
    }
    return JsonResponse(data)


def grf_registro_ponto(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_ponto, SUM(TIME_TO_SEC(horas_trabalhadas)) as total
            FROM monitoramento_pontofuncionario
            WHERE funcionario_id = %s AND data_ponto BETWEEN %s AND %s
            GROUP BY data_ponto
            ORDER BY data_ponto 
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        pontos = cursor.fetchall()

    data = {
        'labels': [ponto[0] for ponto in pontos],
        'data': [ponto[1] for ponto in pontos]
    }
    return JsonResponse(data)


def grf_horas_extras(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_ponto, SUM(TIME_TO_SEC(horas_extra)) as total
            FROM monitoramento_pontofuncionario
            WHERE funcionario_id = %s AND data_ponto BETWEEN %s AND %s
            GROUP BY data_ponto
            ORDER BY data_ponto 
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        extras = cursor.fetchall()

    data = {
        'labels': [extra[0] for extra in extras],
        'data': [extra[1] for extra in extras]
    }
    return JsonResponse(data)


def grf_horas_pendentes(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_ponto, SUM(TIME_TO_SEC(horas_falta)) as total
            FROM monitoramento_pontofuncionario
            WHERE funcionario_id = %s AND data_ponto BETWEEN %s AND %s
            GROUP BY data_ponto
            ORDER BY data_ponto 
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        pendentes = cursor.fetchall()

    data = {
        'labels': [pendente[0] for pendente in pendentes],
        'data': [pendente[1] for pendente in pendentes]
    }
    return JsonResponse(data)


def grf_inatividade(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT TIME_TO_SEC(hora_inativo) as hora, TIME_TO_SEC(tempo_inativo) as tempo
            FROM monitoramento_inatividade
            WHERE funcionario_id = %s AND data_inativo BETWEEN %s AND %s
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        inatividade = cursor.fetchall()

    data = {
        'labels': [inativo[0] for inativo in inatividade],
        'data': [inativo[1] for inativo in inatividade]
    }
    return JsonResponse(data)


def grf_previsao(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)
    hoje = timezone.now().date()
    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_prev as data, prev_setor as setor, prev_func as func
            FROM monitoramento_previsao
            WHERE funcionario_id = %s AND data_prev BETWEEN %s AND %s
            ORDER BY data
        '''
        cursor.execute(query, [funcionario_id, hoje, data_final])
        previsao = cursor.fetchall()

    data = {
        'labels': [prev[0] for prev in previsao],
        'data1': [prev[1] for prev in previsao],
        'data2': [prev[2] for prev in previsao],
    }
    return JsonResponse(data)

def grf_rendimento(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT 
                mtt_sum.data_conclusao,
                ROUND(((TIME_TO_SEC(ma.tempo_entrega) / (mtt_sum.total_horaTotal + 1 + (2 * COALESCE(mit_sum.total_tempo_inativo, 0)))) - 1)*100, 2) as rendimento
            FROM 
                (SELECT atividade_id, data_conclusao, SUM(TIME_TO_SEC(horaTotal)) AS total_horaTotal
                FROM monitoramento_tempo_tarefa
                WHERE funcionario_id = %s
                GROUP BY atividade_id, data_conclusao) AS mtt_sum
            LEFT JOIN 
                (SELECT atividade_id, SUM(TIME_TO_SEC(tempo_inativo)) AS total_tempo_inativo
                FROM monitoramento_inatividade_tarefa
                WHERE funcionario_id = %s
                GROUP BY atividade_id) AS mit_sum 
            ON mtt_sum.atividade_id = mit_sum.atividade_id
            INNER JOIN monitoramento_atividades AS ma ON mtt_sum.atividade_id = ma.id
            WHERE ma.status_atividade = 'Concluído' AND mtt_sum.data_conclusao BETWEEN %s AND %s
            ORDER BY data_conclusao;
        '''
        cursor.execute(query, [funcionario_id, funcionario_id, data_inicial, data_final])
        rendimento = cursor.fetchall()

    data = {
        'labels': [rend[0] for rend in rendimento],
        'data': [rend[1] for rend in rendimento],
    }
    return JsonResponse(data)

def grf_agendado(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT 
                atv.nome_atividade,
                ag.previsao
            FROM monitoramento_atv_agendada as ag
            INNER JOIN monitoramento_atividades as atv ON atv.id = ag.atividade_id
            INNER JOIN monitoramento_funcionario AS func ON ag.funcionario_id = func.id
            WHERE func.id = %s AND atv.data_atividade BETWEEN %s AND %s;
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        agendado = cursor.fetchall()

    data = {
        'labels': [agen[0] for agen in agendado],
        'data': [agen[1] for agen in agendado],
    }
    return JsonResponse(data)

##########################################################################
############################## TABELAS #########################
##########################################################################

def tbl_acesso_site(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_inicial = data_final = datetime.now().date()
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_visita, nome_site, url, horario_visita, blacklistsite
            FROM monitoramento_capturasite
            WHERE funcionario_id = %s AND data_visita BETWEEN %s AND %s
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        sites = cursor.fetchall()

        data = [{
            'data_visita': site[0].strftime('%d-%m-%Y'),
            'nome_site': site[1],
            'url': site[2],
            'horario_visita': site[3],
            'blacklistsite': site[4]
        } for site in sites]
        
    return JsonResponse(data, safe=False)

def tbl_acesso_aplicativo(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_inicial = data_final = datetime.now().date()
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
    with connection.cursor() as cursor:
        query = '''
        SELECT data_execucao, nome_app, horario_execucao, tempo_execucao, tempo_execucaoExp, blacklistapp, fc.nome_funcionario
                    FROM monitoramento_capturaapp, monitoramento_funcionario as fc
                    WHERE funcionario_id = %s AND data_execucao BETWEEN %s AND %s AND funcionario_id = fc.id
                    ORDER BY data_execucao
            
            
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        apps = cursor.fetchall()

        data = [{
            'data_execucao': app[0].strftime('%d-%m-%Y'),
            'nome_app': app[1],
            'horario_execucao': app[2],
            'tempo_execucao': app[3],
            'tempo_execucaoExp': app[4],
            # 'blacklistapp': "Negado" if app[4] == 1 else "Aprovado"
            'blacklistapp': app[5]
        }for app in apps]
    return JsonResponse(data, safe=False)

def tbl_registro_ponto(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        # Se nenhum filtro de data for especificado, mostre o mês atual
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_ponto, horario_entrada_manha, horario_saida_manha, horario_entrada_tarde, horario_saida_tarde, horas_trabalhadas, horas_extra, horas_falta
            FROM monitoramento_pontofuncionario
            WHERE funcionario_id = %s AND data_ponto BETWEEN %s AND %s
            ORDER BY data_ponto
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        pontos = cursor.fetchall()

    data = [{
        'data_ponto': ponto[0].strftime('%d-%m-%Y'),
        'horario_entrada_manha': ponto[1],
        'horario_saida_manha': ponto[2],
        'horario_entrada_tarde': ponto[3],
        'horario_saida_tarde': ponto[4],
        'horas_trabalhadas': ponto[5],
        'horas_extra': ponto[6],
        'horas_falta': ponto[7],
    } for ponto in pontos]
    return JsonResponse(data, safe=False)


def tbl_inatividade(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    with connection.cursor() as cursor:
        query = '''
            SELECT data_inativo, hora_inativo, tempo_inativo
            FROM monitoramento_inatividade
            WHERE funcionario_id = %s AND data_inativo BETWEEN %s AND %s
            ORDER BY data_inativo
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        inatividade = cursor.fetchall()

    data = [{
        'data_inativo': inativo[0].strftime('%d-%m-%Y'),
        'hora_inativo': inativo[1],
        'tempo_inativo': inativo[2],

    } for inativo in inatividade]
    return JsonResponse(data, safe=False)


def tbl_rendimento(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
    with connection.cursor() as cursor:
        query = '''
        SELECT 
            mtt_sum.data_conclusao,
            ROUND(((TIME_TO_SEC(ma.tempo_entrega) / (mtt_sum.total_horaTotal + 1 + (2 * COALESCE(mit_sum.total_tempo_inativo, 0)))) - 1)*100, 2) as rendimento,
            mp.prev_func
        FROM 
            (SELECT funcionario_id, atividade_id, data_conclusao, SUM(TIME_TO_SEC(horaTotal)) AS total_horaTotal
            FROM monitoramento_tempo_tarefa
            WHERE funcionario_id = %s
            GROUP BY atividade_id, data_conclusao) AS mtt_sum
        LEFT JOIN 
            (SELECT atividade_id, SUM(TIME_TO_SEC(tempo_inativo)) AS total_tempo_inativo
            FROM monitoramento_inatividade_tarefa
            WHERE funcionario_id = %s
            GROUP BY atividade_id) AS mit_sum 
        ON mtt_sum.atividade_id = mit_sum.atividade_id
        INNER JOIN monitoramento_atividades AS ma ON mtt_sum.atividade_id = ma.id
        INNER JOIN monitoramento_previsao AS mp ON mtt_sum.funcionario_id = mp.funcionario_id
        WHERE ma.status_atividade = 'Concluído' AND mtt_sum.data_conclusao = mp.data_prev AND mtt_sum.data_conclusao BETWEEN %s AND %s;
        '''
        cursor.execute(query, [funcionario_id, funcionario_id, data_inicial, data_final])
        rendimento = cursor.fetchall()

        data = [{
            'data_conclusao': rend[0].strftime('%d-%m-%Y'),
            'rendimento': rend[2],
            'previsao': rend[1],
        }for rend in rendimento]
    return JsonResponse(data, safe=False)

def tbl_atv_concluida(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
    with connection.cursor() as cursor:
        query = '''
        SELECT 
            ma.data_atividade,
            ma.nome_atividade,
            ma.tempo_entrega,
            mtt_sum.total_horaTotal,
            ma.status_atividade
        FROM 
            (SELECT atividade_id, data_conclusao, SUM(TIME_TO_SEC(horaTotal)) AS total_horaTotal
                FROM monitoramento_tempo_tarefa
                WHERE funcionario_id = %s
                GROUP BY atividade_id, data_conclusao) AS mtt_sum
		INNER JOIN monitoramento_atividades AS ma ON mtt_sum.atividade_id = ma.id
        WHERE status_atividade = 'Concluído' AND ma.funcionario_id = %s AND data_atividade BETWEEN %s AND %s
        ORDER BY ma.data_atividade;
        '''
        cursor.execute(query, [funcionario_id, funcionario_id, data_inicial, data_final])
        concluido = cursor.fetchall()

        data = [{
            'data_atividade': conclui[0].strftime('%d-%m-%Y'),
            'nome_atividade': conclui[1],
            'tempo_entrega': conclui[2],
            'horaTotal':conclui[3],
            'status': conclui[4],
        }for conclui in concluido]
    return JsonResponse(data, safe=False)

def tbl_atv_agendada(request, funcionario_id):
    data_inicial = request.GET.get('data_inicial', None)
    data_final = request.GET.get('data_final', None)

    if data_inicial is None or data_final is None:
        data_atual = timezone.now()
        data_inicial = data_atual.replace(day=1)
        ultimo_dia_mes = (data_atual.replace(
            day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        data_final = ultimo_dia_mes
    else:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
    with connection.cursor() as cursor:
        query = '''
        SELECT 
            atv.data_atividade,
            atv.nome_atividade,
            atv.status_atividade,
            ag.previsao
        FROM monitoramento_atv_agendada as ag, monitoramento_atividades as atv
        WHERE ag.atividade_id = atv.id AND ag.funcionario_id = %s AND atv.data_atividade BETWEEN %s AND %s AND atv.status_atividade = 'Não iniciado'
        ORDER BY atv.data_atividade;
        '''
        cursor.execute(query, [funcionario_id, data_inicial, data_final])
        agendado = cursor.fetchall()

        data = [{
            'data_atividade': ag[0].strftime('%d-%m-%Y'),
            'nome_atividade': ag[1],
            'status_atividade': ag[2],
            'previsao': ag[3],
        }for ag in agendado]
    return JsonResponse(data, safe=False)

##########################################################################
############################## BLACKLIST #################################
##########################################################################

def blackList(request, funcionario_id):
    funcionario = Funcionario.objects.get(id=funcionario_id)

    if request.method == 'POST':
        site_form = Cadastro_blacklistSite(request.POST)
        app_form = Cadastro_blacklistApp(request.POST)

        if site_form.is_valid():
            url = site_form.cleaned_data['url']

            if BlackListSite.objects.filter(funcionario=funcionario_id, url=url).exists():
                site_form.add_error(
                    'url', 'Esta URL já está cadastrada para este funcionário.')

            if not site_form.errors:
                blsite = BlackListSite(
                    funcionario=funcionario,
                    nome_site=site_form.cleaned_data['nome_site'],
                    url=url
                )
                blsite.save()
                return redirect('blackList', funcionario_id=blsite.funcionario.id)

        elif app_form.is_valid():
            executavel = app_form.cleaned_data['executavel']

            if BlackListApp.objects.filter(funcionario=funcionario_id, executavel=executavel).exists():
                app_form.add_error(
                    'executavel', 'Este aplicativo já está cadastrado para este funcionário.')

            if not app_form.errors:
                blapp = BlackListApp(
                    funcionario=funcionario,
                    nome_app=app_form.cleaned_data['nome_app'],
                    executavel=executavel
                )
                blapp.save()
                return redirect('blackList', funcionario_id=blapp.funcionario.id)

    else:
        site_form = Cadastro_blacklistSite()
        app_form = Cadastro_blacklistApp()

    return render(request, 'blackList.html', {'funcionario': funcionario, 'site_form': site_form, 'app_form': app_form})


def tbl_blsite(request, funcionario_id):
    with connection.cursor() as cursor:
        query = '''
            SELECT id, nome_site, url
            FROM monitoramento_blacklistsite
            WHERE funcionario_id = %s
        '''
        cursor.execute(query, [funcionario_id])
        sites = cursor.fetchall()

    data = [{
        'id': site[0],
        'nome_site': site[1],
        'url': site[2],
    } for site in sites]
    return JsonResponse(data, safe=False)

def tbl_blapp(request, funcionario_id):
    with connection.cursor() as cursor:
        query = '''
            SELECT id, nome_app, executavel
            FROM monitoramento_blacklistapp
            WHERE funcionario_id = %s
        '''
        cursor.execute(query, [funcionario_id])
        apps = cursor.fetchall()

    data = [{
        'id': app[0],
        'nome_app': app[1],
        'executavel': app[2],
    } for app in apps]
    return JsonResponse(data, safe=False)

def excluir_blacklistsite(request, blacklistsite_id):
    blsite = get_object_or_404(BlackListSite, pk=blacklistsite_id)
    blsite.delete()
    return redirect('blackList', funcionario_id=blsite.funcionario.id)

def excluir_blacklistapp(request, blacklistapp_id):
    blapp = get_object_or_404(BlackListApp, pk=blacklistapp_id)
    blapp.delete()
    return redirect('blackList', funcionario_id=blapp.funcionario.id)

@login_required
def principal(request):
    return render(request, 'principal.html')

def tbl_func_online(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    with connection.cursor() as cursor:
        query = '''
            SELECT matricula_funcionario, nome_funcionario, online
            FROM monitoramento_funcionario AS mf
            WHERE online = %s AND mf.id IN %s AND mf.ativo = True
            
        '''
        ids_funcionarios = [funcionario.id for funcionario in funcionarios]
        cursor.execute(query, [True, tuple(ids_funcionarios)])
        ativos = cursor.fetchall()

    data = [{
        'matricula_funcionario': online[0],
        'nome_funcionario': online[1],
        'online': online[2],
    } for online in ativos]
    return JsonResponse(data, safe=False)

""" def tbl_func_offline(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    with connection.cursor() as cursor:
        query = '''
            SELECT matricula_funcionario, nome_funcionario, online
            FROM monitoramento_funcionario AS mf
            WHERE online = %s AND mf.id = %s
            
        '''
        cursor.execute(query, [False])
        inativos = cursor.fetchall()

    data = [{
        'matricula_funcionario': online[0],
        'nome_funcionario': online[1],
        'online': online[2],
    } for online in inativos]
    return JsonResponse(data, safe=False) """
    
def tbl_func_offline(request):
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    with connection.cursor() as cursor:
        query = '''
            SELECT matricula_funcionario, nome_funcionario, online
            FROM monitoramento_funcionario AS mf
            WHERE online = %s AND mf.id IN %s AND mf.ativo = True
        '''
        # Aqui estamos convertendo funcionarios em uma lista de ids
        ids_funcionarios = [funcionario.id for funcionario in funcionarios]
        cursor.execute(query, [False, tuple(ids_funcionarios)])
        inativos = cursor.fetchall()

    data = [{
        'matricula_funcionario': online[0],
        'nome_funcionario': online[1],
        'online': online[2],
    } for online in inativos]
    return JsonResponse(data, safe=False)



def grf_aplicativo_online(request):
    data_atual = datetime.now().date()
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    with connection.cursor() as cursor:
        query = '''
            SELECT nome_app, SUM(TIME_TO_SEC(tempo_execucaoExp)) as total
            FROM monitoramento_capturaApp, monitoramento_funcionario as fc
            WHERE fc.online = %s AND data_execucao = %s AND fc.id IN %s
            GROUP BY nome_app
            ORDER BY total DESC
            LIMIT 10
        '''
        ids_funcionarios = [funcionario.id for funcionario in funcionarios]
        cursor.execute(query, [True, data_atual, tuple(ids_funcionarios)])
        apps = cursor.fetchall()
    
    data = {
        'labels': [app[0] for app in apps],
        'data': [app[1] for app in apps]
    }
    return JsonResponse(data)

def grf_site_online(request):
    data_atual = datetime.now().date()
    empresa = request.user.empresa
    funcionarios = Funcionario.objects.filter(empresa=empresa)
    with connection.cursor() as cursor:
        query = '''
            SELECT nome_site, COUNT(*) as total
            FROM monitoramento_capturasite, monitoramento_funcionario as fc
            WHERE online = %s AND data_visita = %s AND fc.id IN %s
            GROUP BY nome_site
            ORDER BY total DESC
            LIMIT 10
        '''
        ids_funcionarios = [funcionario.id for funcionario in funcionarios]
        cursor.execute(query, [True, data_atual, tuple(ids_funcionarios)])
        sites = cursor.fetchall()

    data = {
        'labels': [site[0] for site in sites],
        'data': [site[1] for site in sites]
    }
    return JsonResponse(data)