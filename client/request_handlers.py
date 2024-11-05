import http.client
import os
DIR = os.path.join(os.getcwd(), "post_request_files")

def save_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)

#function to get the name based on the type
def get_filename(base_name, content_type):
    if 'text/html' in content_type:
        extension = ".html"
    elif 'text/plain' in content_type:
        extension = ".txt"
    elif 'image/' in content_type:
        extension = ".jpeg"  
    else:
        raise ValueError("Unsupported content type")
    
    filename = f"{base_name}{extension}"
    return filename

#get_request
def client_get(file_path, host_name, port_number=8000):
        msg = f"GET {file_path} HTTP/1.1\r\nHost: {host_name}:{port_number}\r\nConnection: keep-alive\r\n\r\n"
        return msg

def get_content_length(response):
    try:
        response_str = response.decode('utf-8' , errors='ignore')
    except Exception as e:
        print(f"Error: {e}")
        return None 

    lines = response_str.split('\r\n')
    for line in lines:
        if line.startswith('Content-Length:'):
            _, length = line.split(':', 1)
            return int(length.strip()) 

    return None

def handle_get(response , file_path):
    header_data, _, body = response.partition(b"\r\n\r\n")
    headers = header_data.decode("utf-8").split("\r\n")
    status_line = headers[0]
    status_code = int(status_line.split()[1])
    if status_code == 200:
        content_type = None
        for header in headers:
            if header.lower().startswith("content-type:"):
                content_type = header.split(":")[1].strip()
                break

        #get the ile path
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if not base_name:
            base_name = "index"

        file_name = get_filename(base_name, content_type)
         
        #save to the default directory
        save_directory = "get_request_files"
        os.makedirs(save_directory, exist_ok=True)  # Ensure directory exists
        complete_file_path = os.path.join(save_directory, file_name)

        save_file(complete_file_path, body)
        print(f"File saved as: {complete_file_path}")
    else:
        print(f"Failed to get file: Status {status_code}")

#post request
def handle_post(file_path, host_name, port_number=8000):
    #get the file path
    file_path = os.path.join(DIR, file_path.lstrip('/'))
    print(f"Full file path: {file_path}")
    try:
        if file_path.endswith('.txt'):
            Ctype = "text/plain"
            rM = 'r' 
        elif file_path.endswith('.html'):
            Ctype = 'text/html'
            rM = 'r' 
        else:
            Ctype = 'image/jpeg'
            rM = 'rb'  

        with open(file_path, rM) as file:
            body = file.read()

        # Encode body 
        if Ctype in ['text/plain', 'text/html']:
            body = body.encode('utf-8') 
        
        # Create the POST request
        msg = (f"POST {file_path} HTTP/1.1\r\n"
               f"Host: {host_name}:{port_number}\r\n"
               f"Connection: keep-alive\r\n"
               f"Content-Length: {len(body)}\r\n"
               f"Content-Type: {Ctype}\r\n\r\n")
        # Return the full message 
        return msg.encode('utf-8') + body

    except Exception as e:
        print(f"Error: {e}")
        return ("HTTP/1.1 404 Not Found\r\n"
                "Content-Length: 15\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "File not found.").encode('utf-8')
    

