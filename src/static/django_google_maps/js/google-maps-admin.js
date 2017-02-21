
/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="address" id="id_address" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/

function enter_press(e){
                if(e.keyCode == 13){
                    console.log("Hello");
                    search($('#searchbar').val());
                }
            }

function initAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
      (document.getElementById('id_address')),
      {types: ['geocode']});

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  $("#id_address").attr({"placeholder": ""});
  autocomplete.addListener('place_changed', fillInAddress);
  $("#address-search-button").on("click", function(){
      fillInAddress();
  });
}

function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();
    document.getElementById("id_address").value = place.formatted_address;
    googlemap.updateGeolocation(place.geometry.location);
    googlemap.centerMarker(place.geometry.location);
}

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}



function googleMapAdmin() {

    var geocoder = new google.maps.Geocoder();
    var map;
    var marker;

    var self = {
        initialize: function() {
            var lat = 0;
            var lng = 0;
            var zoom = 2;
            // set up initial map to be world view. also, add change
            // event so changing address will update the map
            existinglocation = self.getExistingLocation();
            if (existinglocation) {
                lat = existinglocation[0];
                lng = existinglocation[1];
                zoom = 18;
            }

            var latlng = new google.maps.LatLng(lat,lng);
            var myOptions = {
              zoom: zoom,
              center: latlng,
              mapTypeId: google.maps.MapTypeId.MAP
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            if (existinglocation) {
                self.setMarker(latlng);
            }
            
            $("#id_address").on("change", function(){
                  self.codeAddress();
            });
            $("#id_geolocation").change(function() {self.decodeAdress();});
        },

        getExistingLocation: function() {
            var geolocation = $("#id_geolocation").val();
            if (geolocation) {
                return geolocation.split(',');
            }
        },

        codeAddress: function() {
            var address = $("#id_address").val();
            geocoder.geocode({'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var latlng = results[0].geometry.location;
                    var address = results[0].formatted_address;
                    map.setCenter(latlng);
                    map.setZoom(18);

                    self.setMarker(latlng);
                    self.updateGeolocation(latlng);
                    self.updateAddress(address);
                } else {
                    $("#id_geolocation")
                        .val("Invalid address or no results");
                }
            });
        },
        
        centerMarker: function(latlng){
            map.setCenter(latlng);
            map.setZoom(18);

            self.setMarker(latlng);
        },

        setMarker: function(latlng) {
            if (marker) {
                self.updateMarker(latlng);
            } else {
                self.addMarker({'latlng': latlng, 'draggable': true});
            }
        },

        addMarker: function(Options) {
            marker = new google.maps.Marker({
                map: map,
                position: Options.latlng
            });

            var draggable = Options.draggable || false;
            if (draggable) {
                self.addMarkerDrag(marker);
            }
        },

        addMarkerDrag: function() {
            marker.setDraggable(true);
            google.maps.event.addListener(marker, 'dragend', function(new_location) {
                self.updateGeolocation(new_location.latLng);
                $("#id_geolocation").trigger("change");
            });
        },

        updateMarker: function(latlng) {
            marker.setPosition(latlng);
        },

        updateGeolocation: function(latlng) {
            $("#id_geolocation")
                .val(latlng.lat() + "," + latlng.lng());
        },
        
        updateAddress: function(address) {
            $("#id_address")
                .val(address);
        },
        
        decodeAdress: function() {
            var input = document.getElementById('id_geolocation').value;
            var latlngStr = input.split(',', 2);
            var latlng = {lat: parseFloat(latlngStr[0]), lng: parseFloat(latlngStr[1])};

            geocoder.geocode({'location': latlng}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var latlng = results[0].geometry.location;
                    var address = results[0].formatted_address;
                    map.setCenter(latlng);
                    map.setZoom(18);

                    self.setMarker(latlng);
                    self.updateGeolocation(latlng);
                    self.updateAddress(address);
                } else {
                }
            });
        }

    }

    return self;
}
var googlemap;
$(document).ready(function() {
    initAutocomplete();
    googlemap = googleMapAdmin();
    $("#id_address").after('\
        <a id="address-search-button" style="z-index: 1000;position: absolute;right: 15px;top: 15px;"><i class="material-icons" style="font-size: 18px;">search</i></a>\
    ');
    googlemap.initialize();
    
});