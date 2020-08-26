"use strict"
// create map based on itinerary and activity information in DB.
function initMap() {

  const latLngObject = {lat: 0, lng: 0}

  //  Get itinerary and activity information
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

    // Check out the section on "Destructuring objects" here:
    // https://hacks.mozilla.org/2015/05/es6-in-depth-destructuring/
    const activities = response.activities

    activities.forEach(a => {
      // Since you only use each of these variables once,
      // consider passing them directly to the Marker constructor
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
      const infoContent = document.createElement('div');
      // Consider adding a class on the infoContent div
      // that sets the font-weight, instead of using <strong>
      const strong = document.createElement('strong');
      strong.setAttribute('class', 'marker-name');
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