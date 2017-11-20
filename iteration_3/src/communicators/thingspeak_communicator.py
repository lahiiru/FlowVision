from communicators import Communicator
import httplib
import urllib
import time

class ThingspeakCommunicator(Communicator):
    def __init__(self):
        Communicator.__init__(self)
        self.base_url = "api.thingspeak.com"

    def prepare_message_json(self, velocity, level, debugObj):
        m = "field1={0}&field2={1}&field3={2}".format(urllib.quote(str(velocity)), urllib.quote(str(level)), "0")
        return m

    def send_message(self, message):
        query = "/{1}&{2}".format(self.base_url,"update?api_key=0XHD06IBKCQ4ANZ6",message)

        print query
        body = ("<html><body><h1>Sorry it's not Friday yet</h1> </body></html>")
        payload = {'HTML': body}
        hdr = {
                "content-type": "application/x-www-form-urlencoded"
               }

        conn = httplib.HTTPConnection(self.base_url, 80)
        conn.request('GET', query)
        response = conn.getresponse()
        data = response.read()
        time.sleep(2)
        conn.close()
        return data