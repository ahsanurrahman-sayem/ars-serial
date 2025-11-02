from com import Com1Receiver as rcvr
from com import FakeComReceiver
import time

#port = rcvr()
#print(port.data())


if __name__ == "__main__":
	receiver = FakeComReceiver()
	try:
		while True:
			print("Latest:", receiver.data())
			time.sleep(1)
	except KeyboardInterrupt:
		receiver.on_close()