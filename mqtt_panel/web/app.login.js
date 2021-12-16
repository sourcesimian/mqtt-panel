
$(document).ready(function() {
    $("div.login form").submit(function(event) {
      event.preventDefault();
      $('#screen-overlay').trigger('spinner');
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
      .then(response => {
        return response.json();
      })
      .then(json => {
        $('.login .message').html(json['message']);
        if (json['success'] == true) {
          document.cookie = json['session'];
          location.reload();
        } else {
          $('#screen-overlay').trigger('hide');
        }
      })
      .catch(error => {
        $('#screen-overlay').trigger('hide');
        $('.login .message').html(error);
        console.error('login error: ' + error);
      });
    });
});

let screenOverlay = new ScreenOverlay();
