# Gimp Plugin

## TODO 
- Create an output of points like in the original program.
- Add dilatation
- Add a way to enlarge the preview
- Add a way to run the whole program ?
- Clean the code, it's a big mess (sorry)
- Full C++ transition ?

## Dependencies 

Obviously you'll need [gimp](https://www.gimp.org/).
Make sure you have it installed and install the following libraries :

```
sudo apt-get install libgimp2.0
sudo apt-get install libgimp2.0-dev
sudo apt-get install libglib2.0-dev
```


## Compile

To compile the plugin : 

```
./configure
make
```

## Install

```
sudo make install
```

## Run

Now the plugin should be available in Gimp under *Filter -> Vectrabool* (for now)
You can preview the output of the contour detection algorithm and tune the threshold. 
`<= threshold <= 255`

## Clean
```
make clean
```
# If you are developing the plugin

If you added files add them to
```
src/Makefile.am
```
and then
```
./autogen.sh
./configure
make
sudo make install
```

To tar the whole project :
```
make dist-gzip
```
