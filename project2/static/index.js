  //
  //
  //
  //

  document.addEventListener('DOMContentLoaded', () => {
      document.querySelector('#registered_form').onsubmit = () => {

          // Initialize new request
          const request = new XMLHttpRequest();
          const username = document.querySelector('#username').value;
          request.open('POST', '/registered');

          // Callback function for when request completes
          request.onload = () => {

              // Extract JSON data from request
              const data = JSON.parse(request.responseText);
              // Update local storage
              if (data.success) {
                  const contents = `username is ${data.username}.`
                  localStorage.setItem("username", data.username)
                  localStorage.setItem("logged_in", data.success)
                  document.querySelector('#result').innerHTML = contents;
              } else {
                  document.querySelector('#result').innerHTML = 'There was an error.';
              }
          }

          // Add data to send with request
          const data = new FormData();
          data.append('username', username);
          console.log(localStorage.username);
          console.log(localStorage.success);
          // Send request
          request.send(data);

          window.location.href = "/"

          return false;
      };








  });


  /* Put the object into storage
  localStorage.setItem('username', JSON.stringify(testObject));

  // Retrieve the object from storage
  var retrievedObject = localStorage.getItem('testObject');

  console.log('retrievedObject: ', JSON.parse(retrievedObject));
  */