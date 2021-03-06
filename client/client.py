from __future__ import print_function, unicode_literals
import requests  
import hashlib
import threading
import time
from PyInquirer import prompt, print_json
  
def get_file_list(server_url):  
    # create response object  
    r = requests.get(server_url)
    data = r.json()
    return data

def download_file(file_name, file_link, file_md5):
    # print( "Downloading file:%s"%file_name)  
    start = time.time()
    
    # request file from server
    try:
        r = requests.get(file_link, stream = True)  
    except:
        print("Failed to download" + file_name)
        return

    end = time.time()

    md5 = hashlib.md5(r.content).hexdigest()

    if md5 == file_md5:
        # print("Checksum successful")
        with open(file_name, 'wb') as f:  
            for chunk in r.iter_content(chunk_size = 1024*1024):  
                if chunk:  
                    f.write(chunk)
        print(file_name + f" downloaded, time taken: {end - start} sec" ) 
    else:
        print(file_name + f" download failed, md5 not match" )
    
  
def download_files_serial(file_list, server_url):  
    for file_name, file_info in file_list.items():  
        if file_info["type"] == "file": # Only download files
            download_file(file_name, server_url + file_info["link"], file_info["md5"])
  
    return

def download_files_parallel(file_list, server_url):  
    threads = list()
    for file_name, file_info in file_list.items():  
        if file_info["type"] == "file": # Only download files
            t = threading.Thread(target=download_file, args=(file_name, server_url + file_info["link"], file_info["md5"]))
            threads.append(t)
            t.start()
    
    for thread in threads:
        thread.join()
            
    return

def run_client(selected_files, server_url, mode, repeat):
    for _ in range(repeat):
        if mode == 'serial':
            download_files_serial(selected_files, server_url)
        elif mode == 'parallel':
            download_files_parallel(selected_files, server_url)
  
  
if __name__ == "__main__":
    # Ask users for the server info
    server_questions = [
        {
            'type': 'input',
            'name': 'url',
            'message': 'Please enter the server IP and port:',
            'default': 'http://localhost:8888/'
        },
    ]

    server_config = prompt(server_questions)
    if server_config['url'][-1] != '/':
        server_config['url'] += '/'
  
    # getting the file list
    file_list = get_file_list(server_config['url'])
    # print(file_list)

    # Ask users about downloading details
    choices = [{'name': f} for f in file_list.keys()]
    download_questions = [
        {
            'type': 'checkbox',
            'name': 'selected_files',
            'message': 'Please choose the files to download:',
            'choices': choices
        },
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Please choose the mode for downloading:',
            'choices': [
                'serial',
                'parallel'
            ]
        },
        {
            'type': 'input',
            'name': 'client_num',
            'message': 'How many client would you like to spawn?',
            'default': '1'
        },
        {
            'type': 'input',
            'name': 'client_repeat',
            'message': 'How many experiments would you like to repeat for each client?',
            'default': '1'
        }
    ]
    download_config = prompt(download_questions)
    selected_files = {f : file_list[f] for f in download_config["selected_files"]}

    print("Start to download following files:")
    print(download_config["selected_files"])
    print("\n")
    
    start = time.time()

    # Spawning serveral clients in threads
    threads = list()
    for i in range(int(download_config['client_num'])):  
        t = threading.Thread(target=run_client, args=(selected_files, server_config['url'], download_config["mode"], int(download_config["client_repeat"])))
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()
    
    end = time.time()
    print("\n")
    print(f"Total Time taken: {end - start} sec")