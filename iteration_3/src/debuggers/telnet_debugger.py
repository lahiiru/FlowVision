from debugger import Debugger

import SocketServer
from telnetsrv.threaded import TelnetHandler, command


class TelnetDebugger(Debugger, TelnetHandler):

    def __init__(self, device):
        Debugger.__init__(self, device, "Telnet")
        self.port = 7777
        self.device = device

    def routine(self):
        server = TelnetServer(("0.0.0.0", self.port), RequestHandler)
        server.debugger = self
        server.serve_forever()
        while True:
            pass


class RequestHandler(TelnetHandler):

    WELCOME = "Successfully connected. \n Welcome to the debug interface of FlowVision node."
    PROMPT = "Debugger> "

    def set_debugger(self, debugger):
        self.debugger = debugger

    @command('test')
    def test(self, params):
        '''
            test funcion
        '''
        msg = self.input.raw
        self.writeline("You entered: " + msg)
        self.writeline("Reply from device with id, {0}".format(self.server.debugger.device.id))

    @command('params')
    def command_params(self, params):
        '''[<params>]*
        Echos back the raw received parameters.
        '''

        self.writeresponse("Entered parameters == %r" % params)


class TelnetServer(SocketServer.TCPServer):
    allow_reuse_address = True