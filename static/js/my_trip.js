"use strict"

function initMap() {

const latLngObject = {lat: 0, lng: 0}

$.get('/users/trips/api', (data) => {
  // const response = data.json()
  console.log(data)
  const response = JSON.parse(data)
  console.log(response)
  // console.log(data.itinerary)

  // latLngObject['lat'] = response['itinerary']['lat'];
  // latLngObject['lng'] = response['itinerary']['lng'];

  // latLngObject['lat'] = data.lat;
  // latLngObject['lng'] = data.lng;
  latLngObject['lat'] = response.itinerary.lat;
  latLngObject['lng'] = response.itinerary.lng;


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
        content: `<h2>Let's go to ${response.itinerary.trip_name}</h2>`
      });
    
      tripInfo.open(basicMap, tripMarker);
  });
}