// urls.js

const urls = {
    urlSite: "{% url 'grf_acesso_site' funcionario.id %}",
    urlApp: "{% url 'grf_acesso_aplicativo' funcionario.id %}",
    urlPonto: "{% url 'grf_registro_ponto' funcionario.id %}",
    urlExtra: "{% url 'grf_horas_extras' funcionario.id %}",
    urlPendente: "{% url 'grf_horas_pendentes' funcionario.id %}",
    urlInatividade: "{% url 'grf_inatividade' funcionario.id %}",
    urlTableSite: "{% url 'tbl_acesso_site' funcionario.id %}",
    urlTableApp: "{% url 'tbl_acesso_aplicativo' funcionario.id %}",
    urlTablePonto: "{% url 'tbl_registro_ponto' funcionario.id %}",
    urlTableInativo: "{% url 'tbl_inatividade' funcionario.id %}"
  };
  
  export default urls;
  