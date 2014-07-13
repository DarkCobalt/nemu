var user = 'root';
var grupa = 1;
var app = angular.module('System', [ 'ngCookies', 'ngResource', 'ngSanitize', 'ngRoute'])

app.service('djangoAuth', function djangoAuth($q, $http, $cookies) {
    var service = {
        'API_URL': '/rest-auth',
        'use_session': true,
        'authenticated': null,
        'request': function(args) {
            if($cookies.token){
                $http.defaults.headers.common.Authorization = 'Token ' + $cookies.token;
            }
            params = args.params || {}
            args = args || {};
            var deferred = $q.defer(),
                url = this.API_URL + args.url,
                method = args.method || "GET",
                params = params,
                data = args.data || {};
            $http({
                url: url,
                withCredentials: this.use_session,
                method: method.toUpperCase(),
                headers: {'X-CSRFToken': $cookies['csrftoken']},
                params: params,
                data: data
            })
            .success(angular.bind(this,function(data, status, headers, config) {
                deferred.resolve(data, status);
            }))
            .error(angular.bind(this,function(data, status, headers, config) {
                if(data){
                    data.status = status;
                }
                if(status == 0){
                    if(data == ""){
                        data = {};
                        data['status'] = 0;
                        data['non_field_errors'] = ["Could not connect. Please try again."];
                    }
                    if(data == null){
                        data = {};
                        data['status'] = 0;
                        data['non_field_errors'] = ["Server timed out. Please try again."];
                    }
                }
                deferred.reject(data, status, headers, config);
            }));
            return deferred.promise;
        },
        'register': function(username,password,email){
            return this.request({
                'method': "POST",
                'url': "/register/",
                'data':{
                    'username':username,
                    'password':password,
                    'email':email
                }
            });
        },
        'login': function(username,password){
            var djangoAuth = this;
            return this.request({
                'method': "POST",
                'url': "/login/",
                'data':{
                    'username':username,
                    'password':password
                }
            }).then(function(data){
                if(!djangoAuth.use_session){
                    $http.defaults.headers.common.Authorization = 'Token ' + data.key;
                    $cookies.token = data.key;
                }
            });
        },
        'logout': function(){
            return this.request({
                'method': "GET",
                'url': "/logout/"
            }).then(function(data){
                delete $http.defaults.headers.common.Authorization;
                delete $cookies.token;
            });
        },
        'changePassword': function(password1,password2){
            return this.request({
                'method': "POST",
                'url': "/password/change/",
                'data':{
                    'new_password1':password1,
                    'new_password2':password2
                }
            });
        },
        'resetPassword': function(email){
            return this.request({
                'method': "POST",
                'url': "/password/reset/",
                'data':{
                    'email':email
                }
            });
        },
        'profile': function(){
            return this.request({
                'method': "GET",
                'url': "/user/"
            });
        },
        'updateProfile': function(first_name,last_name,email){
            return this.request({
                'method': "POST",
                'url': "/user/",
                'data':{
                    'user':{
                        'first_name':first_name,
                        'last_name':last_name,
                        'email':email
                    }
                }
            });
        },
        'verify': function(key){
            return this.request({
                'method': "GET",
                'url': "/verify-email/"+key+"/"
            });
        },
        'confirmReset': function(code1,code2,password1,password2){
            return this.request({
                'method': "POST",
                'url': "/password/reset/confirm/"+code1+"/"+code2+"/",
                'data':{
                    'new_password1':password1,
                    'new_password2':password2
                }
            });
        },
        'initialize': function(url, sessions, model){
            console.log('initialize');
            this.API_URL = url;
            this.use_session = sessions;
            if(model){
                model.authenticated = null;
                if(this.authenticated == null){
                    var djangoAuth = this;
                    this.profile().then(function(){
                        djangoAuth.authenticated = true;
                        model.authenticated = true;
                    },function(){
                        djangoAuth.authenticated = false;
                        model.authenticated = false;
                    });
                }else{
                    model.authenticated = this.authenticated;
                }
                model.setAuth = function(auth){
                    model.authenticated = auth;
                }
            }
        }

    }
    return service;
  });
app.service('Validate', function Validate() {
    return {
        'message': {
            'minlength': 'This value is not long enough.',
            'maxlength': 'This value is too long.',
            'email': 'A properly formatted email address is required.',
            'required': 'This field is required.'
        },
        'more_messages': {
            'demo': {
                'required': 'Here is a sample alternative required message.'
            }
        },
        'check_more_messages': function(name,error){
            return (this.more_messages[name] || [])[error] || null;
        },
        validation_messages: function(field,form,error_bin){
            var messages = [];
            for(var e in form[field].$error){
                if(form[field].$error[e]){
                    var special_message = this.check_more_messages(field,e);
                    if(special_message){
                        messages.push(special_message);
                    }else if(this.message[e]){
                        messages.push(this.message[e]);
                    }else{
                        messages.push("Error: " + e)
                    }
                }
            }
            var deduped_messages = [];
            angular.forEach(messages, function(el, i){
                if(deduped_messages.indexOf(el) === -1) deduped_messages.push(el);
            });
            if(error_bin){
                error_bin[field] = deduped_messages;
            }
        },
        'form_validation': function(form,error_bin){
            for(var field in form){
                if(field.substr(0,1) != "$"){
                    this.validation_messages(field,form,error_bin);
                }
            }
        }
    }
});


app.config(['$routeProvider','$locationProvider', function($routeProvider,$locationProvider) {
    //$locationProvider.html5Mode(true);
    $routeProvider.
      when('/', {
       templateUrl : '/static/pages/home.html'
      }).when('/register', {
        templateUrl: '/static/pages/auth/register.html',
        controller  : 'RegisterCtrl'
      })
      .when('/passwordReset', {
        templateUrl: '/static/pages/auth/passwordreset.html',
        controller  : 'PasswordresetconfirmCtrl'
      })
      .when('/passwordResetConfirm/:firstToken/:passwordResetToken', {
        templateUrl: '/static/pages/auth/passwordresetconfirm.html',
        controller  : 'PasswordresetconfirmCtrl'
      })
      .when('/login', {
        templateUrl: '/static/pages/auth/login.html',
        controller  : 'LoginCtrl'
      })
      .when('/verifyEmail/:emailVerificationToken', {
        templateUrl: '/static/pages/auth/verifyemail.html',
        controller  : 'VerifyemailCtrl'
      })
      .when('/logout', {
        templateUrl: '/static/pages/auth/logout.html',
        controller  : 'LogoutCtrl'
      })
      .when('/userProfile', {
        templateUrl: '/static/pages/auth/userprofile.html',
        controller  : 'UserprofileCtrl'
      })
      .when('/passwordChange', {
        templateUrl: '/static/pages/auth/passwordchange.html',
        controller  : 'PasswordchangeCtrl'
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
    });
});

//auth controler

app.controller('LoginCtrl', function ($scope, djangoAuth, Validate) {
    $scope.model = {'username':'','password':''};
  	$scope.complete = false;
    $scope.login = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.login($scope.model.username, $scope.model.password)
        .then(function(data){
        	$scope.complete = true;
            window.location = '/';
            $scope.setAuth(true);
        },function(data){
        	// error case
        	$scope.error = data.error;
        });
      }
    }
  });
app.controller('LogoutCtrl', function ($scope, $location, djangoAuth) {
    djangoAuth.logout();
    $scope.setAuth(false);
  });
app.controller('PasswordchangeCtrl', function ($scope, djangoAuth, Validate) {
    $scope.model = {'new_password1':'','new_password2':''};
  	$scope.complete = false;
    $scope.changePassword = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.changePassword($scope.model.new_password1, $scope.model.new_password2)
        .then(function(data){
        	// success case
        	$scope.complete = true;
        },function(data){
        	// error case
        	$scope.errors = data;
        });
      }
    }
  });
app.controller('PasswordresetCtrl', function ($scope, djangoAuth, Validate) {
    $scope.model = {'email':''};
  	$scope.complete = false;
    $scope.resetPassword = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.resetPassword($scope.model.email)
        .then(function(data){
        	// success case
        	$scope.complete = true;
        },function(data){
        	// error case
        	$scope.errors = data;
        });
      }
    }
  });
app.controller('PasswordresetconfirmCtrl', function ($scope, $routeParams, djangoAuth, Validate) {
    $scope.model = {'new_password1':'','new_password2':''};
  	$scope.complete = false;
    $scope.confirmReset = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.confirmReset($routeParams['firstToken'], $routeParams['passwordResetToken'], $scope.model.new_password1, $scope.model.new_password2)
        .then(function(data){
        	// success case
        	$scope.complete = true;
        },function(data){
        	// error case
        	$scope.errors = data;
        });
      }
    }
  });
app.controller('RegisterCtrl', function ($scope, djangoAuth, Validate) {
  	$scope.model = {'username':'','password':'','email':''};
  	$scope.complete = false;
    $scope.register = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.register($scope.model.username,$scope.model.password,$scope.model.email)
        .then(function(data){
        	// success case
        	$scope.complete = true;
        },function(data){
        	// error case
        	$scope.errors = data.user;
        });
      }
    }
  });
app.controller('UserprofileCtrl', function ($scope, djangoAuth, Validate) {
    $scope.model = {'first_name':'','last_name':'','email':''};
  	$scope.complete = false;
  	djangoAuth.profile().then(function(data){
  		$scope.model = data.user;
  	});
    $scope.updateProfile = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.updateProfile($scope.model.first_name, $scope.model.last_name, $scope.model.email)
        .then(function(data){
        	// success case
        	$scope.complete = true;
        },function(data){
        	// error case
        	$scope.error = data;
        });
      }
    }
  });
app.controller('VerifyemailCtrl', function ($scope, $routeParams, djangoAuth) {
    djangoAuth.verify($routeParams["emailVerificationToken"]).then(function(data){
    	$scope.success = data.success;
    },function(data){
    	$scope.failure = data.errors;
    });
  });
