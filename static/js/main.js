'use strict';


angular.module('app', ['ngRoute', 'ngWebsocket', 'appServices'])
    .run(function ($websocket) {
        var ws = $websocket.$new('ws://localhost:9000');

        ws.$on('$open', function () {
            console.log('Opened');
            ws.$emit('add', {
                    a: 5,
                    b: 4
                });
        });

        ws.$on('pong', function (data) {
            console.log('The websocket server has sent the following data:');
            console.log(data);

            ws.$close();
        });

        ws.$on('$close', function () {
            console.log('Closed');
        });
    })
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'html/home.html',   controller: function ($scope) {

                }
            })
            .when('/sensors', {
                templateUrl: 'html/sensors.html',   controller: ['$scope', '$routeParams', 'Rpc', '$location', function ($scope, $routeParams, Rpc, $location) {
                    Rpc.listSensor()
                        .success(function (r) {
                            $scope.sensors = r.result;
                        });
                }]
            })
            .otherwise({redirectTo: '/'});
    }]);


angular.module('appServices', ['angular-json-rpc'])

        .factory ('Rpc', ['$http', function ($http) {
            var rpcRequest = function (method, args) {
                return $http.jsonrpc('rpc', method, args, {});
            };

            return {
                listSensor: function () {
                    return rpcRequest('list_sensor');
                }
            };
        }]);