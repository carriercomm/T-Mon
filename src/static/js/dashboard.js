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
    this.inverval_id = null;
    this.initMapWithLocation();
};

MapController.prototype.initMapWithLocation = function() {
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
//    var dragZoomHandler = function(e){
//        self.updateMarkers();
//    };
    //google.maps.event.addListener(this.map, 'dragend', dragZoomHandler);
    //google.maps.event.addListener(this.map, 'zoom_changed', dragZoomHandler);
    this.updateMarkers();
};

MapController.prototype.getURL = function(NE, SW){
    var url ="/" + webservice_id + "/data/users/locations/" + round(NE.lat(), 4) + "/" + round(NE.lng(), 4) + "/" + round(SW.lat(), 4) + "/" + round(SW.lng(), 4);
    return url;
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

    $.get(this.getURL(northEast, southWest), {},
          function(data) {
              self.deleteMarkers();
              var positions = data["results"];
              var pos = null;
              for(var i = 0; i < positions.length; i++) {   
                  var marker = new google.maps.Marker({
                          position: new google.maps.LatLng(positions[i]["lat"], positions[i]["lng"]),
                          title: "Origin of one or more requests!",
                          icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=!|FFFF00|000000"
                      });
                  marker.setMap(self.map);
                  self.markers[i] = marker;
              }
          });
};

MapController.prototype.setAutoRefresh = function(interval) {
    var callback = Delegate.create(this, this.updateMarkers);
    this.inverval_id = setInterval(callback, interval);
};

MapController.prototype.clearAutoRefresh = function(interval) {
    clearInterval(this.inverval_id);
};

// Charts
// -----------------------------------------------------------------------------

var ChartController;
ChartController = function(canvas_id, data_source, options, label){
    this.canvas = $("#" + canvas_id);
    this.data_source = data_source;
    this.data = [];
    this.options = options;
    this.updateData();
    this.interval_id = null;
    this.label = label;
};

ChartController.prototype.updateData = function(){
    //showLoadingImage(this.canvas)
    var self = this;
    var onSuccess = function(received) {
                        self.data = received.results;
                        var real_data = self.label != ""? [ { label: self.label,  data: self.data } ]: self.data;
                         $.plot(self.canvas, real_data, self.options);
                    };
    $.ajax({
        url: this.data_source,
        method: 'GET',
        dataType: 'json',
        success: onSuccess
    });
};

ChartController.prototype.setAutoRefresh = function(interval) {
    var callback = Delegate.create(this, this.updateData);
    this.inverval_id = setInterval(callback, interval);
};

ChartController.prototype.clearAutoRefresh = function(interval) {
    clearInterval(this.inverval_id);
};

ChartController.prototype.clearData = function(){
    this.data = []
};

ChartController.prototype.switchSource = function(new_source, label) {
    this.data_source = new_source;
    this.clearData();
    this.updateData();    
    this.label = label;
};


// Application
// -----------------------------------------------------------------------------
var Application = {};
Application = function(e){
    
    this.map = new MapController("map_canvas");
    
    this.per_os = new ChartController("per_os", 
                                       "/" + webservice_id + "/data/users/os",  
                                       { series: { pie: { show: true, innerRadius: 0.4 } }, 
                                         legend: { show: false } 
                                       },
                                       "");
                                       
    this.per_device = new ChartController("per_device", 
                                           "/" + webservice_id + "/data/users/device", 
                                           { series: { pie: { show: true, innerRadius: 0.4 } }, 
                                             legend: { show: false } 
                                           },
                                           "");
                                           
    this.req_per_sec = new ChartController("requests", 
                                            "/" + webservice_id + "/data/requests/second/60", 
                                            { series: { lines: { show: true, fill: true } }, 
                                              xaxes: [ { label: "time from now"} ],
                                              yaxes: [ { min: 0 } ] 
                                            },
                                            "requests per second" );

};

Application.prototype.setRealtime = function() {
    this.req_per_sec.setAutoRefresh(1000);
    this.map.setAutoRefresh(5000);
};

Application.prototype.clearRealtime = function() {
    this.req_per_sec.clearAutoRefresh();
};

Application.prototype.changeResolution = function(resolution, count) {
    this.req_per_sec.switchSource("/" + webservice_id + "/data/requests/" + resolution + "/" + count, "requests per " + resolution);
};

document.addEventListener("DOMContentLoaded", function(e){
        var app = new Application(e);
        app.setRealtime();
    }, false);

