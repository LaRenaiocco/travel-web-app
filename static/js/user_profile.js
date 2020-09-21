"use strict"

// Gets user and itinerary data to render profile page
$.get('/users/profile/api', (data) => {
  $('#user-name').text(`${data.fname} ${data.lname}`);
  $('#user-email').text(data.email);
  const itineraries = data.itineraries;
  // show "no itineraries" message
  if (itineraries.length !== 0) {
    $('#no-itinerary').hide();
  };
  // render list of itineraries
  itineraries.forEach(i => {
    $('#user-itineraries').append(`<li><a href="/users/trips/${i.itinerary_id}">${i.trip_name}</a></li>`);
  });
});

// submits new trip information to be added to DB and adds to html.
$('#new-trip-submit').on('click', () => {
  const formData = {
    trip_name: $('#city-input').val(),
    start_date: $('#depart-date').val(),
    end_date: $('#return-date').val()
  };
  $.post('/users/trips/new-trip.json', formData, (response) => {
    $('#user-itineraries').append(`<li><a href="/users/trips/${response['itinerary_id']}">${response['trip_name']}</a></li>`);
    $('#new-trip-modal').modal('toggle');
    $('#no-itinerary').hide();
  });
});

// Creates a UserItinerary link in DB and adds itinerary to html.
$('#existing-submit').on('click', () => {
  $.post('/users/trips/add-trip.json', {'id': $('#existing-trip-id').val()}, (response) => {
    $('#user-itineraries').append(`<li><a href="/users/trips/${response['itinerary_id']}">${response['trip_name']}</a></li>`);
    document.getElementById("existing-trip-form").reset();
    $('#existing-trip-modal').modal('toggle');
    $('#no-itinerary').hide();
  });
});

// Submits phone number to DB for text updates
$('#phone-submit').on('click', () => {
  $.post('/users/phone-update/api', {'phone': $('#phone-num').val()}, (response) => {
    $('#text-modal').modal('toggle');
    alert(response);
  });
});

// removes a phone number from the database
$('#disable-trip-text').on('click', () => {
  $.post('/users/phone-update/api', {'phone': 'None'}, (response) => {
    $('#text-disable-text').text(response);
    $('#text-disable').modal('toggle');
  })  ;
});