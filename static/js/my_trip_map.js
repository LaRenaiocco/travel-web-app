"use strict"
const latLngObject = {lat: 0, lng: 0}

//  Get itinerary and activity information from database


// create map based on itinerary and activity information in DB.
function initMap() {
    // create map
    $.get('/users/trips/api', (data) => {
      const response = JSON.parse(data)
    
      latLngObject['lat'] = response.itinerary.lat;
      latLngObject['lng'] = response.itinerary.lng;

    const basicMap = new google.maps.Map(
        document.querySelector('#itin-map'),
        {
          center: latLngObject,
          zoom: 7,
          mapTypeControl: false,
          fullscreenControl: false,
          styles: myMapStyle
        }
      );
    // Check out the section on "Destructuring objects" here:
    // https://hacks.mozilla.org/2015/05/es6-in-depth-destructuring/
    const activities = response.activities

      // Since you only use each of these variables once,
      // consider passing them directly to the Marker constructor
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
      // marker info content
      const infoContent = document.createElement('div');
      const placeName = document.createElement('div');
      placeName.setAttribute('class', 'marker-name');
      placeName.textContent = name
      infoContent.appendChild(placeName);
      // infoContent.appendChild(document.createElement('br'));
      
      const text = document.createElement('text');
      text.textContent = address
      infoContent.appendChild(text);

      const activityInfo = new google.maps.InfoWindow({
        content: infoContent
      });
      
      activityMarker.addListener('click', function() {
          activityInfo.open(basicMap, activityMarker);
          for (const a of document.getElementsByClassName('activity-name')) {
            if (a.textContent.includes(name)) {
              // a.style.color = '#339989'
              a.setAttribute("style", "color: #8ae5d6; background-color: #339989; font-size: x-large")
            }
          }
      })
      activityInfo.addListener('closeclick', function() {
        for (const a of document.getElementsByClassName('activity-name')) {
          if (a.textContent.includes(name)) {
            a.setAttribute("style", "color: #2d383e; background-color: #f6ddcb; font-size: large")
          }
        }
      })
    })
  });
}