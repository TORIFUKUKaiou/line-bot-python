import linebot.v3.messaging
from linebot.v3.messaging.models.push_message_request import PushMessageRequest
from linebot.v3.messaging.models.text_message import TextMessage

configuration = linebot.v3.messaging.Configuration(
    access_token = "<channel access token>"
)

# Enter a context with an instance of the API client
with linebot.v3.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linebot.v3.messaging.MessagingApi(api_client)
    push_message_request = PushMessageRequest(to="<あなたのユーザーID>",
        messages = [TextMessage(text="Hello, world!"), TextMessage(text="Hello, world 2!")])

    try:
        api_instance.push_message(push_message_request)
    except Exception as e:
        print("Exception when calling MessagingApi->push_message: %s\n" % e)


