"use strict"

function initMap() {

const latLngObject = {lat: 0, lng: 0}

$.get('/users/trips/api', (data) => {
 
  const response = JSON.parse(data)

  latLngObject['lat'] = response.itinerary.lat;
  latLngObject['lng'] = response.itinerary.lng;


    const basicMap = new google.maps.Map(
        document.querySelector('#map'),
        {
          center: latLngObject,
          zoom: 7
        }
      );
    // console.log(basicMap)
    
    // const tripMarker = new google.maps.Marker({
    //     position: latLngObject,
    //     title: 'My Trip',
    //     map: basicMap
    //     }
    // );

    // const tripInfo = new google.maps.InfoWindow({
    //     content: `<h2>Let's go to ${response.itinerary.trip_name}</h2>`
    //   });
    
    //   tripInfo.open(basicMap, tripMarker);

    const activities = response.activities

    console.log(activities)

    activities.forEach(a => {
      const id = a.activity_id;
      const name = a.activity_name;
      const address = a.address;
      const latLng = {'lat': a.lat, 'lng': a.lng};
      // const date = a.date;
      // const time = a.time;

      
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

      const activityInfo = new google.maps.InfoWindow({
        content: infoContent
      });
      
      activityMarker.addListener('click', function() {
          activityInfo.open(basicMap, activityMarker);
      
      })
      })
  });
}