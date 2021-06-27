angular.module('site').controller('userCtrl', function($scope, $http, $localStorage){

    let urlBase = "http://localhost:5000/";

    $scope.cadastraUser = () => {

        if($scope.pwd == $scope.pwd_confirme){

            let dados = {
                'user': $scope.user,
                'password': $scope.pwd
            };
            
            $http.post(urlBase+"cadastrar", JSON.stringify(dados)).then(
                function(resposta){
                    $scope.mensagem = "Cadastrado com sucesso!";
                    setTimeout(redireciona, 1000);
                },
                function(erro){
                    $scope.erro = "Erro ao cadastrar usuário!";
                }
            );
        }else{
            alert("As senhas devem ser iguais");
        }
    }

    function redireciona(){
        window.location.assign("#!/gerenciar");
    }

    $scope.login = () => {

        let dados = {
            'user': $scope.user,
            'password': $scope.pwd
        };
        
        $http.post(urlBase+"login", JSON.stringify(dados)).then(
            function(resposta){
                $localStorage.token = resposta.data.token;
                $scope.mensagem = "Logado com sucesso";
                setTimeout(redireciona, 1000);
            },
            function(erro){
                $scope.erro = "Erro ao logar, verifique as informações!";
            }
        );
    }
});