  //
  //
  //
  document.addEventListener('DOMContentLoaded', () => {
      var time = new Date();
      // Join Default Channel
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


      if (localStorage.getItem("last_page") === null || localStorage.getItem("last_page") === "") {
          localStorage.setItem("last_page", window.location.href);
          console.log("no last page");
      } else {
          console.log("last page exists", localStorage.getItem("last_page"));
          localStorage.setItem("last_page", window.location.href);
          if (localStorage.getItem.last_page !== window.location.href) {
              localStorage.setItem("last_page", window.location.href);
          }
      }




      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);



      // Sending and Emiting Messages
      socket.on('connect', () => {
          console.log('connected message');
          try {
              document.querySelector('#send').onclick = function () {
                  const message = document.querySelector('#messages').value;
                  socket.emit('submit message', {
                      "message": message,
                      "user": localStorage.getItem("display_name"),
                      "time": time,
                      "channel": document.querySelector('#channel').innerHTML
                  });
                  document.getElementById('messages').value = "";
                  socket.emit('join', {
                      'channel': document.querySelector('#channel').innerHTML
                  });

              };

          } catch (error) {
              console.log(`This page is missing elements causing: ${error}`);
          }


      });
      socket.on('announce message', data => {
          const li = document.createElement('li');
          //var obj = JSON.stringify(data);
          if (data.channel === document.querySelector('#channel').innerHTML) {
              li.innerHTML = `${data.user} says: ${data.message} at ${data.time}`;
              document.querySelector('#msg').append(li);
          }
          console.log(data);
      });


      // Sending New Channels
      socket.on('connect', () => {
          console.log('connected channel');
          try {
              document.querySelector('#submit_channel').onclick = function () {
                  const channel = document.querySelector('#create_channel').value.trim();
                  var existing_channels = [];
                  var ul = document.getElementById("channels_list");
                  var items = ul.getElementsByTagName("li");
                  for (var i = 0; i < items.length; i++) {
                      existing_channels.push(items[i].innerText.trim().toLowerCase());
                  }
                  console.log(existing_channels);

                  if (existing_channels.indexOf(channel) >= 0) {
                      alert("That channel already exists..");
                  } else {
                      socket.emit('submit channel', {
                          'channel': channel
                      });
                      document.getElementById('create_channel').value = "";
                  }
              };
          } catch (error) {
              console.log(`Error: ${error}`);
          }
      });
      socket.on('announce channel', data => {
          const li = document.createElement('li');
          li.innerHTML = "<a href=/channel/" + data.channel + ">" + data.channel + "</a>";
          document.querySelector('#channels_list').append(li);

          console.log(data.channel);
      });

  });

  /*
   // When connected, configure buttons
      socket.on('connect', () => {
          console.log('connected');
          // Each button should emit a "submit vote" event
          document.querySelectorAll('button').forEach(button => {
              button.onclick = () => {
                  const selection = button.dataset.vote;
                  socket.emit('submit vote', {
                      'selection': selection
                  });
              };
          });
      });
      // When a new vote is announced, add to the unordered list
      socket.on('vote totals', data => {
          document.querySelector('#yes').innerHTML = data.yes;
          document.querySelector('#no').innerHTML = data.no;
          document.querySelector('#maybe').innerHTML = data.maybe;
      });

  */