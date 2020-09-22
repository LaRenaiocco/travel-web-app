"use strict"

const latLngObject = {lat: 0, lng: 0};

//  Build activity search map
function initMap() {
//  get latitude and longitude from database to build map
  $.get('/users/trips/activities.json', (data) => {
    const response = JSON.parse(data);
    latLngObject['lat'] = response.lat;
    latLngObject['lng'] = response.lng;
    // map instantiation
    const map = new google.maps.Map(document.getElementById("map"), {
      center: latLngObject,
      zoom: 8,
      mapTypeControl: false,
      fullscreenControl: false,
      styles: myMapStyle
    });
    //  Search bar for map
    const input = document.getElementById("pac-input");
    const autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo("bounds", map);
    autocomplete.setFields(["place_id", "geometry", "name", "formatted_address"]);
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(input);
    //  info window pop up after selecting search item
    const infowindow = new google.maps.InfoWindow();
    const infowindowContent = document.getElementById("infowindow-content");
    infowindow.setContent(infowindowContent);
    const geocoder = new google.maps.Geocoder();
    const marker = new google.maps.Marker({ map: map });
    // marker and info appears when user selects auto complete option
    marker.addListener("click", () => {
      infowindow.open(map, marker);
    });
    autocomplete.addListener("place_changed", () => {
      infowindow.close();
      const place = autocomplete.getPlace();
  
      if (!place.place_id) {
        return;
      }
      geocoder.geocode({ placeId: place.place_id }, (results, status) => {
        if (status !== "OK") {
          window.alert("Geocoder failed due to: " + status);
          return;
        }
        map.setZoom(11);
        map.setCenter(results[0].geometry.location);
        // Set the position of the marker using the place ID and location.
        marker.setPlace({
          placeId: place.place_id,
          location: results[0].geometry.location
        });
        marker.setVisible(true);
        infowindowContent.children["place-name"].textContent = place.name;
        infowindowContent.children["place-id"].textContent = place.place_id;
        infowindowContent.children["place-address"].textContent =
          results[0].formatted_address;
        infowindowContent.children["latlng"].textContent = results[0].geometry.location
        infowindow.open(map, marker);
      });
    });
  });
};
