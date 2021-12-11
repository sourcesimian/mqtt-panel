$(document).ready(function() {
    $("div.login form").submit(function(event) {
      event.preventDefault();
      $('.login .loading').removeClass('d-none');
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
        $('.login .loading').addClass('d-none');
        return response.json();
      })
      .then(json => {
        $('.login .message').html(json['message']);
        if (json['success'] == true) {
          document.cookie = json['session'];
          location.reload();
        }
      })
      .catch(error => {
        $('.login .loading').addClass('d-none');
        $('.login .message').html(error);
        console.error('login error:', error);
      });
    });
});
