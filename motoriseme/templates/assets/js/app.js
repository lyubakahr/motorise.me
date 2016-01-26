$(document).foundation();

window.addEventListener("load", function () {
  if(document.getElementById("signup-button") != null) {
    document.getElementById("signup-button").addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var form = document.getElementById("register-form");
      form.submit();
    });
  }
  
  L.mapbox.accessToken = 'pk.eyJ1IjoidG9zaGxlIiwiYSI6ImNpanR4dzIxODAwMGx0em00eDNwb2c1dnEifQ.0AEcgIpeNUpMCQc5HvKr6A';
  var map = L.mapbox.map('map', 'mapbox.streets');

  var myLayer = L.mapbox.featureLayer().addTo(map);

  if (!navigator.geolocation) {
    alert('Geolocation is not available');
  } else {
    map.locate();
  }

  map.on('locationfound', function(e) {
    map.fitBounds(e.bounds);

    myLayer.setGeoJSON({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [e.latlng.lng, e.latlng.lat]
      },
      properties: {
        'title': 'Here I am!',
        'marker-color': '#ff8888',
        'marker-symbol': 'star'
      }
    });

  });

  map.on('locationerror', function(e) {
    console.log(e);
  });


});
