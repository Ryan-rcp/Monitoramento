const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");

// Verificar o estado armazenado no localStorage
const isDarkMode = localStorage.getItem("darkMode") === "true";

// Aplicar o modo escuro automaticamente se estiver ativado
if (isDarkMode) {
  body.classList.add("dark");
  darkLight.classList.replace("bx-sun", "bx-moon");
}

sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));

sidebarClose.addEventListener("click", () => {
  sidebar.classList.add("close", "hoverable");
});
sidebarExpand.addEventListener("click", () => {
  sidebar.classList.remove("close", "hoverable");
});

sidebar.addEventListener("mouseenter", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.remove("close");
  }
});
sidebar.addEventListener("mouseleave", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("close");
  }
});

darkLight.addEventListener("click", () => {
  body.classList.toggle("dark");

  // Armazenar o estado atual no localStorage
  localStorage.setItem("darkMode", body.classList.contains("dark"));

  if (body.classList.contains("dark")) {
    darkLight.classList.replace("bx-sun", "bx-moon");
  } else {
    darkLight.classList.replace("bx-moon", "bx-sun");
  }
});

submenuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    item.classList.toggle("show_submenu");
    submenuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show_submenu");
      }
    });
  });
});

if (window.innerWidth < 768) {
  sidebar.classList.add("close");
} else {
  sidebar.classList.remove("close");
}

document.addEventListener('DOMContentLoaded', function () {
  const btnsExcluir = document.querySelectorAll('.btn-excluir');

  btnsExcluir.forEach(btn => {
    btn.addEventListener('click', function (event) {
      event.preventDefault();
      const id = this.getAttribute('data-id');
      const excluirUrl = this.getAttribute('data-excluir-url');
      let mensagem;
      if (document.querySelector('#tabela-listar-funcionario')) {
        mensagem = "Tem certeza que deseja excluir este funcionário?";
      } else if (document.querySelector('#tabela-listar-setor')) {
        mensagem = "Tem certeza que deseja excluir este setor?";
      } else if (document.querySelector('#tabela-listar-expediente')) {
        mensagem = "Tem certeza que deseja excluir este horário?";
      }
      else if (document.querySelector('#tabela-listar-atividades')) {
        mensagem = "Tem certeza que deseja excluir esta atividade?";
      }
      if (confirm(mensagem)) {
        window.location.href = excluirUrl;
      }
    });
  });
});

document.querySelector('#id_avatar').addEventListener('change', function (event) {
  var reader = new FileReader();
  reader.onload = function (event) {
    document.querySelector('#avatar-preview').src = event.target.result;
    document.querySelector('#avatar-preview').style.display = 'block';
  }
  reader.readAsDataURL(event.target.files[0]);
});

function voltar() {
  var urlAnterior = document.referrer;
  var urlDoSite = window.location.origin;

  if (urlAnterior.indexOf(urlDoSite) === 0) {
    window.history.back();
  } else {
    window.location.href = urlPrincipal; // Use a variável global urlPrincipal
  }
}




