from debugger import Debugger

import SocketServer
from telnetsrv.threaded import TelnetHandler, command


class MyHandler(TelnetHandler):
    WELCOME = "Successfully connected. \n Welcome to the debug interface of FlowVision node."
    PROMPT = "Debugger> "

    @command('test')
    def test(self, params):
        '''
            test funcion
        '''
        msg = self.input.raw
        self.writeline("You entered: " + msg)

    @command('params')
    def command_params(self, params):
        '''[<params>]*
        Echos back the raw received parameters.
        '''
        self.writeresponse("Entered parameters == %r" % params)


class TelnetServer(SocketServer.TCPServer):
    allow_reuse_address = True





class TelnetDebugger(Debugger):
    def run(self):
        server = TelnetServer(("0.0.0.0", 7777), MyHandler)
        server.serve_forever()
        while True:
            pass