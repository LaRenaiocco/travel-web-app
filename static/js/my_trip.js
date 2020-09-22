"use strict"
//  Get all itinerary, activity and note data from DB to render full itinerary.
$.get('/users/itinerary/api', (data) => {
  const response = JSON.parse(data);
  const itinerary = response.itinerary;
  let activities = response.activities;
  const dates = response.dates;
  const notes = response.notes;
  const friends = response.friends;
  // Fill in trip and itinerary id in HTML
  $('#trip-name').html(`${itinerary.trip_name}`);
  $('#itinerary-id').html(`${itinerary.itinerary_id}`);
  //  Sets up itinerary calender based on days of trip.
  let day = 1;
  dates.forEach(d => {
    const date = document.createElement('div');
    date.textContent = `day ${day}: ${d}`;
    date.setAttribute('id', d);
    date.setAttribute('class', 'days');
    $('#travel-dates').append(date);
    day = day + 1;
  });
    // Sorts activities by time(if one is included) for ordered 
    // placement on itinerary
    const untimedActivities = [];
    const timedActivities = [];
    // separate activities by timed and untimed and convert to iso format
    activities.forEach(a => {
        if (a.activity_time !== null) {
            if (a.activity_day !== null) {
                a.iso = new Date(`${a.activity_day}T${a.activity_time}`);
            } else {
            a.iso = new Date(`1970-01-01T${a.activity_time}`)};
            timedActivities.push(a);
        } else {
            untimedActivities.push(a);
        };
    });
    // sort timed activites in order from earliest to latest.
    timedActivities.sort((a, b) => a.iso - b.iso);
    // rejoin timed and untimed activities to one array
    activities = timedActivities.concat(untimedActivities);
    // Adds activities to the appropriate day or to the bottom of the list 
    // if no day specified.
    activities.forEach(a => {
      // adds undated activity to misc. section of itinerary
      if (a.activity_day === null) {
        const name = document.createElement('div');
        name.setAttribute('class', 'activity-name');
        name.textContent = a.activity_name;
        $('#misc-activities').append(name);
        const address = document.createElement('div');
        address.setAttribute('class', 'activity-address');
        address.textContent = a.address;
        $('#misc-activities').append(address);
        // if an activity has an optional note, adds note to itinerary
        if (a.note !== null) {
          const note = document.createElement('div');
          note.setAttribute('class', 'activity-note');
          note.textContent = a.activity_note;
          $('#misc-activities').append(note);
        };
      // adds dated activities to the itinerary
      } else {
        // if activity has a time, add time to itinerary
        if (a.activity_time !== null) {
          const time = document.createElement('div');
          time.setAttribute('class', 'activity-time');
          time.textContent = a.activity_time;
          $(`#${a.activity_day}`).append(time);
        };
        const name = document.createElement('div');
        name.setAttribute('class', 'activity-name');
        name.textContent = a.activity_name;
        $(`#${a.activity_day}`).append(name);
        const address = document.createElement('div');
        address.setAttribute('class', 'activity-address');
        address.textContent = a.address;
        $(`#${a.activity_day}`).append(address);
        // if activity has a note, add note to itinerary
        if (a.activity_note !== null) {
          const note = document.createElement('div');
          note.setAttribute('class', 'activity-note');
          note.textContent = a.activity_note;
          $(`#${a.activity_day}`).append(note);
        };
      };
    });
    // Adds note to the speicied day or to the notes section
    // if no day specified.
    notes.forEach(n => {
      if (n.day === null) {
        const note = document.createElement('div');
        note.setAttribute('class', 'itinerary-note');
        note.textContent = `${n.comment} - ${n.author}`;
        $('#notes').append(note);
      } else {
        const note = document.createElement('div');
        note.setAttribute('class', 'itinerary-note');
        note.textContent = `${n.comment} - ${n.author}`;
        $(`#${n.day}`).append(note);
      };
    });
    // Displays list of friends sharing this trip.
    friends.forEach(f => {
      const friend = document.createElement('span');
      friend.textContent = `${f[0]}   `;
      $('#travel-mates').append(friend);
    });
    // Sets note date picker to days of trip.
    document.getElementById("comment-date").min = itinerary.start_date;
    document.getElementById("comment-date").max = itinerary.end_date;
});

//  Submits a new note to the DB and renders it to the Itinerary.
$('#new-note-form').on('submit', (evt) => {
  evt.preventDefault();
  const formData = {
    comment: $('#comment').val(),
    date: $('#comment-date').val()
  };
  // reset new note form
  document.getElementById("new-note-form").reset();
  // send note to DB
  $.post('/users/trips/new-note.json', formData, (data) => {
    const response = JSON.parse(data);
    const comment = response.comment;
    const author = response.author;
    const day = response.day;
    // add  undated note to notes section 
    if (day === null) {
      const note = document.createElement('div');
      note.setAttribute('class', 'itinerary-note');
      note.textContent = `${comment} - ${author}`;
      $('#notes').append(note);
    // add note to applicable day
    } else {
      const note = document.createElement('div');
      note.setAttribute('class', 'itinerary-note');
      note.textContent = `${comment} - ${author}`;
      $(`#${day}`).append(note);
    };
  });
});

//  Alerts user of Itinerary ID to link another user to the same itinerary.
$('#add-mate-btn').on('click', () => {
  const itinAlert = $('#itinerary-id').text();
  $('#add-friend-modal-text').text
    (`Please give your travel mate the following id number to link your trips: ${itinAlert}. 
    They will enter this unique id number in their profile to join this trip.`);
  $('#add-friend-modal').modal('toggle');
});

//  redirects to the activity search page.
$('#add-activity-btn').on('click', () => {
  document.location.href = '/users/trips/activities';
});

//  Changes CSS for pretty printing
window.onbeforeprint = function() {
  $('#trip-name').css('text-align', 'left');
  $('#col-two').hide();
};
window.onafterprint = function() {
  $('#trip-name').css('text-align', 'center');
  $('#col-two').show();
};