"use strict"

// Return Itienrary start and end days to lock activity date picker to days of trip.
$.get('/users/trips/activities.json', (data) => {
  const response = JSON.parse(data);
  // lock date picker to days of trip
  document.getElementById("activity-date").min = response.start_date;
  document.getElementById("activity-date").max = response.end_date;
  // return to itinerary
  $('#back-to-itinerary').on('click', () => {
    console.log(response.itinerary_id);
    document.location.href = `/users/trips/${response.itinerary_id}`;
  });
});

// Submit new activity to DB and return alert that activity is added.
$('#new-activity-form').on('submit', (evt) => {
  evt.preventDefault();
  const formData = {
    name: $('#place-name').text(),
    address: $('#place-address').text(),
    latlng: $('#latlng').text(),
    day: $('#activity-date').val(),
    time: $('#activity-time').val(),
    note: $('#activity-note').val()
  };
  // reset new activity form
  document.getElementById("new-activity-form").reset();
  // submit activity to DB and return response in modal
  $.post('/users/trips/new-activity/api', formData, (response) => {
    $('#activity-modal-text').text(response);
    $('#activity-modal').modal('toggle');
  });
});
