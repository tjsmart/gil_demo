default:
	cmake -B build
	cmake --build build
	virtualenv venv -ppy39
	. venv/bin/activate
	cp build/*.so venv/lib/python3.9/site-packages
	python app.py
