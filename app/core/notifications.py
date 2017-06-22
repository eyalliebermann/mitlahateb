from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from app.errors import AppError

class MitlahatebPushMessageSet:
    """
        Send push messages to a set of tokens.  This class inputs a list of ExponentPushTokens and a message.
        It then sends the message to all the push tokens in the list.
    """
    def __init__(self, token_list, message):
        self.token_list = token_list
        self.message = message
        self.extra = None

    def send_push_messages(self):
        for current_token in self.token_list:
            try:
                MPB = MitlahatebPushMessage(current_token, self.message)
                MPB.send_push_message()
            except:
                raise AppError("send push messages failed.  Token:" + current_token + "  Message: " + self.message)

class MitlahatebPushMessage:
    """
        Send a push message.  This is the most basic implementation available.
        >>> MPB = MitlahatebPushMessage('ExponentPushToken[MS85tsPivE9r94XIbS2ODD]', 'This is a test.')
        >>> MPB.send_push_message()

    """

    def __init__(self, token, message):
        # Init the push
        # Send in a token and a message.  Both should be strings.  The token is the
        # identifier of the device in question; the message is the message to be sent.
        self.token = token
        self.message = message
        self.extra = None

    def __repr__(self):
        return()

    def send_push_message(self):

        try:
            response = PushClient().publish(
                PushMessage(to=self.token,
                            body=self.message,
                            data=self.extra))
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            # rollbar.report_exc_info(
            #     extra_data={
            #         'token': token,
            #         'message': message,
            #         'extra': extra,
            #         'errors': exc.errors,
            #         'response_data': exc.response_data,
            #     })
            raise AppError("Failed to contact push server")

        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            from notifications.models import PushToken
            PushToken.objects.filter(token=self.token).update(active=False)
            raise AppError("Device not registered error")