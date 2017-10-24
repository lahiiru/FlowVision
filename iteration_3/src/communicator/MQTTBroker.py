from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os


class MQTTBroker(object):

    def __init__(self):
        self.host = "a16mcf6kx3ija3.iot.us-west-2.amazonaws.com"
        self.rootCAPath = "certs/root-ca.pem"
        self.certificatePath = "certs/cert.pem"
        self.privateKeyPath = "certs/private.key"

        package_dir = os.path.dirname(os.path.abspath(__file__))
        self.rootCAPath = os.path.join(package_dir, self.rootCAPath)
        self.certificatePath = os.path.join(package_dir, self.certificatePath)
        self.privateKeyPath = os.path.join(package_dir, self.privateKeyPath)

        self.myAWSIoTMQTTClient = None
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
        self.myAWSIoTMQTTClient.configureEndpoint(self.host, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec



    def getClient(self):
        self.myAWSIoTMQTTClient.connect()
        return self.myAWSIoTMQTTClient

