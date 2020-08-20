"use strict"

function initMap() {
    const londonCoords = {
      lat: 51.5073509,
      lng: -0.1277583
    };

    const basicMap = new google.maps.Map(
        document.querySelector('#map'),
        {
          center: londonCoords,
          zoom: 11
        }
      );
    console.log(basicMap)
    
    const londonMarker = new google.maps.Marker({
        position: londonCoords,
        title: 'London',
        map: basicMap
        }
    );

    const londonInfo = new google.maps.InfoWindow({
        content: '<h1>London</h1>'
      });
    
      londonInfo.open(basicMap, londonMarker);
}