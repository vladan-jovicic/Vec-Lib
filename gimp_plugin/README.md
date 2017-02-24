# Gimp Plugin

## Dependencies 

Make sure you have Gimp installed and install the following libraries :

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

Now the plugin should be available in Gimp under *Filter -> Misc -> plugin-template* (for now)

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
