$(document).foundation();


window.addEventListener("load", function () {
  var numberOfWaypoints = 0;

  this.getEventMarkers = function() {
    // /read_user_events
    var url = "/read_all_events";
    this.features = [];
    //console.log(this);
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

  var markers = {
    origin: new L.marker([50.5, 30.5], {draggable: false}),
    destination: new L.marker([50.3, 30.5], {draggable: false}),
    waypoints: []
  };
  //console.log(markers);

  this.hasRoutes = function(map) {
     map.eachLayer(function (layer) {
        if(layer.drawRoute) {
          return true;
        }
    });
     return false;
  };

  this.clearRoutes = function(map) {
    map.eachLayer(function (layer) {
      //console.log(layer);
      if(layer.drawRoute) {
        map.removeLayer(layer);
      }
    });
  };

  this.refreshMap = function(map) {
    map.fire('click');
  }

  this.fadeMarkers = function(layer, opacity) {
    layer.eachLayer(function(marker) {
      //console.log(marker);
      marker.setOpacity(opacity);
    });
  };


  this.drawRoute = function(map, markers, rideInfo) {
    this.fadeMarkers(markerLayer, 0.5);

    this.clearRoutes(map);

    var directions = L.mapbox.directions();
    var directionsLayer = L.mapbox.directions.layer(directions);
    directionsLayer.addTo(map);

    directionsLayer.drawRoute = true;

    directionsLayer._directions.setOrigin(markers.origin);
    directionsLayer._directions.setDestination(markers.destination);
    var origin = directionsLayer._directions.getOrigin();
    var destination = directionsLayer._directions.getDestination();
    origin.geometry.coordinates = [markers.origin.getLatLng().lng, markers.origin.getLatLng().lat];
    destination.geometry.coordinates = [markers.destination.getLatLng().lng, markers.destination.getLatLng().lat];

    directionsLayer.routeLayer.options.style.color = "#ff0000";

    if(rideInfo.noob_friendly) {
      directionsLayer.routeLayer.options.style.color = "#00aa00";
    }
    directionsLayer.originMarker.options.draggable = false;
    directionsLayer.destinationMarker.options.draggable = false;
    var directionsRoutesControl = L.mapbox.directions.routesControl('routes', directions).addTo(map);

    map.fire('click');
  };
  var that = this;
  if(document.getElementById("profile-button") != null) {
    document.getElementById("profile-button").addEventListener("click", function (e) {
      e.preventDefault();
      //e.stopPropagation();
    });
  }

  if(document.getElementById("register-form") != null) {
    $("#register-form input").keypress(function(event) {
      if (event.which == 13) {
          event.preventDefault();
          $("#register-form").submit();
      }
    });
  }

  // if(document.getElementById("login-mock") != null) {
  //   document.getElementById("login-mock").addEventListener("click", function (e) {
  //     e.preventDefault();
  //     e.stopPropagation();
  //     method = "post"; // Set method to post by default if not specified.
  //     path = "/login";
  //     // The rest of this code assumes you are not using a library.
  //     // It can be made less wordy if you use one.
  //     var form = document.createElement("form");
  //     form.setAttribute("method", method);
  //     form.setAttribute("action", path);
  //     params = {username: "tapa", password:"tapa"};
  //     for(var key in params) {
  //         if(params.hasOwnProperty(key)) {
  //             var hiddenField = document.createElement("input");
  //             hiddenField.setAttribute("type", "hidden");
  //             hiddenField.setAttribute("name", key);
  //             hiddenField.setAttribute("value", params[key]);

  //             form.appendChild(hiddenField);
  //          }
  //     }

  //     document.body.appendChild(form);
  //     form.submit();
  //   });
  // }

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

  if(document.getElementById("telemetry-open-button") != null) {
    document.getElementById("telemetry-open-button").addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      // var opened = document.getElementById("create-ride").style.visibility;
      // document.getElementById("create-ride").style.visibility = "visible";
      document.getElementById("telemetry-holder").style.right = "0";
      setTimeout(1000);
      drawDegrees();
    });
  }
  var aboutUs = false;
  if(document.getElementById("aboutUs") != null) {
    document.getElementById("aboutUs").addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      if(aboutUs) {
        document.getElementById("lyubo").style['z-index'] = "30";
        document.getElementById("assen").style['z-index'] = "30";
        document.getElementById("rosen").style.left = "-404px";
        document.getElementById("lyubo").style.bottom = "-427px";
        document.getElementById("assen").style.bottom = "-423px";
        document.getElementById("drago").style.right = "-420px";
      } else {
        document.getElementById("drago").style.right = "-28px";
        setTimeout(function() {
          document.getElementById("lyubo").style.bottom = "40px";
          setTimeout(function() {
            document.getElementById("lyubo").style['z-index'] = "33";
          }, 1000);
          setTimeout(function() {
            document.getElementById("assen").style.bottom = "55px";
            setTimeout(function() {
              document.getElementById("assen").style['z-index'] = "33";
            }, 1000);
            setTimeout(function() {
              document.getElementById("rosen").style.left = "0";
            }, 200);
          }, 200);
        }, 200);
      }
      aboutUs = !aboutUs;
      // var opened = document.getElementById("create-ride").style.visibility;
      // document.getElementById("create-ride").style.visibility = "hidden";
    });
  }

  if(document.getElementById("telemetry-close-button") != null) {
    document.getElementById("telemetry-close-button").addEventListener("click", function (e) {
      e.preventDefault();
      // var opened = document.getElementById("create-ride").style.visibility;
      document.getElementById("telemetry-holder").style.right = "-520px";
      // document.getElementById("create-ride").style.visibility = "hidden";
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

  if(document.getElementById("view-close-button") != null) {
    document.getElementById("view-close-button").addEventListener("click", function (e) {
      e.preventDefault();
      // var opened = document.getElementById("view-ride").style.visibility;
      document.getElementById("view-ride-holder").style.right = "-500px";
      var route = {
        origin: new L.marker([0, 0], {draggable: false}),
        destination: new L.marker([0, 0], {draggable: false}),
        waypoints: []
      };

      var directions = L.mapbox.directions();
      //var layer = L.mapbox.directions.layer(directions);
      map.eachLayer(function (layer) {
        //console.log(layer);
        if(layer.drawRoute) {
          map.removeLayer(layer);
        }
      });

      //map.addLayer(markerLayer);
      that.fadeMarkers(markerLayer, 1);
      //$('#map').trigger('click');
      // document.getElementById("view-ride").style.visibility = "hidden";
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
        document.getElementById("expand-filter").style.top = "72px";
        document.getElementById("expand-filter").innerHTML = "&#xf078;";
        document.getElementById("expand-filter").setAttribute('data-expanded', "false");
      } else {
        setTimeout(function() {
          document.getElementById("filter-content").style.visibility = "visible";
        },1000);
        document.getElementById("expand-filter").style.top = "270px";
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
    var markerLayer = L.mapbox.featureLayer().addTo(map);

    // var directions = L.mapbox.directions();
    // var directionsLayer = L.mapbox.directions.layer(directions);
    // directionsLayer.addTo(map);

    var that = this;
    map.on('ready', function(e) {
      //console.log("that");
      //console.log(that);
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
                            'marker-color': '#88ff88',
                            'marker-symbol': 'embassy',
                            'id': feature.id
                          }
                        });
        });
        markerLayer.setGeoJSON({
          type: "FeatureCollection",
          features: features
        });
        markerLayer.on('click', function(e) {
          map.panTo(e.layer.getLatLng());
          //console.log(e);
          var marker = e.layer.feature;
          //console.log(marker);
          document.getElementById("view-ride-holder").style.right = "0";
          var url = "/read_event";
          var request = $.ajax({
            url: url,
            data: "id=" + marker.properties.id
          });
          request.done(function(result) {
            //console.log(result[0]);
            document.getElementById("view-header").innerHTML = result[0].name;
            document.getElementById("view-ride-start").innerHTML = result[0].start_point;
            document.getElementById("view-ride-finish").innerHTML = result[0].end_point;
            document.getElementById("view-ride-date").innerHTML = result[0].date;
            if(result[0].noob_friendly) {
              document.getElementById("nfSpan").style.visibility = "visible";
            } else {
              document.getElementById("nfSpan").style.visibility = "hidden";
            }
            var origin_coords = result[0].start_point_coordinates.split(',');
            var dest_coords = result[0].end_point_coordinates.split(',');
            var route = {
              origin: new L.marker([origin_coords[1], origin_coords[0]], {draggable: false}),
              destination: new L.marker([dest_coords[1], dest_coords[0]], {draggable: false}),
              waypoints: []
            };

            that.drawRoute(map, route, result[0]);
          }).fail(function(jqXHR, statusText) {
            console.log("failed to get event: " + statusText);
          });
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

    // var directionsInputControl = L.mapbox.directions.inputControl('inputs', directions).addTo(map);
    var cl = function(ev) {
      //console.log(ev);
    };
    map.on('click', cl);
    // console.log(markers.origin);
    // console.log(markers.destination);
    // markers.origin.addTo(map);
    // markers.destination.addTo(map);
    //console.log(directionsLayer);
    //this.drawRoute(map, markers);
    //var directionsErrorsControl = L.mapbox.directions.errorsControl('errors', directions).addTo(map);


    //var directionsInstructionsControl = L.mapbox.directions.instructionsControl('instructions', directions).addTo(map);

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

    var canvas = document.getElementById("gauge");
    var ctx = canvas.getContext("2d");
    var img = document.getElementById("gauge-img");
    var imgInfo = document.getElementById("gauge-info-img");
    var imgArrow = document.getElementById("gauge-arrow-img");
    var drawDegrees = function() {
      var degrees = 53;
      var i = 0;
      var refreshIntervalId = setInterval(function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 150, 261, 157);
        ctx.drawImage(imgInfo, 130, 65, 237, 163);
        ctx.translate(128, 153);
        ctx.scale(1, -1);
        ctx.translate(0, -100);
        ctx.rotate(-i*Math.PI/180);
        ctx.drawImage(imgArrow, 0, 0, 8, 91);
        ctx.rotate(i*Math.PI/180);
        ctx.translate(0, 100);
        ctx.scale(1, -1);
        ctx.translate(-128, -153);
        ctx.fillStyle = "#fff";
        ctx.font = "40px Verdana";
        ctx.fillText("" + i, 100, 255);
        ctx.font = "20px Verdana";
        ctx.fillText("o", 150, 230);
        if(i < degrees) {
          i++;
        } else {
          i = 0;
          clearInterval(refreshIntervalId);
        }
      }, 30);
    };

});
