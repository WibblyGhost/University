## COSC364 Assignment 01 19S1

### Authors:  
Isaac Foster 64555890  
Zachary Sanson 58520526 
          
          
### Dependencies

**Pretty Table**  
To install:

```pip3 install prettytable```

If you would like to use the bash script to automatically start the routers then you need to have xterm installed. 
You can do this on debian linux by running ```sudo apt-get install xterm```

### Instructions

To start a router, enter the following in your linux terminal from the router base directory.

```
sudo chmod + x controller.py  
./controller.py <config-file>
```  

Alternatively  

```python3 controller.py <config-file>```

or to run the automatic bash script which loads all router configurations in the /conf
directory, in a terminal type  
 ```bash start.sh```
