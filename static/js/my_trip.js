"use strict"
//  Get all itinerary, activity and note data from DB to render full itinerary.
$.get('/users/itinerary/api', (data) => {

    const response = JSON.parse(data)
    const itinerary = response.itinerary
    const activities = response.activities
    const dates = response.dates
    const notes = response.notes

    $('#trip-name').html(`${itinerary.trip_name}`);
    $('#itinerary-id').html(`${itinerary.itinerary_id}`);

    //  Sets up base itinerary calender based on days of trip.
    let day = 1

    dates.forEach(d => {

        const date = document.createElement('div')
        date.textContent = `Day ${day}: ${d}`
        date.setAttribute('id', d)
        $('#travel-dates').append(date)
        day = day + 1
    });

    // Adds activities to the appropriate day or to the bottom of the list 
    // if no day specified.
    activities.forEach(a => {

        if (a.activity_day === null) {

            const name = document.createElement('div')
            name.setAttribute('class', 'activity-name')
            name.textContent = a.activity_name
            $('#misc-activities').append(name)

            const address = document.createElement('div')
            address.setAttribute('class', 'activity-address')
            address.textContent = a.address
            $('#misc-activities').append(address)

            if (a.note !== null) {
                const note = document.createElement('div')
                note.setAttribute('class', 'activity-note')
                note.textContent = a.activity_note
                $('#misc-activities').append(note)
            }
        } else {
            if (a.activity_time !== null) {
                const time = document.createElement('div')
                time.setAttribute('class', 'activity-time')
                time.textContent = a.activity_time
                $(`#${a.activity_day}`).append(time)
            }

            const name = document.createElement('div')
            name.setAttribute('class', 'activity-name')
            name.textContent = a.activity_name
            $(`#${a.activity_day}`).append(name)

            const address = document.createElement('div')
            address.setAttribute('class', 'activity-address')
            address.textContent = a.address
            $(`#${a.activity_day}`).append(address)

            if (a.activity_note !== null) {
                const note = document.createElement('div')
                note.setAttribute('class', 'activity-note')
                note.textContent = a.activity_note
                $(`#${a.activity_day}`).append(note)
            }
        }
    })
    // Adds note to the speicied day or to the notes section
    // if no day specified.
    notes.forEach(n => {
        if (n.day === null) {
            const note = document.createElement('div')
            note.setAttribute('class', 'itinerary-note')
            note.textContent = `${n.comment} - ${n.author}`
            $('#notes').append(note)
        } else {
            const note = document.createElement('div')
            note.setAttribute('class', 'itinerary-note')
            note.textContent = `${n.comment} - ${n.author}`
            $(`#${n.day}`).append(note)
        }
    })
    // Sets note date picker to days of trip.
    const min = itinerary.start_date;
    const max = itinerary.end_date;
    
    document.getElementById("comment-date").min = min
    document.getElementById("comment-date").max = max
})




//  Submits a new note to the DB and renders it to the Itinerary.
$('#new-note-form').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        comment: $('#comment').val(),
        date: $('#comment-date').val()
    };

    document.getElementById("new-note-form").reset();

    $.post('/users/trips/new-note.json', formData, (data) => {
        
        const response = JSON.parse(data)
        const comment = response.comment
        const author = response.author
        const day = response.day

        if (day === null) {
            const note = document.createElement('div')
            note.setAttribute('class', 'itinerary-note')
            note.textContent = `${comment} - ${author}`
            $('#notes').append(note)
        } else {
            const note = document.createElement('div')
            note.setAttribute('class', 'itinerary-note')
            note.textContent = `${comment} - ${author}`
            $(`#${day}`).append(note)
        }
    })
})

//  Alerts user of Itinerary ID to link another user to the same itinerary.
$('#add-mate-btn').on('click', () => {
    const itinAlert = $('#itinerary-id').text()
    alert(`Please give your mate this id number to link your trips: ${itinAlert}`)
})

//  redirects to the activity search page.
$('#add-activity-btn').on('click', () => {
    document.location.href = '/users/trips/activities'
})

window.onbeforeprint = function() {
    $('#pretty-print').hide()
    $('.itinerary-note').hide()
    $('#notes').hide()
    $('#add-activity-btn').hide()
    $('#add-new-note').hide()
    $('#travel-mates').hide()
    $('.map').hide()
}

window.onafterprint = function() {
    $('#pretty-print').show()
    $('.itinerary-note').show()
    $('#notes').show()
    $('#add-activity-btn').show()
    $('#add-new-note').show()
    $('#travel-mates').show()
    $('.map').show()
}