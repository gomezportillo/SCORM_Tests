all: run

run:
	python src/main.py

clean:
	rm -f *~ src/*~ src/*.pyc
