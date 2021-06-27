angular.module('site', ['ngRoute', 'ngSanitize', 'ngStorage']).config(['$routeProvider', '$httpProvider',
    function($routeProvider, $httpProvider){
        
        $routeProvider.when('/gerenciar', {
            templateUrl: 'partials/gerenciar.html',
            controller: 'gerenciarCtrl'
        });

        $routeProvider.when('/inserir', {
            templateUrl: 'partials/inserir.html',
            controller: 'videoCtrl'
        });

        $routeProvider.when('/atualizar/:id', {
            templateUrl: 'partials/atualizar.html',
            controller: 'videoCtrl'
        });

        $routeProvider.when('/cadastrar', {
            templateUrl: 'partials/cadastrar.html',
            controller: 'userCtrl'
        });

        $routeProvider.when('/login', {
            templateUrl: 'partials/login.html',
            controller: 'userCtrl'
        });

        $routeProvider.otherwise('/gerenciar');

        $httpProvider.interceptors.push(['$q', '$location', '$localStorage', function($q, $location, $localStorage){
            return {
                'request': function(config){
                    config.headers = config.headers || {};
                    if($localStorage.token){
                        config.headers.Authorization = 'Bearer '+$localStorage.token;
                        // console.log("ola")
                    }
                    return config;
                },
                'responseError': function(response){
                    if(response.status === 401 || response.status === 403){
                        delete $localStorage.token;
                        // console.log("oi")
                        $location.path('/login');
                    }
                    return $q.reject(response);
                }
            };
        }]);
    }
]).run(function($rootScope, $location, $localStorage){
    $rootScope.$on("$routeChangeStart", function(event, next){
        if($localStorage.token == null){
            if(next.templateUrl !== "partials/login.html"){
                // console.log("eae")
                $location.path("/login");
            }
        }
    });
});