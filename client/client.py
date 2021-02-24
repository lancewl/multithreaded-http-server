import requests  
from bs4 import BeautifulSoup  

# specify the URL of the archive here  
archive_url = "http://localhost:8888/"
  
def get_file_links():  
      
    # create response object  
    r = requests.get(archive_url)
      
    # create beautiful-soup object  
    soup = BeautifulSoup(r.content,'html5lib')  
      
    # find all links on web-page  
    links = soup.findAll('a')  
  
    file_links = [archive_url + link['href'] for link in links if link['href']]  
  
    return file_links  
  
  
def download_all_files(file_links):  
  
    for link in file_links:  
        '''iterate through all links in file_links  
        and download them one by one'''
          
        # obtain filename by splitting url and getting  
        # last string  
        file_name = link.split('/')[-1]  
  
        print( "Downloading file:%s"%file_name)  
          
        # create response object  
        r = requests.get(link, stream = True)  
          
        # download started  
        with open(file_name, 'wb') as f:  
            for chunk in r.iter_content(chunk_size = 1024*1024):  
                if chunk:  
                    f.write(chunk)  
          
        print( "%s downloaded!\n"%file_name ) 
  
    print ("All files downloaded!") 
    return
  
  
if __name__ == "__main__":  
  
    # getting all video links  
    file_links = get_file_links()
    print(file_links)
  
    # download all videos  
    download_all_files(file_links)  