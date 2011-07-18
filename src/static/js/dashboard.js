// Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
// This file is part of T-Mon.

// T-Mon is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// T-Mon is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public License
// along with T-Mon. If not, see <http://www.gnu.org/licenses/>.

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
                          icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + positions[i]["count"] + "|FFFF00|000000"
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
    this.locked = false;
    this.last_request = null;
};

ChartController.prototype.updateData = function(){
    if (this.locked) {
        return;
    }
    
    var self = this;
    var onSuccess = function(received) {
                        self.data = received.results;
                        var real_data = self.label != ""? [ { label: self.label,  data: self.data } ]: self.data;
                        $.plot(self.canvas, real_data, self.options);
                        self.unlock();
                    };
    this.last_request = $.ajax(this.data_source, {
        method: 'GET',
        dataType: 'json',
        success: onSuccess
    });
    this.lock();
};

ChartController.prototype.setAutoRefresh = function(interval) {
    var callback = Delegate.create(this, this.updateData);
    this.inverval_id = setInterval(callback, interval);
};

ChartController.prototype.clearAutoRefresh = function(interval) {
    clearInterval(this.inverval_id);
    if (this.locked) { 
        this.last_request.abort();
        this.unlock;
    }
};

ChartController.prototype.lock = function(){
    this.locked = true;
};

ChartController.prototype.unlock = function(){
    this.locked = false;
};

ChartController.prototype.clearData = function(){
    this.data = [];
};

ChartController.prototype.switchSource = function(new_source, label) {
    showLoadingImage(this.canvas)
    this.data_source = new_source;
    this.clearData();
    this.updateData();    
    this.label = label;
};


// Lists
// -----------------------------------------------------------------------------

var ListController;
ListController = function(canvas_id, data_source){
    this.canvas = $("#" + canvas_id);
    this.data_source = data_source;
    this.data = [];
    this.updateData();
    this.interval_id = null;
};

ListController.prototype.updateData = function(){
    var self = this;
    var onSuccess = function(received) {
                        self.data = received.results;
                        self.canvas.empty();
                        self.canvas.html("<ol>");
                        var country_list = self.canvas.find("ol");
                        for (var res in self.data) {
                            var obj = self.data[res];
                            for (var country in obj) {                                
                                country_list.append("<li><b>" + country + "</b>: " + obj[country] + "</li>");
                            }
                        }                        
                    };
    $.ajax({
        url: this.data_source,
        method: 'GET',
        dataType: 'json',
        success: onSuccess
    });
};

ListController.prototype.setAutoRefresh = function(interval) {
    var callback = Delegate.create(this, this.updateData);
    this.inverval_id = setInterval(callback, interval);
};

ListController.prototype.clearAutoRefresh = function(interval) {
    clearInterval(this.inverval_id);
};

ListController.prototype.clearData = function(){
    this.data = [];
};

// Application
// -----------------------------------------------------------------------------
var Application = {};
Application = function(e){
    
    this.map = new MapController("map_canvas");

    this.users_per_country = new ListController("per_country", 
                                                 "/" + webservice_id + "/data/users/country");
                                                 
    this.users_per_city = new ListController("per_city", 
                                               "/" + webservice_id + "/data/users/city");
    
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
                                              yaxes: [ { min: 0 } ], 
                                              legend: { position: 'nw' } 
                                            },
                                            "requests per second" );


};

Application.prototype.setRealtime = function() {
    this.req_per_sec.setAutoRefresh(1000);
    this.map.setAutoRefresh(5000);
    this.users_per_country.setAutoRefresh(60000);
    this.users_per_city.setAutoRefresh(60000);
};

Application.prototype.clearRealtime = function() {
    this.req_per_sec.clearAutoRefresh();
};

Application.prototype.changeResolution = function(resolution, count) {
    this.req_per_sec.switchSource("/" + webservice_id + "/data/requests/" + resolution + "/" + count, "requests per " + resolution);
};
var app;
document.addEventListener("DOMContentLoaded", function(e){
        app = new Application(e);
        app.setRealtime();

        $('#cbo_request_count_per').change(function() {
            var count = Number($('#txt_timespan').val());
            if(count > 0){
                var res = $(this).val();
                app.changeResolution(res, count);
            }
        });
        
        $('#txt_timespan').keydown(function(e) {
            var code = (e.keyCode ? e.keyCode : e.which);
            if(code == 13 || code == 9) { //Enter keycode
                var count = Number($('#txt_timespan').val());
                var res = $('#cbo_request_count_per').val();
                if(count > 0) {
                    app.changeResolution(res, count);
                }
            }
        });
        $('#btn_change_resolution').click(function() {
            var count = Number($('#txt_timespan').val());
            if(count > 0) {
                var res = $('#cbo_request_count_per').val();
                app.changeResolution(res, count);
            }
        });
        $('#lnk_show_secret').click(function(e) {
            e.preventDefault();
            var visibility = $('#infobox').css('display');
            $('#infobox').css('display', visibility == 'block'? 'none': 'block');
        });
    }, false);

