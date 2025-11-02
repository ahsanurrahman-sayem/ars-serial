[![Build & Release Python Package](https://github.com/ahsanurrahman-sayem/ars-serial/actions/workflows/build-and-release.yml/badge.svg?branch=main)](https://github.com/ahsanurrahman-sayem/ars-serial/actions/workflows/build-and-release.yml)

## ars-serial
- ars is a Python package contains various modules I made to use in future and make my works more moduler.

### Installation

- Please check - <a href="https://github.com/ahsanurrahman-sayem/ars-serial/releases">Latest Release</a>

## Usage - com Module

```python
from ars import Com1Receiver

receiver = Com1Receiver()

	try:
		while True:
			print("Latest:", receiver.data())
			time.sleep(1)
	except KeyboardInterrupt:
		receiver.on_close()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)
