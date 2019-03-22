  //
  //
  //





  if (window.location.pathname.startsWith("/channel/")) {
      window.onbeforeunload = function (event) {
          event.returnValue = "Write something clever here..";
          localStorage.setItem("last_page", window.location.pathname);
          localStorage.setItem("closure_page", true);
      };
  }




  document.addEventListener('DOMContentLoaded', () => {

      if (localStorage.getItem("closure_page") == true) {
          console.log(localStorage.getItem("last_page"));
          window.location.href = localStorage.getItem("last_page");
          localStorage.setItem("closure_page", false);
      }


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

      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);



      // show active users:
      socket.on('connect', () => {
          console.log('connected user');
          try {
              document.querySelector('#add_user').onclick = function () {
                  const user = document.querySelector('#username').value.trim();
                  var existing_users = [];
                  var ul = document.getElementById("users_list");
                  var items = ul.getElementsByTagName("li");
                  for (var i = 0; i < items.length; i++) {
                      existing_users.push(items[i].innerText.trim().toLowerCase());
                  }
                  console.log(existing_users);

                  if (existing_users.indexOf(user) >= 0) {
                      alert("That users already exists..");
                  } else {
                      socket.emit('submit user', {
                          'user': user
                      });
                      document.querySelector("#registered_form").classList.add("hide");
                      document.querySelector("#logged_in").classList.remove("hide");
                  }
              };
          } catch (error) {
              console.log(`Error: ${error}`);
          }
      });
      socket.on('announce user', data => {
          const li = document.createElement('li');
          li.innerHTML = data.user;
          document.querySelector('#users_list').append(li);
          console.log(data.user);
      });

      // Sending and Emiting Messages
      socket.on('connect', () => {
          console.log('connected message');
          try {
              document.querySelector('#send').onclick = function () {
                  const message = document.querySelector('#messages').value;
                  //let image = document.getElementById('input').files[0];
                  socket.emit('submit message', {
                      "message": message,
                      "user": localStorage.getItem("display_name"),
                      "time": time,
                      "channel": document.querySelector('#channel').innerHTML,
                      //"image": image
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

      socket.on("connect", () => {
          console.log('connected logout');
          document.querySelector('#logout').onclick = function () {
              socket.emit('submit logout', {
                  "user": localStorage.getItem("display_name")
              });
              localStorage.removeItem("display_name");
          };
      });

      socket.on('announce logout', data => {
          var ul = document.getElementById("users_list");

          ul.querySelectorAll('li').forEach(function (item) {
              if (item.innerText == data.user)
                  item.remove();
              document.querySelector("#registered_form").classList.remove("hide");
              document.querySelector("#logged_in").classList.add("hide");

          });

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