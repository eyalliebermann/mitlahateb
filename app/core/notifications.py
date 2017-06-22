import logging

from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage

logger = logging.getLogger(__name__)


class PushService(object):
    def push(self, tokens, body):
        for token in tokens:
            response = PushClient().publish(
                PushMessage(to=str(token), body=str(body)))

            response.validate_response()
