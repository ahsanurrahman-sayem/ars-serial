import threading
import time
import random
import traceback
import serial

class Com1Receiver:
	def __init__(self):
		self.serial_data: str = None
		self.ser = None
		self.reading = False
		self._startReading()

	def _startReading(self):
		try:
			self.ser = serial.Serial(
				port='COM1',
				baudrate=9600,
				bytesize=serial.EIGHTBITS,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				timeout=1
			)
			self.reading = True
			threading.Thread(target=self.readloop, daemon=True).start()
		except serial.SerialException as e:
			print(f"[ERROR] _startReading() - SerialException: {e}")
			print(traceback.format_exc())
		except Exception:
			print("[ERROR] _startReading() - Unexpected exception:")
			print(traceback.format_exc())

	def stopReading(self):
		try:
			self.reading = False
			if self.ser and self.ser.is_open:
				self.ser.close()
		except Exception:
			print("[ERROR] stopReading() - Exception while closing port:")
			print(traceback.format_exc())

	def readloop(self):
		try:
			while self.reading and self.ser and self.ser.is_open:
				raw = self.ser.read(16)
				weight = self._extract_weight(raw)
				if weight is not None:
					self.serial_data = str(weight / 10)
		except Exception:
			print("[ERROR] readloop() - Exception while reading data:")
			print(traceback.format_exc())

	def _extract_weight(self, frame):
		try:
			if len(frame) >= 10 and frame[0] == 0x02:
				ascii_part = frame[1:9].decode('ascii', errors='ignore')
				weight_str = ascii_part.strip('+').lstrip('0')
				return int(weight_str) if weight_str else 0
			return None
		except Exception:
			print("[ERROR] _extract_weight() - Failed to parse frame:")
			print(traceback.format_exc())
			return None

	def on_close(self):
		self.stopReading()

	def data(self):
		return self.serial_data


# ------------- 0.0.0 ------------- #
class FakeComReceiver:
	def __init__(self):
		self.serial_data: str = None
		self.reading = False
		self._startReading()

	def _startReading(self):
		try:
			self.reading = True
			threading.Thread(target=self.readloop, daemon=True).start()
			print("[INFO] FakeComReceiver started — simulating COM1 data stream")
		except Exception:
			print("[ERROR] _startReading() - Unexpected exception:")
			print(traceback.format_exc())

	def stopReading(self):
		try:
			self.reading = False
			print("[INFO] FakeComReceiver stopped")
		except Exception:
			print("[ERROR] stopReading() - Exception while stopping:")
			print(traceback.format_exc())

	def readloop(self):
		try:
			while self.reading:
				# simulate a frame: [0x02][+00001234][\r\n]
				weight_val = random.randint(0, 9999)
				frame = b'\x02' + f"+{weight_val:08d}\r\n".encode('ascii')
				weight = self._extract_weight(frame)
				if weight is not None:
					self.serial_data = str(weight / 10)
					print(f"[FAKE DATA] Weight: {self.serial_data}")
				time.sleep(1)
		except Exception:
			print("[ERROR] readloop() - Exception while generating data:")
			print(traceback.format_exc())

	def _extract_weight(self, frame):
		try:
			if len(frame) >= 10 and frame[0] == 0x02:
				ascii_part = frame[1:9].decode('ascii', errors='ignore')
				weight_str = ascii_part.strip('+').lstrip('0')
				return int(weight_str) if weight_str else 0
			return None
		except Exception:
			print("[ERROR] _extract_weight() - Failed to parse frame:")
			print(traceback.format_exc())
			return None

	def on_close(self):
		self.stopReading()

	def data(self):
		return self.serial_data


