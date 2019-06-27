from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import os

PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
SHADOW_CLIENT = "get"
HOST_NAME = "a1nu7pzutt6elx-ats.iot.eu-west-1.amazonaws.com"
ROOT_CA = PATH + "keys/AmazonRootCA1.pem"
PRIVATE_KEY = PATH + "keys/be65ccf551-private.pem.key"
CERT_FILE = PATH + "keys/be65ccf551-certificate.pem.crt"
SHADOW_HANDLER = "amc-chilli-pi"


# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
    pass


def shadowUpdate(body):
    # Create, configure, and connect a shadow client.
    myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
    myShadowClient.configureEndpoint(HOST_NAME, 8883)
    myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
    myShadowClient.configureConnectDisconnectTimeout(10)
    myShadowClient.configureMQTTOperationTimeout(5)
    myShadowClient.connect()

    # Create a programmatic representation of the shadow.
    myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

    myDeviceShadow.shadowUpdate(body, myShadowUpdateCallback, 5)
