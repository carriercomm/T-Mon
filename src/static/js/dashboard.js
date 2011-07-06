var markesArray = [];

function round(number,X) {
// rounds number to X decimal places, defaults to 2
    X = (!X ? 2 : X);
    return Math.round(number * Math.pow(10, X)) / Math.pow(10, X);
}

function showLoadingImage(element){
    element.empty().html('<img src="/static/loader.gif" class="loader" />');
}

// Google Map
// -----------------------------------------------------------------------------
var MapController;
MapController = function(canvas_id){
    this.canvas = document.getElementById(canvas_id);
    this.markers = [];
    this.options = {
        zoom: 10,
        center: new google.maps.LatLng(0,0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    this.initMapWithLocation();
};

MapController.prototype.initMapWithLocation = function(){
    var self = this;
    var success = function(e) {
        self.options.center = new google.maps.LatLng(e.coords.latitude,
                                                     e.coords.longitude);
        self.map = new google.maps.Map(self.canvas, self.options);
        google.maps.event.addListenerOnce(self.map, 'idle', function(e){
                self.onMapLoad();
            });
    };
    var error = function(e){
        alert("You need to allow the browser to use your location.");
    };
    navigator.geolocation.getCurrentPosition(success,error);
};

MapController.prototype.onMapLoad = function(){
    var self = this;
    var dragZoomHandler = function(e){
        self.updateMarkers();
    };
    google.maps.event.addListener(this.map, 'dragend', dragZoomHandler);
    google.maps.event.addListener(this.map, 'zoom_changed', dragZoomHandler);
    this.updateMarkers();
};

MapController.prototype.getURL = function(NE, SW, zoom){
    var detail = 1;
    var current_context = 1;
    var url = "/api/zeitgeist/" + current_context + "/pos/" + round(NE.lat(), 6) + "/" + round(NE.lng(), 6) + "/" + round(SW.lat(), 6) + "/" + round(SW.lng(), 6) + "/" + detail;
    return "/";
};

MapController.prototype.deleteMarkers = function(){
    if (this.markers) {
        for (i in this.markers) {
            this.markers[i].setMap(null);
        }
        this.markers = [];
    }
};

MapController.prototype.updateMarkers = function(){
    var self = this;
    var bounds = this.map.getBounds();
    var southWest = bounds.getSouthWest();
    var northEast = bounds.getNorthEast();
    var zoom = this.map.getZoom();

    $.get(this.getURL(northEast,southWest,zoom), {},
          function(data) {
              self.deleteMarkers();
              var result = data["response"]["content"];
              var positions = result["positions"];
              var pos = null;
              for(var i = 0; i < positions.length; i++) {   
                  console.log(google.maps.MarkerImage("http://www.googlemapsmarkers.com/v1/"+ positions[i]["contextid"] + "/" + positions[i]["color"] + "/"))
                  var marker = new google.maps.Marker({
                          position: new google.maps.LatLng(positions[i]["latitude"], positions[i]["longitude"]),
                          title: positions[i]["count"] + " people are in context " + positions[i]["contextname"],
                          icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + positions[i]["count"] + "|"+ positions[i]["color"] + "|000000"
                      });
                  marker.setMap(self.map);
                  self.markers[i] = marker;
              }
          });
};

// Pie Chart
// -----------------------------------------------------------------------------

var ChartController;
ChartController = function(canvas_id, data_source, options){
    this.canvas = $("#" + canvas_id);
    this.data_source = data_source;
    this.data = [];
    this.options = options;
    this.updateData()
};

ChartController.prototype.updateData = function(){
    //showLoadingImage(this.canvas)
    var self = this;
    var onSuccess = function(received) {
                        self.data = received.results;
                        $.plot(self.canvas, self.data, self.options);
                    };
                    
    $.ajax({
        url: this.data_source,
        method: 'GET',
        dataType: 'json',
        success: onSuccess
    });
};

ChartController.prototype.refresh = function(interval){
    var callback = Delegate.create(this, this.updateData);
    setInterval(callback, interval);
};

ChartController.prototype.clearData = function(){
    this.data = []
};

var Application = {};
Application.init = function(e){
    //this.map = new MapController("map_canvas");
    this.per_os = new ChartController("per_os", "/" + webservice_id + "/data/users/os",  
                                       { series: { pie: { show: true, innerRadius: 0.4 } }, legend: { show: false } }  );
    this.per_device = new ChartController("per_device", 
                                           "/" + webservice_id + "/data/users/device", 
                                           { series: { pie: { show: true, innerRadius: 0.4 } }, legend: { show: false } } );
    this.req_per_sec = new ChartController("requests", "/" + webservice_id + "/data/requests/second/10", 
                        { series: { lines: { show: true }, points: { show: false } } });
    this.req_per_sec.refresh(500);
};

document.addEventListener("DOMContentLoaded", function(e){
        Application.init(e);
    }, false);

