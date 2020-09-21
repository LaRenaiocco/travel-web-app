"use strict"

// submit new user form to the database and return to login page on success
$('#new-user-submit').on('click', () => {

    const formData = {
        email: $('#new-email').val(),
        password: $('#new-password').val(),
        fname: $('#new-fname').val(),
        lname: $('#new-lname').val()
        };

    $.post('/users/create-user.json', formData, (response) => {
        // $('#alert-modal-text').text(response);
        $('#new-user-modal').modal('toggle');
        alert(response)
        // $('#alert-modal').modal('open');
        });
});


