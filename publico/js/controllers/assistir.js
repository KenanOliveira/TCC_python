angular.module('site').controller('assistirCtrl', function($scope, $http, $routeParams, $sce){

    $scope.trustSrc = function(src){
        return $sce.trustAsResourceUrl(src);
    }

    let urlBase = "http://localhost:5000/";

    function assistir(id){
        $http.get(urlBase+"buscaUnico/"+id).then(
            function(resposta){
                $scope.video = resposta.data.result;
            },
            function(erro){
                console.log(erro);
            }
        );
    }

    if($routeParams.id){
        assistir($routeParams.id);
    }
});