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
                templateUrl: 'html/sensors.html',   controller: ['$scope', 'Rpc', function ($scope, Rpc) {
                    Rpc.listSensor()
                        .success(function (r) {
                            $scope.sensors = r.result;
                        });

                    $scope.deleteSensor = function (index) {
                        var sensorId = $scope.sensors[index].id;
                        Rpc.deleteSensor(sensorId)
                            .success(function (r) {
                                if (r.result) {
                                    $scope.sensors.splice(index, 1);
                                }
                            });
                    }
                }]
            })
            .when('/sensor/:id', {
                templateUrl: 'html/sensor-edit.html',   controller: ['$scope', '$routeParams', 'Rpc', '$location', function ($scope, $routeParams, Rpc, $location) {
                    var sensorId = parseInt($routeParams.id);

                    Rpc.getSensor(sensorId)
                        .success(function (r) {
                            $scope.sensor = r.result;
                        });

                    $scope.save = function () {
                        Rpc.saveSensor($scope.sensor)
                            .success(function (r) {
                                $location.path('/sensors');
                                // or $scope.sensor = r.result to update current scope
                            });
                    };
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
                },
                getSensor: function (id) {
                    return rpcRequest('get_sensor', {sensor_id: id});
                },
                deleteSensor: function (id) {
                    return rpcRequest('delete_sensor', {sensor_id: id});
                },
                saveSensor: function (sensor) {
                    return rpcRequest('save_sensor', {data: sensor});
                }
            };
        }]);