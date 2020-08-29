"use strict"
//  switch home screen to create new user information
$('#create-user-link').on('click', () => {
    $('#new-user').show()
    $('#login-info').hide()
});

//  switch home screen to login information
$('#back-to-login').on('click', () => {
    $('#new-user').hide()
    $('#login-info').show()
});

// submit new user form to the database and return to login page on success
$('#new-user-form').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        email: $('#new-email').val(),
        password: $('#new-password').val(),
        fname: $('#new-fname').val(),
        lname: $('#new-lname').val()
        };

    document.getElementById("new-user-form").reset();

    $.post('/users/create-user.json', formData, (response) => {
        alert(response)
    $('#new-user').hide()
    $('#login-info').show()
    });
});
