$(document).foundation();


window.addEventListener("load", function () {
  var numberOfWaypoints = 0;

  this.getEventMarkers = function() {
    // /read_user_events
    var url = "/read_user_events";
    this.features = [];
    console.log(this);
    var that = this;
    var request = $.ajax({
      url: url,
      method: "GET"
      // error: function(jqXHR, textStatus) {
      //   console.log("Failed to get events: " + textStatus);
      // }
    });
    return request;
  }

  if(document.getElementById("profile-button") != null) {
    document.getElementById("profile-button").addEventListener("click", function (e) {
      e.preventDefault();
      //e.stopPropagation();
    });
  }

  if(document.getElementById("route-add-button") != null) {
    document.getElementById("route-add-button").addEventListener("click", function (e) {
      e.preventDefault();
      //e.stopPropagation();
      //input type="text" id="ride-finish" class="create-form-text" placeholder="Search for a place or click on the map" name="ride_end_point"
      if(numberOfWaypoints < 10) {
        var newItem = document.createElement("input");
        newItem.setAttribute('name', 'waypoint' + numberOfWaypoints);
        newItem.setAttribute('class', 'create-form-text');
        newItem.setAttribute('type', 'text');
        newItem.setAttribute('placeholder', 'Search for a place or click on the map');
        numberOfWaypoints++;
        var finish = document.getElementById("ride-finish-text");
        finish.parentNode.insertBefore(newItem, finish);
      }
    });
  }

  if(document.getElementById("create-ride-button") != null) {
    document.getElementById("create-ride-button").addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      // var opened = document.getElementById("create-ride").style.visibility;
      // document.getElementById("create-ride").style.visibility = "visible";
      document.getElementById("create-ride-holder").style.right = "0";
    });
  }

  if(document.getElementById("create-close-button") != null) {
    document.getElementById("create-close-button").addEventListener("click", function (e) {
      e.preventDefault();
      // var opened = document.getElementById("create-ride").style.visibility;
      document.getElementById("create-ride-holder").style.right = "-500px";
      // document.getElementById("create-ride").style.visibility = "hidden";
    });
  }

  if(document.getElementById("expand-filter") != null) {
    document.getElementById("expand-filter").addEventListener("click", function (e) {
      e.preventDefault();
      var expanded = document.getElementById("expand-filter").getAttribute('data-expanded');
      //alert(expanded);
      if(expanded == "true") {
        document.getElementById("filter").style.height = "5px";
        setTimeout(function() {
          document.getElementById("filter-content").style.visibility = "hidden";
        },1000);
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
  //if(document.getElementById("map") != null) {
    L.mapbox.accessToken = 'pk.eyJ1IjoidG9zaGxlIiwiYSI6ImNpanR4dzIxODAwMGx0em00eDNwb2c1dnEifQ.0AEcgIpeNUpMCQc5HvKr6A';
    var map = L.mapbox.map('map', 'mapbox.streets');
    var myLayer = L.mapbox.featureLayer().addTo(map);
    var that = this;
    map.on('ready', function(e) {
      console.log("that");
      console.log(that);
      var req = that.getEventMarkers();
      req.done(function(result) {
        var data = result;
        var features = [];
        data.forEach(function(feature) {
          var startlng = feature.start_point_coordinates.split(",")[0];
          var startlat = feature.start_point_coordinates.split(",")[1];
          var endlng = feature.end_point_coordinates.split(",")[0];
          var endlat = feature.end_point_coordinates.split(",")[1];

          features.push({
                          type: 'Feature',
                          geometry: {
                            type: 'Point',
                            coordinates: [startlng, startlat]
                          },
                          properties: {
                            'title': feature.name,
                            'marker-color': '#88ff88',
                            'marker-symbol': 'embassy'
                          }
                        });
        });
        myLayer.setGeoJSON({
            type: "FeatureCollection",
            features: features
        });
      }).fail(function(jqXHR, statusText) {
        console.log("Failed to get events: " + statusText);
      });
      
    });

    if (!navigator.geolocation) {
      alert('Geolocation is not available');
    } else {
      map.locate();
    }

    map.on('locationfound', function(e) {
      map.fitBounds(e.bounds);
      console.log(e.latlng.lng + " " + e.latlng.lat);
    });

    map.on('locationerror', function(e) {
      console.log(e);
    });
  //}
    map.addControl(L.mapbox.geocoderControl('mapbox.places', {
        autocomplete: true
    }));
    L.control.locate().addTo(map);

    // var directions = L.mapbox.directions();

    // var directionsLayer = L.mapbox.directions.layer(directions).addTo(map);

    // var directionsInputControl = L.mapbox.directions.inputControl('inputs', directions).addTo(map);


    // var directionsErrorsControl = L.mapbox.directions.errorsControl('errors', directions).addTo(map);

    // var directionsRoutesControl = L.mapbox.directions.routesControl('routes', directions).addTo(map);

    // var directionsInstructionsControl = L.mapbox.directions.instructionsControl('instructions', directions).addTo(map);

    var date = $('#dp_ride').fdatepicker({
      format: 'mm-dd-yyyy',
      disableDblClickSelection: true,
      todayBtn: true
    });

    var time = $('#dp_time_ride').fdatepicker({
      format: 'hh:ii',
      startView: 1,
      maxView: 1,
      pickTime: true
    });
});
