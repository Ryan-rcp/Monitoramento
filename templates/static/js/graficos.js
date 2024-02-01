$(document).ready(function () {
    appsOnline_acessados(urlAppOnline);
    siteOnline_acessados(urlSiteOnline);
    site_acessados(urlSite);
    apps_acessados(urlApp);
    registros_ponto(urlPonto);
    horas_extras(urlExtra);
    horas_pendentes(urlPendente);
    tempo_inatividade(urlInatividade);
    previsao(urlPrevisao)
    rendimento(urlRendimento)
    agendado(urlAgendado)
});

function atualizarGrafico() {
    const dataInicial = document.getElementById('data-inicial').value;
    const dataFinal = document.getElementById('data-final').value;
    const urlSiteFiltrada = `${urlSite}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    site_acessados(urlSiteFiltrada);
    const urlAppFiltrada = `${urlApp}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    apps_acessados(urlAppFiltrada);
    const urlPontoFiltrada = `${urlPonto}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    registros_ponto(urlPontoFiltrada);
    const urlExtrasFiltrada = `${urlExtra}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    horas_extras(urlExtrasFiltrada);
    const urlPendenteFiltrada = `${urlPendente}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    horas_pendentes(urlPendenteFiltrada);
    const urlInatividadeFiltrada = `${urlInatividade}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    tempo_inatividade(urlInatividadeFiltrada);
    const urlPrevisaoFiltrada = `${urlPrevisao}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    previsao(urlPrevisaoFiltrada);
    const urlRendimentoFiltrada = `${urlRendimento}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    rendimento(urlRendimentoFiltrada);
    const urlAgendadoFiltrada = `${urlAgendado}?data_inicial=${dataInicial}&data_final=${dataFinal}`;
    agendado(urlAgendadoFiltrada);

}

function gera_cor(qtd = 1) {
    var bg_color = []
    var border_color = []
    for (let i = 0; i < qtd; i++) {
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.8})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }

    return [bg_color, border_color]
}

var appOnlineChart;
function appsOnline_acessados(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('appsonline').getContext('2d');
        if (appOnlineChart) {
            appOnlineChart.destroy();
        }
        var corOn_app = gera_cor(qtd = 10)
        appOnlineChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Tempo de Execução',
                    data: data.data,
                    backgroundColor: corOn_app[0],
                    borderColor: corOn_app[1],
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        // Defina um rótulo personalizado para o eixo Y, se desejar
                        title: {
                            display: true,
                            text: 'Tempo'
                        },
                        // Defina o formato do rótulo do eixo Y para exibir horas, minutos e segundos
                        ticks: {
                            callback: function (value, index, values) {
                                // Função para formatar os valores em horas, minutos e segundos
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks:{
                            label: function(tooltipItem) {
                                const value = tooltipItem.raw;
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    },
                    legend:{
                        position: 'right'
                    }
                },
            }
        });
    })
}

var siteOnlineChart;
function siteOnline_acessados(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('sitesonline').getContext('2d');
        if (siteOnlineChart) {
            siteOnlineChart.destroy();
        }
        var corOn_site = gera_cor(qtd = 10)
        siteOnlineChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Acessos',
                    data: data.data,
                    backgroundColor: corOn_site[0],
                    borderColor: corOn_site[1],
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend:{
                        position: 'right'
                    }
                }
            }
        });
    })

}

var siteChart;
function site_acessados(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('sites').getContext('2d');
        if (siteChart) {
            siteChart.destroy();
        }
        var cor_site = gera_cor(qtd = 10)
        siteChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Acessos',
                    data: data.data,
                    backgroundColor: cor_site[0],
                    borderColor: cor_site[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })

}

var appChart;
function apps_acessados(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('apps').getContext('2d');
        if (appChart) {
            appChart.destroy();
        }
        var cor_app = gera_cor(qtd = 10)
        appChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Tempo de Execução',
                    data: data.data,
                    backgroundColor: cor_app[0],
                    borderColor: cor_app[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        // Defina um rótulo personalizado para o eixo Y, se desejar
                        title: {
                            display: true,
                            text: 'Tempo'
                        },
                        // Defina o formato do rótulo do eixo Y para exibir horas, minutos e segundos
                        ticks: {
                            callback: function (value, index, values) {
                                // Função para formatar os valores em horas, minutos e segundos
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    }
                }
            }
        });
    })
}

var pontoChart;
function registros_ponto(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('horas_trabalhadas').getContext('2d');
        if (pontoChart) {
            pontoChart.destroy();
        }

        const formattedLabels = data.labels.map(function (dateStr) {
            const dateParts = dateStr.split('-');
            return dateParts[2] + '/' + dateParts[1] + '/' + dateParts[0];
        });
        var cor_pontos = gera_cor(qtd = 10)
        pontoChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: formattedLabels,
                datasets: [{
                    label: 'Horas Trabalhadas',
                    data: data.data, // Valores em segundos
                    backgroundColor: cor_pontos[0],
                    borderColor: cor_pontos[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        // Defina um rótulo personalizado para o eixo Y, se desejar
                        title: {
                            display: true,
                            text: 'Tempo'
                        },
                        // Defina o formato do rótulo do eixo Y para exibir horas, minutos e segundos
                        ticks: {
                            callback: function (value, index, values) {
                                // Função para formatar os valores em horas, minutos e segundos
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    }
                }
            }
        });
        
    })
}

var extrasChart;
function horas_extras(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('horas_extras').getContext('2d');
        if (extrasChart) {
            extrasChart.destroy();
        }

        const formattedLabels = data.labels.map(function (dateStr) {
            const dateParts = dateStr.split('-');
            return dateParts[2] + '/' + dateParts[1] + '/' + dateParts[0];
        });
        var cor_extras = gera_cor(qtd = 10)
        extrasChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedLabels,
                datasets: [{
                    label: 'Horas Extras',
                    data: data.data, // Valores em segundos
                    backgroundColor: cor_extras[0],
                    borderColor: cor_extras[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        // Defina um rótulo personalizado para o eixo Y, se desejar
                        title: {
                            display: true,
                            text: 'Tempo'
                        },
                        // Defina o formato do rótulo do eixo Y para exibir horas, minutos e segundos
                        ticks: {
                            callback: function (value, index, values) {
                                // Função para formatar os valores em horas, minutos e segundos
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    }
                }
            }
        });
        
    })

}

var pendentesChart;
function horas_pendentes(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('horas_pendentes').getContext('2d');
        if (pendentesChart) {
            pendentesChart.destroy();
        }

        const formattedLabels = data.labels.map(function (dateStr) {
            const dateParts = dateStr.split('-');
            return dateParts[2] + '/' + dateParts[1] + '/' + dateParts[0];
        });
        var cor_pendente = gera_cor(qtd = 10)
        pendentesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedLabels,
                datasets: [{
                    label: 'Horas Pendentes',
                    data: data.data, // Valores em segundos
                    backgroundColor: cor_pendente[0],
                    borderColor: cor_pendente[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        // Defina um rótulo personalizado para o eixo Y, se desejar
                        title: {
                            display: true,
                            text: 'Tempo'
                        },
                        // Defina o formato do rótulo do eixo Y para exibir horas, minutos e segundos
                        ticks: {
                            callback: function (value, index, values) {
                                // Função para formatar os valores em horas, minutos e segundos
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    }
                }
            }
        });
        
    })

}

function formatarHoraSegundos(segundos) {
    const hours = Math.floor(segundos / 3600);
    const minutes = Math.floor((segundos % 3600) / 60);
    const secondsRestantes = segundos % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secondsRestantes.toString().padStart(2, '0')}`;
}

var inativoChart;
function tempo_inatividade(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('tempo_inativo').getContext('2d');
        if (inativoChart) {
            inativoChart.destroy();
        }

        const formattedLabels = data.labels.map(function (hourStr) {
            const segundos = parseInt(hourStr);
            return formatarHoraSegundos(segundos);
        });
        var cor_inativo = gera_cor(qtd = 10)
        inativoChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedLabels,  // Horas formatadas no formato "hh:mm:ss"
                datasets: [{
                    label: 'Tempo Inativo',
                    data: data.data,         // Valores em segundos
                    backgroundColor: cor_inativo[0],
                    borderColor: cor_inativo[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        // Defina um rótulo personalizado para o eixo Y, se desejar
                        title: {
                            display: true,
                            text: 'Tempo'
                        },
                        // Defina o formato do rótulo do eixo Y para exibir horas, minutos e segundos
                        ticks: {
                            callback: function (value, index, values) {
                                // Função para formatar os valores em horas, minutos e segundos
                                const hours = Math.floor(value / 3600);
                                const minutes = Math.floor((value % 3600) / 60);
                                const seconds = value % 60;
                                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                            }
                        }
                    }
                }
            }
        });
        
    })

}

var PrevisaoChart;
function previsao(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('previsao').getContext('2d');
        if (PrevisaoChart) {
            PrevisaoChart.destroy();
        }
        var cor_previsao = gera_cor(qtd = 10)
        PrevisaoChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Setor',
                        data: data.data1,
                        backgroundColor: cor_previsao[0],
                        borderColor: cor_previsao[0],
                        borderWidth: 1
                    },
                    {
                        label: 'Funcionário',
                        data: data.data2,
                        backgroundColor: cor_previsao[1],
                        borderColor: cor_previsao[1],
                        borderWidth: 1
                    },
            ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })

}

var RendimentoChart;
function rendimento(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('rendimento').getContext('2d');
        if (RendimentoChart) {
            RendimentoChart.destroy();
        }
        var cor_rendimento = gera_cor(qtd = 10)
        RendimentoChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Rendimento',
                        data: data.data,
                        backgroundColor: cor_rendimento[0],
                        borderColor: cor_rendimento[1],
                        borderWidth: 1
                    }
            ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })

}


var AgendadoChart;
function agendado(url) {
    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        const ctx = document.getElementById('agendada').getContext('2d');
        if (AgendadoChart) {
            AgendadoChart.destroy();
        }
        var cor_agendado = gera_cor(qtd = 10)
        AgendadoChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Atividade Agendada',
                        data: data.data,
                        backgroundColor: cor_agendado[0],
                        borderColor: cor_agendado[1],
                        borderWidth: 1
                    }
            ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })

}


