angular.module('site').controller('buscaCtrl', function($scope, $http, $routeParams, $sce){

    $scope.pesquisar = (busca) => {
        window.location.assign("#!/pesquisar/"+busca);
    }

    let urlBase = "http://localhost:5000/";

    function buscarResultados(id){
        $http.get(urlBase+"buscaResultados/"+id).then(
            function(resposta){
                console.log(resposta.data.result);
                $scope.busca = resposta.data.result;
            },
            function(erro){
                console.log(erro);
            }
        );
    }

    if($routeParams.id){
        buscarResultados($routeParams.id);
    }
});