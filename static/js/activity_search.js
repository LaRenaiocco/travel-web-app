"use strict"

// Return Itienrary start and end days to lock activity date picker to days of trip.
$.get('/users/trips/activities.json', (data) => {

    const response = JSON.parse(data)

    const min = response.start_date;
    const max = response.end_date;

    document.getElementById("activity-date").min = min
    document.getElementById("activity-date").max = max
})

// Submit new activity to DB and return alert that activity is added.
$('#new-activity-form').on('submit', (evt) => {
    evt.preventDefault();

    const placeName = $('#place-name').text()
    console.log(placeName)

    const formData = {
        name: $('#place-name').text(),
        address: $('#place-address').text(),
        latlng: $('#latlng').text(),
        day: $('#activity-date').val(),
        time: $('#activity-time').val(),
        note: $('#activity-note').val()
    }
    
    console.log(formData)

    document.getElementById("new-activity-form").reset();


    $.post('/users/trips/new-activity/api', formData, (response) => {

        alert(response)
    })
});

// redirect back to Itinerary page.
// $('#back-to-itinerary').on('click', () => {
//     document.location.href = `/users/trips/`
// })