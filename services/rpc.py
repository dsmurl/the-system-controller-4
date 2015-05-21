import logging
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException


class ApiHandler(RpcHandler):

    def list_sensor(self):

        return [
            {
                'id': 1,
                'label': 'Test 234',
            },
            {
                'id': 2,
                'label': 'ABCTest 234',
            }
        ]