"use strict"

// Shows new trip form
$('#new-trip-btn').on('click', () => {
  $('#add-new-trip').show();
})

// submits new trip information to be added to DB and adds to html.
$('#new-trip-form').on('submit', (evt) => {
  evt.preventDefault();
    
  const formData = {
    trip_name: $('#city-input').val(),
    start_date: $('#depart-date').val(),
    end_date: $('#return-date').val()
  };

  document.getElementById("new-trip-form").reset();

  $.post('/users/trips/new-trip.json', formData, (response) => {
    $('ul').append(`<li><a href="/users/trips/${response['itinerary_id']}">${response['trip_name']}</a></li>`)
    $('#add-new-trip').hide();
  });
});

// shows add existing trip form
$('#existing-trip-button').on('click', () => {
  $('#add-existing-trip').show();
})

// Creates a UserItinerary link in DB and adds itinerary to html.
$('#existing-trip-form').on('submit', (evt) => {
  evt.preventDefault();

  $.post('/users/trips/add-trip.json', {'id': $('#existing-trip-id').val()}, (response) => {
    $('ul').append(`<li><a href="/users/trips/${response['itinerary_id']}">${response['trip_name']}</a></li>`)
    document.getElementById("existing-trip-form").reset();
    $('#add-existing-trip').hide();
  });
});