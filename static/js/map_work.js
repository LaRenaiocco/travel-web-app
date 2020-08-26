const activities = response.activites
for (a of activities) {
const id = a.activity_id;
const name = a.activity_name;
const address = a.address;
const latLng = {'lat': a.lat, 'lng': a.lng}

const activityMarker = new google.maps.Marker({
    position: latLng,
    title: `id: ${id}, ${name}`,
    map: basicMap
    }
);
const infoContent = document.createElement('div');
const strong = document.createElement('strong');
strong.textContent = name
infoContent.appendChild(strong);
infoContent.appendChild(document.createElement('br'));

const text = document.createElement('text');
text.textContent = address
infoContent.appendChild(text);

//  render day and time if included on info window.  Not working currently.

// if (a.activity_time !== null) {
//     infoContent.appendChild(document.createElement('br'));
//     const time = document.createElement('time');
//     time.textContent = a.activity_time
//     infoContent.appendChild(time);
// }

// if (a.activity_day !== null) {
//     const day = document.createElement('day');
//     day.textContent = a.activity_day
//     infoContent.appendChild(day);
// }
activityMarker.addListener('click', function() {
    infoWindow.setContent(infoContent);
    infoWindow.open(basicMap, activityMarker);

})
}