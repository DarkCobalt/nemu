// grupa i user jest przypisany statycznie zmieni się to gdy będzie logowanie
var user = 'root';
var grupa = 1;
var app = angular.module('System', ['ngRoute'])

app.config(['$routeProvider','$locationProvider', function($routeProvider,$locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider.
      when('/', {
       templateUrl : '/static/pages/home.html'
      }).
      when('/projects', {
		templateUrl : '/static/pages/projects.html',
		controller  : 'projectsController'
	  }).
      when('/profile', {
		templateUrl : '/static/pages/profile.html',
		controller  : 'profileController'
	  }).
      otherwise({
        redirectTo: '/'
      });
    }]);

app.controller('projectsController', function($scope,$http) {
    $scope.projects = [];
    $http.get('/api/projects').success(function(data) {
        angular.forEach(data, function(value, key) {
            if(parseInt(value.group_id) == grupa) this.push(value);
         }, $scope.projects);
    });
});

app.controller('profileController', function($scope,$http) {
    $scope.user = [];
    $http.get('/api/users').success(function(data) {
        angular.forEach(data, function(value, key) {
            if(value.username == user) this.push(value);
         }, $scope.user);
        console.log($scope.user)
    });
});