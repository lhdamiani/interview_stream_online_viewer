$(document).ready(function(){

    $('input.autocomplete').autocomplete({
      data: {
        "Apple": null,
        "Microsoft": null,
        "Google": 'https://placehold.it/250x250'
      },
    });

    $('.collapsible').collapsible();
    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $(".dropdown-trigger").dropdown();
    $('.materialboxed').materialbox();


    var data = [];
    var dataset;
    var updateInterval = 1000;
    var now = new Date().getTime();
    var timer;
    // resizes the window range of the interesting plot with beam energy
    $(window).bind('resize', function() {
    clearTimeout(timer);
    timer = setTimeout(function(){ $(window).resize(); }, 250);
    });

    // Options for the interesting plot with beam energy
    var options = {
        series: {
            lines: {
                show: true,
                lineWidth: 1.2,
                fill: true
            }
        },
        xaxis: {
            mode: "time",
            tickSize: [2, "second"],
            tickFormatter: function (v, axis) {
                var date = new Date(v);
    
                if (date.getSeconds() % 10 == 0) {
                    var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
                    var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
                    var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
    
                    return hours + ":" + minutes + ":" + seconds;
                } else {
                    return "";
                }
            },
            axisLabel: "Time",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 10
        },
        yaxis: {
            min: 5,
            max: 6,        
            tickSize: 0.25,
            tickFormatter: function (v, axis) {
                if (v % .25 == 0) {
                    return v;
                } else {
                    return "";
                }
            },
            axisLabel: "Beam energy",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        },
        legend: {        
            labelBoxBorderColor: "#fff",
            show: false
        },
        grid: {                
            backgroundColor: "#fff",
            tickColor: "#008040",
            hoverable: true
        }
    };

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var messages_received = [];

    // Update the interesting plot with beam energy
    function update(){
        $.plot($("#flot-placeholder1"), dataset, options);
        
    }

    //receive details from server
    socket.on('newmessage', function(msg) {
        messages_received.push(msg.number_of_received_messages);
        // Collapsible image details html
        imgDetails = "Image size x:"+ msg.image_size_x.toString() +"(originally) <br> Image size y:" + msg.image_size_y.toString() +"(originally)"
        $('#ImgDetails').html(imgDetails);
        // Collapsible connection details html
        connectionDetails = "Total bytes received: "+msg.total_bytes_received.toString()+ "<br>Numbers of received messages: " +msg.number_of_received_messages.toString()
        $('#ConnectionDetails').html(connectionDetails);
        // Collapsible metadata details html
        metadataDetails = "Beam energy:"+ msg.beam_energy.toString() +"<br> Repetition rate:" + msg.repetition_rate.toString()
        $('#MetadataDetails').html(metadataDetails);
        // Src for the image from server
        valueTime = new Date().getTime()
        $("#imgFromServer").attr("src","/static/images/stream.png?t=" + valueTime);
        // Updates the data for the interesting plot with beam energy
        if (messages_received.length >= 15){
            data.shift();
        } 
        data.push([now += updateInterval, msg.beam_energy])
        dataset = [{ label: "Info", data: data, color: "#00FF00" }];
        update()
        setTimeout(update, updateInterval);
    });

});



(function () {
    'use strict';
  
    angular.module('StreamApp', [])
  
    .controller('StreamController', ['$scope', '$log', '$http',
      function($scope, $log, $http) {
      }
    ]);
  
  }());

'use strict';

angular.module('StreamApp', ['angularFlaskServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/landing.html',
			controller: IndexController
		})
		.when('/about', {
			templateUrl: '',
			controller: AboutController
		})
		.when('/logout', {
			templateUrl: '',
			controller: LogoutController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);	

	}]);

	$(function() {
		setTimeout(function(){
			$(".message_flash").hide('blind', {}, 500)
		},1000);
	})