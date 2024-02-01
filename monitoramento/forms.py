from django import forms
from django.contrib.auth import get_user_model
from .models import Empresa, Representante, Setores, Funcionario, Expediente, BlackListSite, BlackListApp, Atividades

Representante = get_user_model()


class Cadastro_representante(forms.ModelForm):
    razao_social = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nome_fantasia = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cnpj = forms.CharField(max_length=18, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id':'cnpj'}))
    ramo = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    nome_representante = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sobrenome_representante = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf_representante = forms.CharField(
        max_length=14, widget=forms.TextInput(attrs={'class': 'form-control cpf', }))
    cargo_representante = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_nascimento_representante = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'email'}))
    password1 = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    password2 = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    telefone_representante = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={'class': 'form-control telefone'}))

    class Meta:
        model = Representante
        fields = ['razao_social', 'nome_fantasia', 'cnpj', 'ramo', 'nome_representante', 'sobrenome_representante', 'cpf_representante',
                  'cargo_representante', 'data_nascimento_representante', 'email', 'password1', 'password2', 'telefone_representante']

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Definir o email como o nome de usuário
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class Login(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'email'}))
    senha = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))


class Cadastro_setores(forms.Form):
    nome_setor = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descricao_setor = forms.CharField(
        max_length=100, widget=forms.Textarea(attrs={'class': 'form-control'}))
    ativo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    

    class Meta:
        model = Setores
        fields = ['nome_setor', 'descricao_setor']


class Cadastro_expediente(forms.Form):
    dias_da_semana = forms.MultipleChoiceField(
        choices=Expediente.DIAS_DA_SEMANA,
        widget=forms.CheckboxSelectMultiple
    )

    descricao = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    entrada_1 = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control hora', 'type': 'time'}))
    saida_1 = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control hora', 'type': 'time'}))
    entrada_2 = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control hora', 'type': 'time'}))
    saida_2 = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control hora', 'type': 'time'}))

    class Meta:
        model = Expediente
        fields = ['dias_da_semana', 'entrada_1',
                  'saida_1', 'entrada_2', 'saida_2']


class HorarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.descricao_expediente


class Cadastro_funcionario(forms.Form):
    matricula_funcionario = forms.CharField(
        max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nome_funcionario = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sobrenome_funcionario = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf_funcionario = forms.CharField(
        max_length=14, widget=forms.TextInput(attrs={'class': 'form-control cpf'}))
    cargo_funcionario = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nome_setor = forms.ModelChoiceField(queryset=Setores.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control setor'}))
    horario = HorarioChoiceField(queryset=Expediente.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control hora'}))
    data_nascimento_funcionario = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control data', 'type': 'date'}))
    email_funcionario = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'email'}))
    senha_funcionario = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    confirmar_senha_funcionario = forms.CharField(max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    telefone_funcionario = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={'class': 'form-control telefone'}))
    avatar = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class':'form-control-file'}), required=False)
    ferias = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    ativo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean_confirmar_senha_funcionario(self):
        senha = self.cleaned_data['senha_funcionario']
        confirmar_senha = self.cleaned_data['confirmar_senha_funcionario']
        if senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem.')
        return confirmar_senha

    class Meta:
        model = Funcionario
        fields = ['matricula_funcionario', 'nome_funcionario', 'sobrenome_funcionario', 'cpf_funcionario', 'cargo_funcionario', 'data_nascimento_funcionario', 'email_funcionario',
                  'senha_funcionario', 'confirmar_senha_funcionario', 'telefone_funcionario', 'avatar', 'nome_setor', 'horario']

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super(Cadastro_funcionario, self).__init__(*args, **kwargs)
        if empresa is not None:
            self.fields['nome_setor'].queryset = Setores.objects.filter(empresa=empresa)
            self.fields['horario'].queryset = Expediente.objects.filter(empresa=empresa)

class Cadastro_blacklistSite(forms.Form):
    nome_site = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    model = BlackListSite
    fields = ['nome_site', 'url']


class Cadastro_blacklistApp(forms.Form):
    nome_app = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    executavel = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    model = BlackListApp
    fields = ['nome_app', 'executavel']


class FuncionarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome_funcionario}  {obj.sobrenome_funcionario}"


class Cadastro_atividade(forms.Form):
    nome_atividade = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    descricao_atividade = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    funcionario = FuncionarioChoiceField(queryset=Funcionario.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control func'}))

    tempo_entrega = forms.TimeField(widget=forms.TextInput(
        attrs={'class': 'form-control hora', 'type': 'time'}))

    class Meta:
        model = Atividades
        fields = ['nome_atividade', 'descricao_atividade', 'funcionario', 'tempo_entrega']
        
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super(Cadastro_atividade, self).__init__(*args, **kwargs)
        if empresa is not None:
            self.fields['funcionario'].queryset = Funcionario.objects.filter(empresa=empresa)
