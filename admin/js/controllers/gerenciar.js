angular.module('site').controller('gerenciarCtrl', function($scope, $http, $localStorage){

    let urlBase = "http://localhost:5000/";
    function inicio(){
        $http.get(urlBase+'buscaTodos').then(
            function(resposta){
                let tam = resposta.data.result.length;
                if (tam == 0){
                    $scope.aviso = "Não há vídeos. ";
                    $scope.mensagem = "Nada por aqui!";
                }

                $scope.videos = resposta.data.result;
            },
            function(erro){
                $scope.erro = 'Ixi, algo deu errado!';
            }
        );
    }

    inicio();

    $scope.atualizaVideo = (id) => {
        window.location.assign('#!/atualizar/'+id);
        window.localStorage.setItem('funcao', 'atualizar')
    }

    $scope.deletaVideo = (id) => {
        let url = urlBase+"deletaVideo/";

        $http.delete(url+id).then(
            function(resposta){
                $scope.deleted = "Deletado item com ID: "+id;
                inicio();
            },
            function(erro){
                // console.log(erro);
            }
        );
    }

    $scope.buscar = (termo) =>{
        try {
            if(termo != undefined && termo.toString() != ""){
                    $http.get(urlBase+"buscaResultados/"+termo).then(
                        function(resposta){
                            // console.log(resposta.data.result);
                            $scope.videos = resposta.data.result;
                        },
                        function(erro){
                            console.log(erro);
                        }
                    );
            }else{
                inicio();
            }
        } catch (error) {
            inicio();
        }
    }

    $scope.logout = () => {
        delete $localStorage.token;
        window.location.assign("#!/login");
    }
});