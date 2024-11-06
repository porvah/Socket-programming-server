import os


DIR = os.path.join(os.getcwd(), "files")

# function to save the passed file into storage
def save_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)
    print(f"File saved as: {file_path}")

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


"""
    This function handles GET requests
    it has a home route '/' as a welcome home page which returns a html response
    - gets the path and tries to open the required file 
    - makes appropriate response format with status code 200 OK
    - returns a 404 File not found if it could not access the file
"""
def GET_handler(request, file_path):
    # Home route
    if file_path == '/':
        return ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: keep-alive\r\n\r\n"
                "<body><h1>This is the server home page</h1><p>Try to get and post files!!</p></body>").encode('utf-8')
    file_path = os.path.join(DIR, file_path.lstrip('/'))
    # Decides the content type header of the response based on the extention of the file requested
    try:
        if file_path.endswith('.txt'):
            Ctype = "text/plain"
            rM = 'r'
            pass
        elif file_path.endswith('.html'):
            Ctype = 'text/html'
            rM = 'rb'
        else:
            Ctype = 'image/jpeg'
            rM = 'rb'
        # Opens and reads the file, adds its length and type into response headers
        file = open(file_path, rM)
        body = file.read()
        response = ("HTTP/1.1 200 OK \r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Content-Type: {Ctype}\r\n\r\n"
                    )
        # Encode it when needed
        body = body.encode('utf-8') if Ctype == 'text/plain' else body 
        return response.encode('utf-8')+body
    except Exception as e:
        # Handling file not found response
        print(e)
        return ("HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\nContent-Type: text/plain\r\n\r\n"
                "File not found.").encode('utf-8')
    
"""
    his function handles POST requests
        - it partitions the request to get the header data and the body
        - gets the content type and recombines the file with an extension based on the content type
        - saves the file  in the posted files directory
        - returns an 200 OK in case of success and 400 Bad Request in case of failure
""" 
def POST_handler(request, file_path):
    header_data, _, body = request.partition(b"\r\n\r\n")
    headers = header_data.decode("utf-8").split("\r\n")

    content_type = None
    for header in headers:
        if header.lower().startswith("content-type:"):
            content_type = header.split(":")[1].strip()
            break

    if not content_type:
        print("Failed to get file")
        response = "HTTP/1.1 400 Bad Request\r\n\r\nContent-Type header missing"
        return response.encode("utf-8")

    base_name = os.path.splitext(os.path.basename(file_path))[0] or "index"
    file_name = get_filename(base_name, content_type)

    save_directory = "posted_files"
    os.makedirs(save_directory, exist_ok=True)
    complete_file_path = os.path.join(save_directory, file_name)

    save_file(complete_file_path, body)
    print(f"File saved as: {complete_file_path}")

    response = "HTTP/1.1 200 OK\r\n\r\n"
    return response.encode("utf-8")

# Function to get the content length of a request 
# this is used to get larger requests that do not fit in 1024
def get_content_length(request):
    try:
        request_str = request.decode('utf-8' , errors='ignore')
    except Exception as e:
        print(f"Error: {e}")
        return None 

    lines = request_str.split('\r\n')
    for line in lines:
        if line.startswith('Content-Length:'):
            _, length = line.split(':', 1)
            return int(length.strip()) 
