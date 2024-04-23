
function moveAll(from, to) {
  $('#'+from+' option').remove().appendTo('#'+to); 
}

function moveSelected(from, to) {
  $('#'+from+' option:selected').remove().appendTo('#'+to); 
}
function selectAll(event) {
  event.preventDefault();
  //return all itens$("select option").attr("selected","selected");

  var selectElement = document.getElementById("to");
    
  // Array para armazenar as opções selecionadas
  var opcoesSelecionadas = [];
  
  // Iterar sobre as opções e adicionar as selecionadas ao array
  for (var i = 0; i < selectElement.options.length; i++) {
    console.log(selectElement)
      if (selectElement.options[i]) {
          opcoesSelecionadas.push(selectElement.options[i].text);
          // console.log(opcoesSelecionadas)
      }
  }
  
  // Criar objeto com os dados a serem enviados
  var dados = opcoesSelecionadas
 
  
  //Realizar a solicitação POST
  fetch('/editarlista', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Erro ao enviar os dados');
      }
      return response.json();
  })
  .then(data => {
      // Manipular a resposta, se necessário
      console.log('Resposta do servidor:', data);
      $.alert({
        title: 'Suceso!',
        content: 'Alteração realizada com sucesso',
        theme: 'dark'
    });
  })
  .catch(error => {
      console.error('Erro:', error);
  });
}
  
