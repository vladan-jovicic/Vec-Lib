CC=gcc
CFLAGS=-W -Wall
CFLAGS+=$(shell gimptool-2.0 --cflags)
LDLIBS=$(shell gimptool-2.0 --libs) -lm
EXEC=vectrabool

all: $(EXEC)

vectrabool: vectrabool.o contdet.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDLIBS)

vectrabool.o: vectrabool.c error.h
	$(CC) -c $< $(CFLAGS)

utils.o: utils.c error.h
	$(CC) -c $< $(CFLAGS)

contdet.o: contdet.c error.h
	$(CC) -c $< $(CFLAGS)

clean:
	rm -rf *.o

mrproper: clean
	rm -rf $(EXEC)
