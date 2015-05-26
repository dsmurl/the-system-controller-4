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
                    Rpc.listSensors()
                        .success(function (r) {
                            $scope.sensors = r.result;
                        });
                }]
            })
            .when('/devices', {
                templateUrl: 'html/devices.html',   controller: ['$scope', '$routeParams', 'Rpc', '$location', function ($scope, $routeParams, Rpc, $location) {
                    Rpc.listDevices()
                        .success(function (r) {
                            $scope.devices = r.result;
                        });
                }]
            })
            .when('/rules', {
                templateUrl: 'html/rules.html',   controller: ['$scope', '$routeParams', 'Rpc', '$location', function ($scope, $routeParams, Rpc, $location) {
                    Rpc.listRules()
                        .success(function (r) {
                            $scope.rules = r.result;
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
                listSensors: function () {
                    return rpcRequest('list_sensors');
                },
                listDevices: function () {
                    return rpcRequest('list_devices');
                },
                listRules: function () {
                    return rpcRequest('list_rules');
                }
            };
        }]);