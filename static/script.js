function start_loading(table, tab2) {
  $("#overlay").fadeIn(300);
}

function stop_loading(table, tab2) {
  $("#overlay").fadeOut(300);
}

function gerar_tabela(cripto_data, table, previousPrice) {
  // console.log("gerar_tabela...", cripto_data);
  row = `
    <tr id="${cripto_data.Name}">
    <td>${cripto_data.Data}</td>
    <td>${cripto_data.Hora}</td>
    <td>${cripto_data.Label}</td>
    <td style="font-weight: bold; color:#03a9f4;text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.0);
    background: rgba(80, 80, 80, 0.1); border-radius: 30px; margin:1.5px;">${
      cripto_data.Name
    }</td>
    <td>${Number(cripto_data["Price"]).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    })}</td>
    <td id="variacao">${calcularVariacao(
      cripto_data["Price"],
      previousPrice
    )}</td>
    </tr>`;
  try {
    table.append(row);
    return true;
  } catch (err) {
    console.log(err);
    return false;
  }
}

function criar_cards(cripto_data) {
  console.log("criar_cards...");
  console.log(cripto_data);
  const valores_atuais = new Array();
  let tds = $(`#${cripto_data.Name}`).find("td");
  tds.each(function (index, element) {
    valores_atuais.push(element.textContent);
  });
  console.log("valores atuais:", valores_atuais);

  let cards = document.getElementById("cards");
  //console.log(cripto_data);
  let card = document.createElement("div");
  card.className = "max-w-xs mx-auto";
  card.innerHTML = `
      <div style="height: 8rem" class="shadow-md rounded-lg overflow-hidden bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 ">
          <div class="p-4" >
              <h5 class="text-xl font-semibold">${cripto_data["Name"]}</h5>
              <div id = "content_cards">
                <div>
                  <p class="p-alta" data-toggle="tooltip" data-placement="top"
                  title=${cripto_data["timestamp_max"]}>Alta:
                  ${Number(cripto_data["Maior"]).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}👍</p>  

                  <p class="p-baixa mt-2" data-toggle="tooltip" data-placement="top"
                  title=${cripto_data["timestamp_min"]}>Baixa:
                  ${Number(cripto_data["Menor"]).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}👎</p>                                      
                </div>     
                <div>
                  <p class="p-valor" data-toggle="tooltip" data-placement="top"
                  title=${cripto_data["timestamp_max"]}>
                  <b>${valores_atuais[4]} </b>
                  </p>
                </div>    
          </div>
      </div>
  `;
  cards.append(card);
}

function gerar_estatisticas(cripto_name) {
  fetch("/api/analise/" + cripto_name)
    .then((response) => response.json())
    .then((cripto_data) => {
      criar_cards(cripto_data);

      return true;
    });
}

function scroll() {
  $(".tab-content").on("wheel", function (event) {
    event.preventDefault(); // Impede a rolagem padrão da página

    var delta = event.originalEvent.deltaY; // Obtém a direção da rolagem

    if (delta > 0) {
      // Se estiver rolando para baixo, move a div para baixo
      $(this).stop().animate(
        {
          scrollTop: "+=50",
        },
        200
      );
    } else {
      // Se estiver rolando para cima, move a div para cima
      $(this).stop().animate(
        {
          scrollTop: "-=50",
        },
        200
      );
    }
  });
}

function drag() {
  var isDragging = false;
  var startY;
  var startX;

  $(document).on("mousedown", function (event) {
    isDragging = true;
    startY = event.clientY;
    startX = event.clientX;
  });

  $(document).on("mousemove", function (event) {
    if (isDragging) {
      var deltaY = event.clientY - startY;
      $("html, body").scrollTop($("html, body").scrollTop() - deltaY);
      startY = event.clientY; 
      var deltaX = event.clientX - startX;
      // $("html, body").scroollLeft($("html, body").scroollLeft() - deltaX);
      console.log(deltaX);
      startX = event.clientX;
    }
  });

  $(document).on("mouseup", function () {
    isDragging = false;
  });
}

function calcularVariacao(precoAtual, precoAnterior) {
  var _variacao = ((precoAtual - precoAnterior) / precoAnterior) * 100;

  vari = '<span class="text-danger">' + _variacao.toFixed(2) + "% " + "✅";
  if (_variacao < 0) {
    vari =
      '<span class="text-danger">' +
      _variacao.toFixed(2) +
      "% " +
      "🔻" +
      "</span>";
  } else if (_variacao > 0) {
    vari =
      '<span class="text-success">' +
      _variacao.toFixed(2) +
      "% " +
      '<span style="font-size: 20px;">⏫</span>' +
      "</span>";
  }
  return vari;
}

function atualizarTabela(tabela, tab2) {
  // Limpa a tabela
  tabela.empty();
  tab2.empty();
  start_loading(tabela, tab2);
  try {
    // Faz a chamada para a API de criptomoedas
    fetch("/api/criptomoedas")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao obter os dados da API");
        }

        return response.json();
      })
      .then((criptomoedas) => {
        console.log("Número de criptomoedas:", criptomoedas.length);

        if (criptomoedas.length > 0) {
          criptomoedas.forEach(function (criptomoeda) {
            let previousPrice =
              sessionStorage.getItem(criptomoeda["Name"]) || null;
            if (previousPrice === null || previousPrice === undefined) {
              previousPrice = criptomoeda["Price"];
              sessionStorage.setItem(criptomoeda["Name"], criptomoeda["Price"]);
            }
            let tabela_ok = gerar_tabela(criptomoeda, tabela, previousPrice);
            let estatisticas_ok = gerar_estatisticas(criptomoeda["Name"], tab2);

            let response = {
              tabela: tabela_ok,
              estatisticas: estatisticas_ok,
            };
            console.log("Resposta:", response);
            // Você pode fazer algo com 'response' aqui, se necessário
          });
        } else {
          console.log("Não há criptomoedas retornadas pela API");
        }

        stop_loading(tabela, tab2);
      })
      .catch((error) => {
        console.error("Erro ao obter os dados da API:", error);
        // Faça algo com o erro, se necessário
      });
  } catch (error) {
    console.error("Erro inesperado:", error);
  }
}

function iniciar_tab3() {
  fetch("/criptolist")
    .then((response) => response.json())
    .then((cripto_list) => {
      for (var i = 0; i < cripto_list.length; i++) {
        let item = `<option value="html">${cripto_list[i]}</option>`;
        list = cripto_list;
        $("#to").append(item);
      }
    });

  fetch("/criptodiponivel")
    .then((response) => response.json())
    .then((cripto_data) => {
      console.log(cripto_data);
      // dsl.setCandidate(cripto_data);
      // console.log(`Criptomoedas carregadas: ${cripto_data.length}`);
      for (var i = 0; i < cripto_data.length; i++) {
        let item = `<option value="html">${cripto_data[i]}</option>`;
        // console.log(item);
        $("#from").append(item);
      }
    });
}

$(document).ready(function () {
  const tabela = $("#dados-criptomoedas");
  const tab2 = $("#cards");

  iniciar_tab3();

  setInterval(function () {
    atualizarTabela(tabela, tab2);
  }, 80000);

  $(".reload").click(function () {
    atualizarTabela(tabela, tab2);
  });

  atualizarTabela(tabela, tab2);
  scroll();
  drag();
});
