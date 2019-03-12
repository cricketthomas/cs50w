  //
  //
  //
  document.addEventListener('DOMContentLoaded', () => {
      // Once the page and contents loads
      if (localStorage.getItem("display_name") === 'undefined' || localStorage.getItem("display_name") === null || localStorage.getItem("display_name") === "") {
          document.querySelector("#registered_form").classList.remove("hide");
          document.querySelector("#logged_in").classList.add("hide");
          document.querySelector('#registered_form').onsubmit = function () {
              // Store
              const display_name = localStorage.setItem("display_name", document.querySelector("#username").value);
              document.querySelector("#registered_form").classList.add("hide");
              // Retrieve
          };
      } else {
          document.querySelector("#display_name").innerHTML = localStorage.display_name;

      }



      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

      // When connected, configure buttons
      socket.on('connect', () => {

          // Each button should emit a "submit vote" event
          document.querySelectorAll('button').forEach(button => {
              button.onclick = () => {
                  const selection = button.dataset.vote;
                  socket.emit('submit vote', {
                      'selection': selection,
                  });
              };
          });
      });

      // When a new vote is announced, add to the unordered list
      socket.on('announce vote', data => {
          const li = document.createElement('li');
          li.innerHTML = `User: ${localStorage.display_name} Voted for: ${data.selection}`;
          document.querySelector('#votes').append(li);
      });





  });


  /* Put the object into storage
  localStorage.setItem('username', JSON.stringify(testObject));

  // Retrieve the object from storage
  var retrievedObject = localStorage.getItem('testObject');

  console.log('retrievedObject: ', JSON.parse(retrievedObject));
  */