"use strict"

const latLngObject = {lat: 0, lng: 0};
// create map based on itinerary and activity information in DB.
function initMap() {
  //  Get itinerary and activity information from database
  $.get('/users/trips/api', (data) => {
    const response = JSON.parse(data);
    latLngObject['lat'] = response.itinerary.lat;
    latLngObject['lng'] = response.itinerary.lng;
    const activities = response.activities
    // create map
    const basicMap = new google.maps.Map(
        document.querySelector('#itin-map'),
        {
          center: latLngObject,
          zoom: 12,
          mapTypeControl: false,
          fullscreenControl: false,
          styles: myMapStyle
        });
    // create map markers for each activity
    activities.forEach(a => {
      const id = a.activity_id;
      const name = a.activity_name;
      const address = a.address;
      const latLng = {'lat': a.lat, 'lng': a.lng};

      const activityMarker = new google.maps.Marker({
          position: latLng,
          title: `id: ${id}, ${name}`,
          map: basicMap
          }
      );
      // marker info content: place name and address
      const infoContent = document.createElement('div');
      const placeName = document.createElement('div');
      placeName.setAttribute('class', 'marker-name');
      placeName.textContent = name;
      infoContent.appendChild(placeName);
      const text = document.createElement('text');
      text.textContent = address
      infoContent.appendChild(text);
      // create info window attached to each marker
      const activityInfo = new google.maps.InfoWindow({content: infoContent});
      // set info window to open on click of marker
      activityMarker.addListener('click', function() {
          activityInfo.open(basicMap, activityMarker);
          // find matching place on itinerary and highlight
          for (const a of document.getElementsByClassName('activity-name')) {
            if (a.textContent.includes(name)) {
              a.setAttribute("style", "color: #8ae5d6; background-color: #339989; font-size: x-large")
            };
          };
      });
      // un-highlight on close of info window
      activityInfo.addListener('closeclick', function() {
        for (const a of document.getElementsByClassName('activity-name')) {
          if (a.textContent.includes(name)) {
            a.setAttribute("style", "color: #2d383e; background-color: #f6ddcb; font-size: large")
          };
        };
      });
    });
  });
};