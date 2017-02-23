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
make
```

## Run

To be able to run the plugin, copy the executable just compiled (**vectrabool**) to the plugin directory :
```
cp vectrabool ~/.gimp-2.8/plug-ins/
```

Now the plugin should be available in Gimp under *Image -> Transform -> Vectorize*
