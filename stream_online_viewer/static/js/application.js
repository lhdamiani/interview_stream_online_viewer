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


    var data = [];
    var dataset;
    var totalPoints = 10;
    var updateInterval = 1000;
    var now = new Date().getTime();
    var timer;
    $(window).bind('resize', function() {
    clearTimeout(timer);
    timer = setTimeout(function(){ $(window).resize(); }, 250);
    });

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
    
                if (date.getSeconds() % 4 == 0) {
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
            min: 0,
            max: 10,        
            tickSize: 1,
            tickFormatter: function (v, axis) {
                if (v % 1 == 0) {
                    return v;
                } else {
                    return "";
                }
            },
            axisLabel: "Info",
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
    var numbers_received = [];

    function update(){
        $.plot($("#flot-placeholder1"), dataset, options);
        
    }

    //receive details from server
    socket.on('newnumber', function(msg) {
        // console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
            data.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }
        $('#log').html(numbers_string);
        

        data.push([now += updateInterval, msg.number])
        dataset = [
            { label: "Info", data: data, color: "#00FF00" }
        ];
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