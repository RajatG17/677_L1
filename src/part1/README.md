#INSTRUCTIONS For Running Part 1


Copy “lab-1-asterix-and-the-stock-bazaar-677-lab1” to the destination machine : 

```sh
scp -r source_dir/lab-1-asterix-and-the-stock-bazaar-677-lab1 username@elnux1.cs.umass.edu:dest_dir
```
## Run Server

ssh into the server :

```sh
ssh username@elnux1.cs.umass.edu
```

In the directory which contains the folder “lab-1-asterix-and-the-stock-bazaar-677-lab1”, run:

```sh
./lab-1-asterix-and-the-stock-bazaar-677-lab1/src/part1/run_remote_script_server.sh
```

Note: In “run_remote_script_server.sh”, the hostname/IP and port of the server are set to a fixed number used for running the experiment, for running a server with a different configuration change the IP and the port as required.

The ThreadPool size is passed as an argument to the constructor of the server. Currently, it is hard-coded in the code and set to 2. In order to change it, change the value of the server constructor argument in "server.py".

## Run Client

ssh into the client :

```sh
ssh username@elnux2.cs.umass.edu
```

In the directory which contains the folder “lab-1-asterix-and-the-stock-bazaar-677-lab1”, run:

```sh
./lab-1-asterix-and-the-stock-bazaar-677-lab1/src/part1/run_remote_script_client.sh
```

Note:  In “run_remote_script_client.sh”, the hostname/IP and port of the server are set to a fixed number used for running the experiment, for running a server with a different configuration change the IP and the port as required. 
Also, the number of client processes is set to 5, in order to add a client process add the following line:

```sh
python3 -u $PWD/lab-1-asterix-and-the-stock-bazaar-677-lab1/src/part1/client/client.py 128.119.243.147 8976 &
```

To reduce the number of client processes, remove the above line.

The number of requests sent sequentially by each client is a fixed number, currently set to 3000. In order to change the number of requests, change the value of the variable “max_client_requests” in the file “client.py”



