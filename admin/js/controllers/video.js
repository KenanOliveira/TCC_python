angular.module('site').controller('videoCtrl', function($scope, $http, $routeParams){

    let urlBase = "http://localhost:5000/";

    function buscarInfo(id){
        $http.get(urlBase+"buscaUnico/"+id).then(
            function(resposta){
                let dados = resposta.data.result;
                // console.log(dados);
                $scope.titulo = dados.titulo;
                $scope.descricao = dados.descricao;
                $scope.link = dados.link;
                $scope.tags = dados.tags;
            },
            function(erro){
                $scope.erro = "Erro ao buscar as informações!";
            }
        );
    }

    $scope.atualizaVideo = () => {
        let tags = verificaTags($scope.tags);
        
        let dados = {
            titulo: $scope.titulo,
            link: $scope.link,
            descricao: $scope.descricao,
            tags: tags,
            atualizado: new Date()
        }

        $http.put(urlBase+"atualizaVideo/"+$routeParams.id, JSON.stringify(dados)).then(
            function(resposta){
                $scope.mensagem = "Atualizado com sucesso";
                setTimeout(redirecionar, 1000);
            },
            function(erro){
                console.log(erro);
            }
        )
    }

    $scope.inserirVideo = () => {
        let tags = verificaTags($scope.tags);
        
        let dados = {
            titulo: $scope.titulo,
            link: $scope.link,
            descricao: $scope.descricao,
            tags: tags,
            dataPublicacao: new Date()
        }
        $http.post(urlBase+"inserir", JSON.stringify(dados)).then(
            function(resposta){
                // console.log(resposta.data.result);
                $scope.mensagem = "Inserido com sucesso";
                setTimeout(redirecionar, 1000);
            },
            function(erro){
                $scope.erro = "Erro ao inserir o vídeo";
            }
        );
    }

    function verificaTags(tags){
        if(typeof(tags) == "string"){
            tags = tags.replace(/\s+/g, '');
            tags = tags.split(',').map( s => s.trim());
        }

        return tags;
    }

    function redirecionar(){
        window.location.assign("#!/gerenciar");
    }

    if($routeParams.id){
        let id = $routeParams.id;
        
        let funcao = window.localStorage.getItem('funcao');
        
        if (funcao == "atualizar") {
            buscarInfo(id);
        }
    }
});