import requests  
import hashlib
  
def get_file_list(server_url):  
    # create response object  
    r = requests.get(server_url)
    data = r.json()
    return data

def download_file(file_name, file_link, file_md5):
    print( "Downloading file:%s"%file_name)  
    
    # create response object  
    r = requests.get(server_url + file_link, stream = True)  

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
            download_file(file_name, file_info["link"], file_info["md5"])
  
    print ("All files downloaded!") 
    return
  
  
if __name__ == "__main__":  
    server_url = "http://localhost:8888/"
  
    # getting all video links  
    file_list = get_file_list(server_url)
    print(file_list)
  
    # download all videos  
    download_all_files(file_list, server_url)