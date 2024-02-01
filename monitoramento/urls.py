from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('cadastro_representante/', views.cadastro_representante,
         name="cadastro_representante"),
    path('principal/', views.principal, name="principal"),

    # ###########  LISTAS ###############
    path('cadastros/usuarios', views.lista_funcionarios, name="lista_funcionarios"),
    path('cadastros/setores', views.lista_setores, name="lista_setores"),
    path('cadastros/expediente', views.lista_expediente, name="lista_expediente"),
    path('cadastros/atividades', views.lista_atividade, name="lista_atividade"),
    path('analise/acessos', views.lista_acessos, name="lista_acessos"),
    path('analise/acessos/visualizar/<int:funcionario_id>/',
         views.acessos_funcionario, name="acessos_funcionario"),
    path('analise/produtividade', views.lista_produtividade, name="lista_produtividade"),
    path('analise/produtividade/visualizar/<int:funcionario_id>/',
         views.produtividade_funcionario, name="produtividade_funcionario"),
    path('analise/registros', views.lista_pontos, name="lista_pontos"),
    path('analise/registros/visualizar/<int:funcionario_id>/',
         views.pontos_funcionario, name="pontos_funcionario"),


    # ########### CADASTROS ###############
    path('cadastros/usuarios/cadastro',
         views.cadastro_funcionarios, name="cadastro_funcionarios"),
    path('cadastros/setores/cadastro',
         views.cadastro_setor, name="cadastro_setor"),
    path('cadastros/expediente/cadastro',
         views.cadastro_expediente, name="cadastro_expediente"),
    path('cadastros/atividades/cadastro',
         views.cadastro_atividade, name="cadastro_atividade"),
   

    # ###########  EDIÇÕES ###############
    path('cadastros/usuarios/editar/<int:funcionario_id>/',
         views.editar_funcionario, name="editar_funcionario"),
    path('cadastros/setores/editar/<int:setor_id>/',
         views.editar_setor, name="editar_setor"),
    path('cadastros/expediente/editar/<int:expediente_id>/',
         views.editar_expediente, name="editar_expediente"),
    path('cadastros/atividade/editar/<int:atividade_id>/',
         views.editar_atividade, name="editar_atividade"),
    path('configuracoes/editar_representante',
         views.editar_representante, name="editar_representante"),

    # ###########  EXCLUSÕES ###############
    path('usuarios/excluir/<int:funcionario_id>/',
         views.excluir_funcionario, name="excluir_funcionario"),
    path('setores/excluir/<int:setor_id>/',
         views.excluir_setor, name="excluir_setor"),
    path('expediente/excluir/<int:expediente_id>/',
         views.excluir_expediente, name="excluir_expediente"),
    path('atividade/excluir/<int:atividade_id>/',
         views.excluir_atividade, name="excluir_atividade"),
    


    
    path('logout/', views.logout_view, name='logout'),

    # ########### GRÁFICOS ###############
    path('grf_acesso_site/<int:funcionario_id>/',
         views.grf_acesso_site, name="grf_acesso_site"),
    path('grf_acesso_aplicativo/<int:funcionario_id>/',
         views.grf_acesso_aplicativo, name="grf_acesso_aplicativo"),
    path('grf_registro_ponto/<int:funcionario_id>/',
         views.grf_registro_ponto, name="grf_registro_ponto"),
    path('grf_horas_extras/<int:funcionario_id>/',
         views.grf_horas_extras, name="grf_horas_extras"),
    path('grf_horas_pendentes/<int:funcionario_id>/',
         views.grf_horas_pendentes, name="grf_horas_pendentes"),
    path('grf_inatividade/<int:funcionario_id>/',
         views.grf_inatividade, name="grf_inatividade"),
    path('grf_previsao/<int:funcionario_id>/',
         views.grf_previsao, name="grf_previsao"),
    path('grf_rendimento/<int:funcionario_id>/',
         views.grf_rendimento, name="grf_rendimento"),
    path('grf_agendado/<int:funcionario_id>/',
         views.grf_agendado, name="grf_agendado"),
    path('grf_app_online/',
         views.grf_aplicativo_online, name="grf_aplicativo_online"),
    path('grf_site_online/',
         views.grf_site_online, name="grf_site_online"),

    # ###########  TABELAS ###############
    path('tbl_acesso_site/<int:funcionario_id>/',
         views.tbl_acesso_site, name="tbl_acesso_site"),
    path('tbl_acesso_app/<int:funcionario_id>/',
         views.tbl_acesso_aplicativo, name="tbl_acesso_aplicativo"),
    path('tbl_registro_ponto/<int:funcionario_id>/',
         views.tbl_registro_ponto, name="tbl_registro_ponto"),
    path('tbl_inatividade/<int:funcionario_id>/',
         views.tbl_inatividade, name="tbl_inatividade"),
    path('tbl_rendimento/<int:funcionario_id>/',
         views.tbl_rendimento, name="tbl_rendimento"),
    path('tbl_atv_concluida/<int:funcionario_id>/',
         views.tbl_atv_concluida, name="tbl_atv_concluida"),
    path('tbl_atv_agendada/<int:funcionario_id>/',
         views.tbl_atv_agendada, name="tbl_atv_agendada"),
    path('tbl_online/',
         views.tbl_func_online, name="tbl_func_online"),
    path('tbl_offline/',
         views.tbl_func_offline, name="tbl_func_offline"),
    
    

    
    
    
    
     path('analise/acessos/backlist/<int:funcionario_id>/',
         views.blackList, name="blackList"),
     path('tbl_blsite/<int:funcionario_id>/',
         views.tbl_blsite, name="tbl_blsite"),
     path('tbl_blapp/<int:funcionario_id>/',
         views.tbl_blapp, name="tbl_blapp"),
     path('excluir_blacklistsite/<int:blacklistsite_id>/', views.excluir_blacklistsite, name='excluir_blacklistsite'),
     path('excluir_blacklistapp/<int:blacklistapp_id>/', views.excluir_blacklistapp, name='excluir_blacklistapp'),

     ###################### ATIVAÇÃO DE CONTA ##################################
     path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
     
     #################### ESQUECI A SENHA ######################################
     path('esqueci_a_senha/', views.recuperar_senha, name="recuperar_senha"),
     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
     path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='nova_senha.html'), name='password_reset_confirm'),
     path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='confirmacao_senha.html'), name='password_reset_complete'),
]

