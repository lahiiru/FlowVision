from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class MQTTBroker(object):

    def __init__(self):
        self.host = "a16mcf6kx3ija3.iot.us-west-2.amazonaws.com"
        self.rootCAPath = "certs/root-ca.pem"
        self.certificatePath = "certs/cert.pem"
        self.privateKeyPath = "certs/private.key"
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

