CFLAGS += $$(pkg-config opencv --cflags)
CFLAGS += -ggdb
LDLIBS += $$(pkg-config opencv --libs)

all: threshold_heuristics
threshold_heuristics.o: threshold_heuristics.cpp
	g++ -std=c++11 -c $<
threshold_heuristics: threshold_heuristics.o
	g++ -std=c++11 -o $@ $^ $(CFLAGS) $(LDLIBS)

clean:
	rm -v  ./*.o
mrproper: clean
	rm -rf threshold_heuristics

