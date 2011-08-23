// Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
// This file is part of T-Mon.

// T-Mon is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// T-Mon is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with T-Mon. If not, see <http://www.gnu.org/licenses/>.

var markesArray = [];

function round(number,X) {
// rounds number to X decimal places, defaults to 2
    X = (!X ? 2 : X);
    return Math.round(number * Math.pow(10, X)) / Math.pow(10, X);
};

function showLoadingImage(element){
    element.empty().html('<img src="/static/loader.gif" class="loader" />');
};

function drawChart(canvas, data, options){
    if(data != undefined) {
        canvas.empty();
        $.plot(canvas, data, options);
    }
};

function showTooltip(x, y, contents) {
    $('<div id="tooltip">' + contents + '</div>').css( {
        top: y + 5,
        left: x + 5,
        color: "black",
        position: 'absolute',
        display: 'none',
        border: '1px solid darkgray',
        padding: '2px',
        'background-color': 'white',
        'border-radius': '4px',
        opacity: 0.80
    }).appendTo("body").fadeIn(150);
};

function reportProgress(canvas, timeout) {
    canvas.progressbar('value', 100);
    var i = timeout;
    function decrement() {
        canvas.progressbar('value', 100 * i / timeout);
        i--;
        if(i > 1)
            setTimeout(decrement, 1000);
    };
    setTimeout(decrement, 1000);
};
    
// Google Map
// -----------------------------------------------------------------------------

var MapController = function(canvas_id){
    this.canvas = document.getElementById(canvas_id);
    this.markers = [];
    this.options = {
        zoom: 2,
        center: new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    this.inverval_id = null;
    this.locked = false;
    this.last_request = null;
    this.initMapWithLocation();
};

MapController.prototype.initMapWithLocation = function() {
    var self = this;
    var success = function(e) {
        self.options.center = new google.maps.LatLng(e.coords.latitude, e.coords.longitude);
        
        self.map = new google.maps.Map(self.canvas, self.options);
        google.maps.event.addListenerOnce(self.map, 'idle', function(e){
                self.onMapLoad();
            });
    };
    
    var error = function(e) {
        self.map = new google.maps.Map(self.canvas, self.options);
        google.maps.event.addListenerOnce(self.map, 'idle', function(e){
                self.onMapLoad();
            });
    };
    navigator.geolocation.getCurrentPosition(success, error);
};

MapController.prototype.onMapLoad = function(){
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
    if (this.locked) {
        return;
    }
    var self = this;
    var bounds = this.map.getBounds();
    var southWest = bounds.getSouthWest();
    var northEast = bounds.getNorthEast();
    var zoom = this.map.getZoom();

    var onSuccess = function(data) {
              var positions = data["results"];
              if(positions != undefined) {
                  self.deleteMarkers();
                  
                  var pos = null;
                  
                  for(var i = 0; i < positions.length; i++) {   
                      var marker = new google.maps.Marker({
                              position: new google.maps.LatLng(positions[i]["lat"], positions[i]["lng"]),
                              title: "Origin of one or more requests!",
                              icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + positions[i]["count"] + "|FFFF00|000000"
                          });
                      marker.setMap(self.map);
                      self.markers.push(marker);
                  }
              }
              self.unlock();
          };
          
    this.last_request = $.ajax(this.getURL(northEast, southWest), {
        method: 'GET',
        dataType: 'json',
        success: onSuccess,
        error: self.unlock
    });
    this.lock();
};

MapController.prototype.setAutoRefresh = function(interval) {
    var callback = Delegate.create(this, this.updateMarkers);
    this.inverval_id = setInterval(callback, interval);
};

MapController.prototype.clearAutoRefresh = function(interval) {
    clearInterval(this.inverval_id);
    if (this.locked) { 
        this.last_request.abort();
        this.unlock;
    }
};

MapController.prototype.enlarge = function(canvas_id){
    $(this.canvas).empty();
    this.large_canvas = document.getElementById(canvas_id);
    this.map = new google.maps.Map(this.large_canvas, this.options); 
    
    this.updateMarkers();
};

MapController.prototype.shrink = function(){
    $(this.large_canvas).empty();
    this.map = new google.maps.Map(this.canvas, this.options); 
    this.updateMarkers();
};

MapController.prototype.lock = function(){
    this.locked = true;
};

MapController.prototype.unlock = function(){
    this.locked = false;
};


// Charts
// -----------------------------------------------------------------------------

var ChartController = function(canvas_id, data_source, options, label){
    this.canvas = $("#" + canvas_id);
    this.data_source = data_source;
    this.data = [];
    this.options = options;

    this.updateData();
    
    this.interval_id = null;
    this.label = label;
    this.locked = false;
    this.last_request = null;
    this.drawable_data = [];
};

ChartController.prototype.updateData = function(){
    if (this.locked) {
        return;
    }
    
    var self = this;
    var onSuccess = function(received) {
                        self.data = received.results;
                        self.drawable_data = self.label != ""? [ { label: self.label,  data: self.data } ]: self.data;
                        drawChart(self.canvas, self.drawable_data, self.options);
                        self.unlock();
                    };
    this.last_request = $.ajax(this.data_source, {
        method: 'GET',
        dataType: 'json',
        success: onSuccess,
        error: self.unlock
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

ChartController.prototype.enlarge = function(canvas_id, options){
    drawChart($("#" + canvas_id), this.data, options);
};

ChartController.prototype.setHover = function(){
    var self = this;
    
    this.canvas.bind("plothover", function (event, pos, item) {
        if (item) {
            $("#tooltip").remove();
            
            var y = parseFloat(item.datapoint[1]);
            
            var label = item.series.label + ": " + y;
            if(self.options.series.hasOwnProperty('pie')) {
                label = item.series.label + ": " + parseFloat(item.series.percent).toFixed(2) + "%";
            }

            showTooltip(pos.pageX, pos.pageY, label);
        }
        else {
            $("#tooltip").remove();
        }
    });
};


// Lists
// -----------------------------------------------------------------------------

var ListController = function(canvas_id, data_source, progressbar_canvas){
    this.canvas = $("#" + canvas_id);
    this.data_source = data_source;
    this.data = [];
    this.interval_id = null;
    this.updateData();

    if(progressbar_canvas != "") {
        this.progressbar = $("#" + progressbar_canvas);
        this.progressbar.progressbar();
    }
};

ListController.prototype.updateData = function(){
    var self = this;
    var onSuccess = function(received) {
                        if(received.results != undefined) {
                            
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
                        }
                    };
    $.ajax({
        url: this.data_source,
        method: 'GET',
        dataType: 'json',
        success: onSuccess
    });
    
    if(this.interval_id != null && this.progressbar != undefined) {
        reportProgress(this.progressbar, this.interval);
    }
};

ListController.prototype.setAutoRefresh = function(interval) {
    var callback = Delegate.create(this, this.updateData);
    this.interval = interval / 1000;
    this.interval_id = setInterval(callback, interval);
    
    if(this.progressbar != undefined) {
        reportProgress(this.progressbar, this.interval);
    }
}

ListController.prototype.clearAutoRefresh = function(interval) {
    clearInterval(this.inverval_id);
    this.interval_id = null;
};

ListController.prototype.clearData = function(){
    this.data = [];
};

// Application
// -----------------------------------------------------------------------------

var Application = function(e){
    
    this.map = new MapController("map_canvas");

    this.users_per_country = new ListController("per_country", 
                                                 "/" + webservice_id + "/data/users/country",
                                                 "prg_country");
                                                 
    this.users_per_city = new ListController("per_city", 
                                               "/" + webservice_id + "/data/users/city",
                                               "prg_city");
    
    this.per_os = new ChartController("per_os", 
                                       "/" + webservice_id + "/data/users/os",  
                                       { series: { 
                                                    pie: { 
                                                            show: true, 
                                                            label: { show: false }, 
                                                            combine: {
                                                                color: '#999',
                                                                threshold: 0.03}
                                                    } }, 
                                         legend: { show: false },
                                         grid: { hoverable: true },
                                       },
                                       "");
                                       
    this.per_device = new ChartController("per_device", 
                                           "/" + webservice_id + "/data/users/device", 
                                           { series: { pie: { show: true, label: { show: false } } }, 
                                             legend: { show: false }, 
                                             grid: { hoverable: true } 
                                           },
                                           "");
                                           
    this.per_url = new ChartController("per_url", 
                                           "/" + webservice_id + "/data/users/url", 
                                           { series: { pie: { show: true, label: { show: false } } }, 
                                             legend: { show: false }, 
                                             grid: { hoverable: true } 
                                           },
                                           "");
                                           
    this.req_per_sec = new ChartController("requests", 
                                            "/" + webservice_id + "/data/requests/second/60", 
                                            { series: { lines: { show: true, fill: true } },
                                              grid: { hoverable: true }, 
                                              yaxes: [ { min: 0 } ], 
                                              legend: { show: false } 
                                            },
                                            "Requests/Second");
                                            
    this.per_os.setHover();
    this.per_device.setHover();
    this.per_url.setHover();
    this.req_per_sec.setHover();
                                            
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
    this.req_per_sec.switchSource("/" + webservice_id + "/data/requests/" + resolution + "/" + count, "Requests/" + resolution.charAt(0).toUpperCase() + resolution.slice(1));
};

var app;
document.addEventListener("DOMContentLoaded", function(e){
        app = new Application(e);
        app.setRealtime();

        //
        // GUI Events
        //
        $('#cbo_request_count_per').change(function() {
                var count = $('#cbo_timespan').val();
                var res = $(this).val();
                app.changeResolution(res, count);
        });
        
        $('#cbo_timespan').change(function() {
            var count = $(this).val();
            var res = $('#cbo_request_count_per').val();
            app.changeResolution(res, count);
        });
        
        $('#cbo_webservices').change(function() {
            var webservice = $(this).val();
            if(webservice != webservice_id) {
                window.location = "/view/dashboard/" + webservice;
            }
        });
        
        $('#lnk_information').click(
            function() {
                $("#dlg_information").dialog({
		            height: 180,
		            width: 330,
		            modal: true,
		            resizable: false,
		            title: "More about " + webservice_name,
	            }); 
            }
        );
        
        $('#os_enlarge').click(
            function() {
                $("#dlg_big_os").dialog({
		            height: 684,
		            width: 703,
		            resizable: false,
		            title: "Operating Systems",
		            modal: true,
		            create: function() {
		                app.per_os.enlarge("os_charting_area", 
		                    { series: { pie: { 
		                                       show: true, 
		                                       label: { 
		                                                radius: 3/4,
		                                                show: true,
	                                                    formatter: function(label, series){
                                                            return '<div class="large_chart_label"><b>' + label + '</b> (' + Math.round(series.percent) + '%)</div>';
                                                        }, 
                                                        threshold: 0.02,
                                               },
                                               combine: {
                                                    color: '#999',
                                                    threshold: 0.02
                                                }
                                        } 
                             }, 
                             legend: { show: false }
                           });
		            }
	            }); 
            }
        );
        
        $('#dev_enlarge').click(
            function() {
                $("#dlg_big_dev").dialog({
		            height: 684,
		            width: 703,
		            resizable: false,
		            title: "Devices",
		            modal: true,
		            create: function() {
		                app.per_device.enlarge("dev_charting_area", 
		                    { series: { pie: { 
		                                       show: true, 
		                                       label: { 
		                                                radius: 3/4,
		                                                show: true,
	                                                    formatter: function(label, series){
                                                            return '<div class="large_chart_label"><b>' + label + '</b> (' + Math.round(series.percent) + '%</div>';
                                                        }, 
                                                        threshold: 0.02,
                                               },
                                               combine: {
                                                    color: '#999',
                                                    threshold: 0.02
                                                }
                                        } 
                             }, 
                             legend: { show: false }
                           });
		            }
	            }); 
            }
        );
        
        $('#url_enlarge').click(
            function() {
                $("#dlg_big_url").dialog({
		            height: 684,
		            width: 703,
		            resizable: false,
		            title: "URLs",
		            modal: true,
		            create: function() {
		                app.per_url.enlarge("url_charting_area", 
		                    { series: { pie: { 
		                                       show: true, 
		                                       label: { 
		                                                radius: 3/4,
		                                                show: true,
	                                                    formatter: function(label, series){
                                                            return '<div class="large_chart_label"><b>' + label + '</b> (' + Math.round(series.percent) + '%</div>';
                                                        }, 
                                                        threshold: 0.02,
                                               },
//                                               combine: {
//                                                    color: '#999',
//                                                    threshold: 0.02
//                                                }
                                        } 
                             }, 
                             legend: { show: false }
                           });
		            }
	            }); 
            }
        );
    
        
        $('#map_enlarge').click(
            function() {
                $("#dlg_big_map").dialog({
		            height: 600,
		            width: 960,
		            minWidth: 300,
		            minHeight: 300,
		            resizable: true,
		            modal: true,
		            title: "Map",
		            
		            resizeStop: function(event, ui) { 
		                google.maps.event.trigger(app.map.map, 'resize')  
	                },
                    open: function(event, ui) { 
                        app.map.enlarge("big_map"); 
                        google.maps.event.trigger(app.map.map, 'resize'); 
                    },
                    close: function(event, ui) {
                        app.map.shrink(); 
                        google.maps.event.trigger(app.map.map, 'resize'); 
                    },
		           
	            }); 
            }
        );
        
        

    }, false);
         
