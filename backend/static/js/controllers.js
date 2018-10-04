'use strict';

/* Controllers */

function IndexController($scope) {
	// console.log("index controller")
}

function LogoutController($location, $window) {
	// console.log("logout controller");
	window.location.href = '/';
	
}

function AboutController($scope) {
	// console.log("about controller");
}
