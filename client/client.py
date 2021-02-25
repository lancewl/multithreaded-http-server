from __future__ import print_function, unicode_literals
import requests  
import hashlib
from PyInquirer import prompt, print_json
  
def get_file_list(server_url):  
    # create response object  
    r = requests.get(server_url)
    data = r.json()
    return data

def download_file(file_name, file_link, file_md5):
    print( "Downloading file:%s"%file_name)  
    
    # create response object  
    r = requests.get(file_link, stream = True)  

    md5 = hashlib.md5(r.content).hexdigest()

    if md5 == file_md5:
        print("Checksum successful")
        with open(file_name, 'wb') as f:  
            for chunk in r.iter_content(chunk_size = 1024*1024):  
                if chunk:  
                    f.write(chunk)
    else:
        print("Checksum failed")
        
    print( "%s downloaded!\n"%file_name ) 
  
def download_all_files(file_list, server_url):  
  
    for file_name, file_info in file_list.items():  
        if file_info["type"] == "file": # Only download files
            download_file(file_name, server_url + file_info["link"], file_info["md5"])
  
    print ("All files downloaded!") 
    return
  
  
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
        }
    ]
    download_config = prompt(download_questions)
    selected_files = {f : file_list[f] for f in download_config["selected_files"]}
    # download all videos  
    download_all_files(selected_files, server_config['url'])