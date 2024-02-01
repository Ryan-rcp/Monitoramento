///////////////// DATA TABLES ////////////////////
$(document).ready(function () {
    $("#tabela-listar-funcionario").DataTable({
    "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });
   
    $("#tabela-listar-setor").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });
    $("#tabela-listar-expediente").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });
    $("#tabela-listar-acessos").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });
    $("#tabela-listar-pontos").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });
    $("#tabela-listar-atividades").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        "order": [[2, 'asc']]
    });

    $("#tabela-online").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableOnline,
            dataSrc: ''
        },
        columns: [
            { data: 'matricula_funcionario' },
            { data: 'nome_funcionario' },
            {
                data: 'online',
                render: function (data, type, row) {
                    if (type == 'display') {
                        return '<i class="bx bxs-circle" style="color: #15ff00;;"></i>';
                    }
                    return data;
                }
            },
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });

    $("#tabela-offline").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableOffline,
            dataSrc: ''
        },
        columns: [
            { data: 'matricula_funcionario' },
            { data: 'nome_funcionario' },
            {
                data: 'online',
                render: function (data, type, row) {
                    if (type == 'display') {
                        return '<i class="bx bxs-circle" style="color: #ff0000;;"></i>';
                    }
                    return data;
                }
            },
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });

    $('#tabela-acesso-site').DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableSite,
            dataSrc: ''
        },
        columns: [
            { data: 'data_visita' },
            { data: 'nome_site' },
            {
                data: 'url',
                render: function (data, type, row) {
                    if (type === 'display') {
                        if (data.length > 30) {
                            return '<a href="' + data + '" target="_blank"><span title="' + data + '">' + data.substr(0, 30) + '...</span></a>';
                        } else {
                            return '<a href="' + data + '" target="_blank">' + data + '</a>';
                        }
                    } else {
                        return data;
                    }
                }
            },
            { data: 'horario_visita' },
            {
                data: 'blacklistsite',
                render: function (data, type, row) {
                    if (type == 'display') {
                        if (data == 1) {
                            return '<i class="bx bx-x" style="color: #ff0000;"></i>';
                        } else {
                            return '<i class="bx bx-check" style="color: #15ff00;"></i>';
                        }
                    }
                    return data;
                }
            }
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger',
                customize: function (doc) {
                    var bodyData = doc.content[1].table.body;
                    bodyData.forEach(function (data, i) {
                        if (i !== 0) { // Ignorando o cabeçalho da tabela
                            data[3] = data[3] == 1 ? 'Negado' : 'Permitido';
                        }
                    });

                }
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]

    });

    $('#tabela-acesso-aplicativo').DataTable({
        destroy: true,
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableApp,
            dataSrc: ''
        },
        columns: [
            { data: 'data_execucao' },
            { data: 'nome_app' },
            { data: 'horario_execucao' },
            { data: 'tempo_execucao' },
            { data: 'tempo_execucaoExp' },
            {
                data: 'blacklistapp',
                render: function (data, type, row) {
                    if (type == 'display') {
                        if (data == 1) {
                            return '<i class="bx bx-x" style="color: #ff0000;"></i>';
                        } else {
                            return '<i class="bx bx-check" style="color: #15ff00;"></i>';
                        }
                    }
                    return data;
                }
            }
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger',
                customize: function (doc) {
                    var bodyData = doc.content[1].table.body;
                    bodyData.forEach(function (data, i) {
                        if (i !== 0) { // Ignorando o cabeçalho da tabela
                            data[5] = data[5] == 1 ? 'Acesso negado' : 'Acesso Permitido';
                        }
                    });
                }
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]
    });

    $('#tabela-blacklist-site').DataTable({
        destroy: true,
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableBLSite,
            dataSrc: ''
        },
        columns: [
            { data: 'nome_site' },
            { data: 'url' },
            {
                data: null,
                render: function (data, type, row) {
                    return '<a href="/excluir_blacklistsite/' + row.id + '/" class="btn btn-danger btn-sm btn-excluir-site" title="Excluir" data-id="' + row.id + '" data-excluir-url="/excluir_blacklistsite/' + row.id + '/"><i class=\'bx bx-trash\'></i></a>';
                }
            }
        ],
        columnDefs: [
            { width: '20%', targets: 0 },
            { width: '60%', targets: 1 },
            { width: '20%', targets: 2 }
        ],
        initComplete: function () {
            const btnsExcluir = document.querySelectorAll('.btn-excluir-site');

            btnsExcluir.forEach(btn => {
                btn.addEventListener('click', function (event) {
                    event.preventDefault();
                    const id = this.getAttribute('data-id');
                    const excluirUrl = this.getAttribute('data-excluir-url');
                    let mensagem;
                    if (document.querySelector('#tabela-blacklist-site')) {
                        mensagem = "Tem certeza que deseja excluir este site?";
                    }
                    if (confirm(mensagem)) {
                        window.location.href = excluirUrl;
                    }
                });
            });
        },
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });

    $('#tabela-blacklist-app').DataTable({
        destroy: true,
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableBLApp,
            dataSrc: ''
        },
        columns: [
            { data: 'nome_app' },
            { data: 'executavel' },
            {
                data: null,
                render: function (data, type, row) {
                    return '<a href="/excluir_blacklistapp/' + row.id + '/" class="btn btn-danger btn-sm btn-excluir-app" title="Excluir" data-id="' + row.id + '" data-excluir-url="/excluir_blacklistapp/' + row.id + '/"><i class=\'bx bx-trash\'></i></a>';
                }
            }
        ],
        columnDefs: [
            { width: '20%', targets: 0 },
            { width: '60%', targets: 1 },
            { width: '20%', targets: 2 }
        ],
        initComplete: function () {
            const btnsExcluir = document.querySelectorAll('.btn-excluir-app');

            btnsExcluir.forEach(btn => {
                btn.addEventListener('click', function (event) {
                    event.preventDefault();
                    const id = this.getAttribute('data-id');
                    const excluirUrl = this.getAttribute('data-excluir-url');
                    let mensagem;
                    if (document.querySelector('#tabela-blacklist-app')) {
                        mensagem = "Tem certeza que deseja excluir este app?";
                    }
                    if (confirm(mensagem)) {
                        window.location.href = excluirUrl;
                    }
                });
            });
        },
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });


    /*  $("#tabela-registro-ponto").DataTable({
         destroy: true, // Destruir a tabela existente, se houver
         "scrollX": true,
         "scrollCollapse": true,
         responsive: true,
         ajax: {
             url: urlTablePonto,
             dataSrc: ''
         },
         columns: [
             { data: 'data_ponto' },
             { data: 'horario_entrada_manha' },
             { data: 'horario_saida_manha' },
             { data: 'horario_entrada_tarde' },
             { data: 'horario_saida_tarde' },
             { data: 'horas_trabalhadas' },
             { data: 'horas_extra' },
             { data: 'horas_falta' },
         ],
     }); */

    $("#tabela-registro-ponto").DataTable({
        destroy: true,
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTablePonto,
            dataSrc: ''
        },
        columns: [
            { data: 'data_ponto' },
            { data: 'horario_entrada_manha' },
            { data: 'horario_saida_manha' },
            { data: 'horario_entrada_tarde' },
            { data: 'horario_saida_tarde' },
            { data: 'horas_trabalhadas' },
            { data: 'horas_extra' },
            { data: 'horas_falta' },
        ],
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            // Converter horas:minutos:segundos para segundos
            var intVal = function (i) {
                if (typeof i === 'string') {
                    var array = i.split(':');
                    return array[0] * 3600 + array[1] * 60 + array[2] * 1;
                }
                return typeof i === 'number' ? i : 0;
            };

            // Converter segundos para horas:minutos:segundos
            var secToTime = function (i) {
                var hours = Math.floor(i / 3600);
                var minutes = Math.floor((i % 3600) / 60);
                var seconds = i % 60;
                return hours + ':' + minutes + ':' + seconds;
            };

            totalHorasTrabalhadas = api
                .column(5)
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Horas Extras
            totalHorasExtras = api
                .column(6)
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Horas Pendentes
            totalHorasPendentes = api
                .column(7)
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Atualizar o rodapé
            $(api.column(5).footer()).html(secToTime(totalHorasTrabalhadas));
            $(api.column(6).footer()).html(secToTime(totalHorasExtras));
            $(api.column(7).footer()).html(secToTime(totalHorasPendentes));
        },
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger'
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]
    });


    $("#tabela-inatividade").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableInativo,
            dataSrc: ''
        },
        columns: [
            { data: 'data_inativo' },
            { data: 'hora_inativo' },
            { data: 'tempo_inativo' },
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger'
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]
    });

    $("#tabela-rendimento").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableRendimento,
            dataSrc: ''
        },
        columns: [
            { data: 'data_conclusao' },
            { data: 'previsao' },
            { data: 'rendimento' },
        ],
        "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
            }
        });

    $("#tabela-atv-concluida").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableConcluido,
            dataSrc: ''
        },
        columns: [
            { data: 'data_atividade' },
            { data: 'nome_atividade' },
            { data: 'tempo_entrega' },
            {data:  'horaTotal',
            render: function (data) {
                // Converte os segundos para hh:mm:ss
                var hours = Math.floor(data / 3600);
                var minutes = Math.floor((data % 3600) / 60);
                var seconds = data % 60;
                return (hours < 10 ? '0' : '') + hours + ':' +
                    (minutes < 10 ? '0' : '') + minutes + ':' +
                    (seconds < 10 ? '0' : '') + seconds;
            }},
            { data: 'status' },
        ],
        "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
            }
        });

    $("#tabela-atv-agendada").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlTableAgendado,
            dataSrc: ''
        },
        columns: [
            { data: 'data_atividade' },
            { data: 'nome_atividade' },
            { data: 'status_atividade' },
            { data: 'previsao' },
        ],
        "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
            }
        });

});



function atualizarTabela() {
    const dataInicial = document.getElementById('data-inicial').value;
    const dataFinal = document.getElementById('data-final').value;
    const urlSiteFiltrada = `${urlTableSite}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    const urlAppFiltrada = `${urlTableApp}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    const urlpontoFiltrada = `${urlTablePonto}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    const urlinatividadeFiltrada = `${urlTableInativo}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    const urlRendimentoFiltrada = `${urlTableRendimento}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    const urlConcluidoFiltrada = `${urlTableConcluido}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    const urlAgendadoFiltrada = `${urlTableAgendado}?data_inicial=${dataInicial}&data_final=${dataFinal}`;

    $('#tabela-acesso-site').DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlSiteFiltrada,
            dataSrc: ''
        },
        columns: [
            { data: 'data_visita' },
            { data: 'nome_site' },
            {
                data: 'url',
                render: function (data, type, row) {
                    if (type === 'display') {
                        if (data.length > 30) {
                            return '<a href="' + data + '" target="_blank"><span title="' + data + '">' + data.substr(0, 30) + '...</span></a>';
                        } else {
                            return '<a href="' + data + '" target="_blank">' + data + '</a>';
                        }
                    } else {
                        return data;
                    }
                }
            },
            { data: 'horario_visita' },
            {
                data: 'blacklistsite',
                render: function (data, type, row) {
                    if (type == 'display') {
                        if (data == 1) {
                            return '<i class="bx bx-x" style="color: #ff0000;"></i>';
                        } else {
                            return '<i class="bx bx-check" style="color: #15ff00;"></i>';
                        }
                    }
                    return data;
                }
            }

        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger',
                customize: function (doc) {
                    var bodyData = doc.content[1].table.body;
                    bodyData.forEach(function (data, i) {
                        if (i !== 0) { // Ignorando o cabeçalho da tabela
                            data[4] = data[4] == 1 ? 'Negado' : 'Permitido';
                        }
                    });

                }
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]

    });
    var minhaImagemBase64 = 'data:image/png;base64,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';
    $('#tabela-acesso-aplicativo').DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlAppFiltrada,
            dataSrc: ''
        },
        columns: [
            { data: 'data_execucao' },
            { data: 'nome_app' },
            { data: 'horario_execucao' },
            { data: 'tempo_execucao' },
            { data: 'tempo_execucaoExp' },
            {
                data: 'blacklistapp',
                render: function (data, type, row) {
                    if (type == 'display') {
                        if (data == 1) {
                            return '<i class="bx bx-x" style="color: #ff0000;"></i>';
                        } else {
                            return '<i class="bx bx-check" style="color: #15ff00;"></i>';
                        }
                    }
                    return data;
                }
            }
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger',
                customize: function (doc) {
                    var bodyData = doc.content[1].table.body;
                    bodyData.forEach(function (data, i) {
                        if (i !== 0) { // Ignorando o cabeçalho da tabela
                            data[5] = data[5] == 1 ? 'Negado' : 'Permitido';
                        }
                    });

                }
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]

    });

    $("#tabela-registro-ponto").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlpontoFiltrada,
            dataSrc: ''
        },
        columns: [
            { data: 'data_ponto' },
            { data: 'horario_entrada_manha' },
            { data: 'horario_saida_manha' },
            { data: 'horario_entrada_tarde' },
            { data: 'horario_saida_tarde' },
            { data: 'horas_trabalhadas' },
            { data: 'horas_extra' },
            { data: 'horas_falta' },
        ],
        "footerCallback": function (row, data, start, end, display) {
            var api = this.api(), data;

            // Converter horas:minutos:segundos para segundos
            var intVal = function (i) {
                if (typeof i === 'string') {
                    var array = i.split(':');
                    return array[0] * 3600 + array[1] * 60 + array[2] * 1;
                }
                return typeof i === 'number' ? i : 0;
            };

            // Converter segundos para horas:minutos:segundos
            var secToTime = function (i) {
                var hours = Math.floor(i / 3600);
                var minutes = Math.floor((i % 3600) / 60);
                var seconds = i % 60;
                return hours + ':' + minutes + ':' + seconds;
            };

            totalHorasTrabalhadas = api
                .column(5)
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Horas Extras
            totalHorasExtras = api
                .column(6)
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Horas Pendentes
            totalHorasPendentes = api
                .column(7)
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Atualizar o rodapé
            $(api.column(5).footer()).html(secToTime(totalHorasTrabalhadas));
            $(api.column(6).footer()).html(secToTime(totalHorasExtras));
            $(api.column(7).footer()).html(secToTime(totalHorasPendentes));
        },
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i>',
                titleAttr: 'Exportar para Excel',
                className: 'btn btn-success'
            },

            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i>',
                titleAttr: 'Exportar para pdf',
                className: 'btn btn-danger'
            },

            {
                extend: 'print',
                text: '<i class="fas fa-print"></i>',
                titleAttr: 'Imprimir',
                className: 'btn btn-info'
            },

        ]

    });

    $("#tabela-inatividade").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlinatividadeFiltrada,
            dataSrc: ''
        },
        columns: [
            { data: 'data_inativo' },
            { data: 'hora_inativo' },
            { data: 'tempo_inativo' },
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
        }
    });

    $("#tabela-rendimento").DataTable({
        destroy: true, // Destruir a tabela existente, se houver
        "scrollX": true,
        "scrollCollapse": true,
        responsive: true,
        ajax: {
            url: urlRendimentoFiltrada,
            dataSrc: ''
        },
        columns: [
            { data: 'data_conclusao' },
            { data: 'rendimento' },
            { data: 'previsao' },
        ],
        "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
            }
        });

        $("#tabela-atv-concluida").DataTable({
            destroy: true, // Destruir a tabela existente, se houver
            "scrollX": true,
            "scrollCollapse": true,
            responsive: true,
            ajax: {
                url: urlConcluidoFiltrada,
                dataSrc: ''
            },
            columns: [
                { data: 'data_atividade' },
                { data: 'nome_atividade' },
                { data: 'tempo_entrega' },
                {data:  'horaTotal',
            render: function (data) {
                // Converte os segundos para hh:mm:ss
                var hours = Math.floor(data / 3600);
                var minutes = Math.floor((data % 3600) / 60);
                var seconds = data % 60;
                return (hours < 10 ? '0' : '') + hours + ':' +
                    (minutes < 10 ? '0' : '') + minutes + ':' +
                    (seconds < 10 ? '0' : '') + seconds;
            }},
                { data: 'status' },
            ],
            "language": {
                    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
                }
            });

            $("#tabela-atv-agendada").DataTable({
                destroy: true, // Destruir a tabela existente, se houver
                "scrollX": true,
                "scrollCollapse": true,
                responsive: true,
                ajax: {
                    url: urlAgendadoFiltrada,
                    dataSrc: ''
                },
                columns: [
                    { data: 'data_atividade' },
                    { data: 'nome_atividade' },
                    { data: 'status_atividade' },
                    { data: 'previsao' },
                ],
                "language": {
                        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
                    }
                });
}
