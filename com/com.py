class Com1Receiver:
        def __init__(self):
                self.weightVar:str
                self.ser = None
                self.reading = False
                self.start_reading()
        def startReading(self):
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
                        threading.Thread(target=self.read_loop, daemon=True).start()
                except serial.SerialException as e:
                         print(f"Error on startReceiver -: {e}")
                         return f"Error on startReceiver -: {e}"
        def stopReading(self):
                self.reading = False
                if self.ser and self.ser.is_open:
                        self.ser.close()
        def readloop(self):
                while self.reading and self.ser.is_open:
                        try:
                                raw = self.ser.read(16)  # Read full frame
                                weight = int(self.extract_weight(raw))
                                if weight is not None:
                                        self.weightVar = str(int(weight) / 10)
                        except:
                                break
        def _extract_weight(self, frame):
                try:
			# Expect frame starting with 0x02, ASCII digits follow
                        if len(frame) >= 10 and frame[0] == 0x02:
                                ascii_part = frame[1:9].decode('ascii', errors='ignore')
                                weight_str = ascii_part.strip('+').lstrip('0')
                                return int(weight_str) if weight_str else 0
                        return None
                except:
                        return None

        def on_close(self):
                self.stopReading()
