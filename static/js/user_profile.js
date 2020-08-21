$('#new-trip-form').on('submit', (evt) => {
  evt.preventDefault();
    
  const formData = {
    trip_name: $('#city-input').val(),
    start_date: $('#depart-date').val(),
    end_date: $('#return-date').val()
  };
  // console.log(formData)
  $.post('/users/trips/new-trip.json', formData, (response) => {
    $('ul').append(`<li><a href="/users/trips/${response['itinerary_id']}">${response['trip_name']}</a></li>`)
    // $('ul').append(`<li><a href="/users/trips/${response.itinerary_id}"></a>${response.trip_name}</li>`)
  });
});
