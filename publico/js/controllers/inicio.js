angular.module('site').controller('inicioCtrl', function($scope, $http){

    let urlBase = "http://localhost:5000/";

    $http.get(urlBase+"buscaInicio").then(
        function(resposta){
            $scope.videos = resposta.data.result;
        },
        function(erro){
            console.log(erro);
        }
    );
});