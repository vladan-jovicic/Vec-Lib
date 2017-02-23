# Gimp Plugin

## Dependencies 

Make sure you have Gimp installed and install the following libraries :

```
sudo apt-get install libgimp2.0
sudo apt-get install libgimp2.0-dev
```


## Compile

To compile the plugin : 

```
./configure
make
```

## Install

```
make install
```

## Run

Now the plugin should be available in Gimp under *Filter -> Misc -> plugin-template* (for now)
