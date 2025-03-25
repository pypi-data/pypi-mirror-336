import cv2

from kevinbotlib.comm import CommunicationClient
from kevinbotlib.logger import Logger, LoggerConfiguration
from kevinbotlib.vision import FrameDecoders, MjpegStreamSendable, VisionCommUtils

logger = Logger()
logger.configure(LoggerConfiguration())
client = CommunicationClient()
VisionCommUtils.init_comms_types(client)

client.connect()
client.wait_until_connected()

try:
    while True:
        sendable = client.get("streams/camera0", MjpegStreamSendable)
        if sendable:
            cv2.imshow("image", FrameDecoders.decode_sendable(sendable))
        cv2.waitKey(1)
except KeyboardInterrupt:
    client.disconnect()
