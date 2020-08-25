"use strict"

$('#create-user-link').on('click', () => {
    $('#new-user').show()
    $('#login-info').hide()
})

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
    })
})