import json
import ssl
import socket
from twython import Twython, TwythonStreamer, TwythonError
from threading import Timer

from requests.exceptions import Timeout, ConnectionError, ReadTimeout
from urllib3.exceptions import ReadTimeoutError

from auth import consumer_key, consumer_secret, access_token, access_token_secret

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if "user" in data:
            # print('tweet with no data')
            if data["user"]["screen_name"] == "Babchik":
                if "retweeted_status" in data:
                    print(data["text"])
                else:
                    print("retweeted status NOT AVAILABLE")
                    print(data)
                    twitter.retweet(id=data["id"])

    def on_error(self, status_code, data):
        self.disconnect()
        print("stream class error... ")
        print(status_code, data)
        stream()

    def on_timeout(self, data):
        print("Stream timedout. Restarting stream..../n")
        stream()


def stream():
    while True:
        try:
            stream = MyStreamer(
                consumer_key, consumer_secret, access_token, access_token_secret
            )
            stream.statuses.filter(track="Babchik")
        except socket.timeout as ser:
            print("socket timeout")
            print(ser)
            pass
        except (
            TimeoutError,
            ssl.SSLError,
            ReadTimeoutError,
            TimeoutError,
            ConnectionError,
        ) as exc:
            print("error")
            print(exc)
            pass
        except KeyboardInterrupt:
            print("keyboard interrupt")
            break
        except:
            print("worst case ontario")
            pass


stream()
