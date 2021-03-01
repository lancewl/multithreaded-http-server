# Design Doc

## Server Side

Since we are required to build a client-server mode file downloading system, I think a HTTP server would be enough for the requirement. We don't actually need a bidirectional protocol such as web socket.

I chose to use `Python3` which support multithreaded HTTP server in the built-in module `http.server`. I use `SimpleHTTPServer` to quickly setup an HTTP Server that serve files in the working directory which allows useres to browse and download the files. By default, `SimpleHTTPServer` will respond an HTML includes the file list for the request to the root path of the server. The HTML is not very ideal in our case, since it takes more effort to deal with HTML format and we also plan to add md5 information to do the checksum. Therefore, I override the `list_directory()` method in `SimpleHTTPRequestHandler` to custimize the respond format in json and also add md5 of each files to the response.

To make the server script more easily to use, I use [click](https://github.com/pallets/click) to create a user friendly command line interface. Users can simply run `python server.py --help` to see every options that can be passed into the server script and the default values.

### Possible Improvements

According to the evaluation results, the multithreaded HTTP server seems not working effectively when the number of clients increase. I think it might be limited by the maximum number of threads that `Python` or `SimpleHTTPServer` can create. Therefore, it required more research in the built-in module to see if we can improve the efficiency.

## Client Side

The main task of the client is to make a request to the HTTP server to get either the file list or the files. I use [requests](https://github.com/psf/requests) package for easily making HTTP requests and built-in `threading` module to create threads. I breakdown the logic of client script into serverl functions so that users can run customized experiments by passing arrguments. For example, the users can choose which file to download and how many clients need to be spawn in the runtime.

The parallell mode of client script will create multiple threads for each file to be download. Therefore, for the evaluations that require to create 10 threads in each client, I create 10 files on the server side so that the client will also create 10 threads in the runtime. The reason why I design the client script in this way instead of downloading the same files with multiple threads is because downloading a file parallelly will highly increase the compliexity of the program. We need to reassemble the chunks of file in the right order wchich required some pre-processing to the file before we download it.

When the users sending read file list request to the server, the server will respond the file link and md5 to the users. Therefore, the users can calculate the md5 value after downloading the file then compare to the one sent by server to see if the file is correct.

To let the users customize the experiments with client script, I use [PyInquirer](https://github.com/CITGuru/PyInquirer) to create a interactive command line interface. The client script will ask users serveral questions such as the server IP, the port, files to downloand etc. Although this highly imporove the user experience, the command line interface is built on pseudo terminal which cannot easily work with bash scripts, since we cannot simply pipe arguments to the client script. Therefore, I end up with spawning clients within the client script by threads to imitate creating serveral client process.

### Possible Improvements

Due to the constraint of pseudo terminal, I use threads to create client instance instead of running the script parallelly by bash scripts. This raise an issue which is pretty similar to the server side. The maximum number of threads might limit the efficiency of the client which is not very ideal. Therefore, I'm thinking about either do more research in the `Threading` module to see if I can fix this issue or write a bash script that can pass arguments to the pseudo terminal so that I can create many clients in process.
