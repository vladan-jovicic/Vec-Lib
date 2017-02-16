CFLAGS += $$(pkg-config opencv --cflags)
CFLAGS += -ggdb
LDLIBS += $$(pkg-config opencv --libs)

all: contourDetection
contourDetection.o: contourDetection.cpp contourDetection.h
	g++ -c -Wall $<
contourDetection: contourDetection.o
	g++ -o $@ $^ $(CFLAGS) $(LDLIBS)

clean:
	rm -v  ./*.o
mrproper: clean
	rm -rf contourDetection

