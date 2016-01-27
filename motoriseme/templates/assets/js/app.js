$(document).foundation();

window.addEventListener("load", function () {


  if(document.getElementById("profile-button") != null) {
    document.getElementById("profile-button").addEventListener("click", function (e) {
      e.preventDefault();
      //e.stopPropagation();
    });
  }

  if(document.getElementById("expand-filter") != null) {
    document.getElementById("expand-filter").addEventListener("click", function (e) {
      e.preventDefault();
      var expanded = document.getElementById("expand-filter").getAttribute('data-expanded');
      //alert(expanded);
      if(expanded == "true") {
        document.getElementById("filter-content").style.visibility = "hidden";
        document.getElementById("filter").style.height = "5px";
        document.getElementById("expand-filter").innerHTML = "&#xf078;";
        document.getElementById("expand-filter").setAttribute('data-expanded', "false");
      } else {
        document.getElementById("filter-content").style.visibility = "visible";
        document.getElementById("filter").style.height = "200px";
        document.getElementById("expand-filter").innerHTML = "&#xf077;";
        document.getElementById("expand-filter").setAttribute('data-expanded', "true");
      }
      //e.stopPropagation();
      //alert("Ти експандна филтъра");
    });
  }

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
