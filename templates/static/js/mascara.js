$(document).ready(function(){
  $('.telefone').mask('(00) 00000-0000');
  $('.cpf').mask('000.000.000-00', {reverse: true});
  $('#cnpj').mask('00.000.000/0000-00', {reverse: true});
});

