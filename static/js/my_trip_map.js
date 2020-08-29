"use strict"
// create map based on itinerary and activity information in DB.
function initMap() {

  const latLngObject = {lat: 0, lng: 0}

  //  Get itinerary and activity information from database
  $.get('/users/trips/api', (data) => {
    const response = JSON.parse(data)

    latLngObject['lat'] = response.itinerary.lat;
    latLngObject['lng'] = response.itinerary.lng;

    // create map
    const basicMap = new google.maps.Map(
        document.querySelector('#map'),
        {
          center: latLngObject,
          zoom: 7
        }
      );
    //  add activity data to map on markers
    const activities = response.activities

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
      infoContent.appendChild(document.createElement('br'));
      
      const text = document.createElement('text');
      text.textContent = address
      infoContent.appendChild(text);

      const activityInfo = new google.maps.InfoWindow({
        content: infoContent
      });
      
      activityMarker.addListener('click', function() {
          activityInfo.open(basicMap, activityMarker);

      
      })
    })
  });
}