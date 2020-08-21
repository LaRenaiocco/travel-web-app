"use strict"

function initMap() {

const latLngObject = {lat: 0, lng: 0}

$.get('/users/trips/api', (data) => {
  latLngObject['lat'] = data.lat;
  latLngObject['lng'] = data.lng;


    const basicMap = new google.maps.Map(
        document.querySelector('#map'),
        {
          center: latLngObject,
          zoom: 7
        }
      );
    console.log(basicMap)
    
    const tripMarker = new google.maps.Marker({
        position: latLngObject,
        title: 'My Trip',
        map: basicMap
        }
    );

    const tripInfo = new google.maps.InfoWindow({
        content: `<h2>Let's go to ${data.trip_name}</h2>`
      });
    
      tripInfo.open(basicMap, tripMarker);
  });
}