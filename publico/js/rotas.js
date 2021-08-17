angular.module("site", ['ngRoute', 'ngSanitize']).config(['$routeProvider',
    function($routeProvider){

        $routeProvider.when('/inicio', {
            templateUrl: 'partials/inicio.html',
            controller: 'inicioCtrl'
        });

        $routeProvider.when('/assistir/:id', {
            templateUrl: 'partials/assistir.html',
            controller: 'assistirCtrl'
        });

        $routeProvider.when('/pesquisar/:id', {
            templateUrl: 'partials/pesquisar.html',
            controller: 'buscaCtrl'
        });

        $routeProvider.otherwise('/inicio');
    }
]);