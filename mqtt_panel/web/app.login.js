$(document).ready(function() {
    $("div.login form").submit(function(event) {
      event.preventDefault();
      fetch(
        $(this).attr('action'),
        {
          method: $(this).attr('method'),
          credentials: 'same-origin',
          cache: 'no-cache',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: $(this).serialize(),
        }
      )
      .then(response => response.json())
      .then(json => {
        document.cookie = json['session'];
        location.reload();
      })
      .catch( error => console.error('login error:', error));
    });
});
