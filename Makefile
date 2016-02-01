all: run copy_and_compress

run:
	python src/main.py

copy_and_compress:
	cp ./out/output_test_.html ./zip_test/test/test_.html
	rm -f ./zip_test/test/test.zip 
	#zip ./zip_test/test.zip ./zip_test/test/* > /dev/null

clean:
	rm -f *~ src/*~ src/*.pyc
