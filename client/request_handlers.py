import http.client
import os

def save_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)
    print(f"File saved as: {file_path}")

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

def handle_get(response , file_path):
    # Separate headers and body
    header_data, _, body = response.partition(b"\r\n\r\n")
    headers = header_data.decode("utf-8").split("\r\n")
    status_line = headers[0]
    status_code = int(status_line.split()[1])
    print(response)

    # Check status and handle file saving if successful
    if status_code == 200:
        # Get content type from headers if available
        content_type = None
        for header in headers:
            if header.lower().startswith("content-type:"):
                content_type = header.split(":")[1].strip()
                break

        # Set base name based on the file path or a default name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if not base_name:  # If the file path doesn't specify a file, use a default name
            base_name = "index"

        # Create a file name based on the content type
        file_name = get_filename(base_name, content_type)

        # Define directory to save the file
        save_directory = "client/get_request_files"
        os.makedirs(save_directory, exist_ok=True)  # Ensure directory exists
        complete_file_path = os.path.join(save_directory, file_name)

        # Save the file
        save_file(complete_file_path, body)
        print(complete_file_path)
        print(f"File saved as: {complete_file_path}")
    else:
        print(f"Failed to get file: Status {status_code}")


#post request
def client_post(file_path, host_name, port_number=80):
    connection = http.client.HTTPConnection(host_name, port_number)

    try:
        connection.request("POST", file_path, body="")
        response = connection.getresponse()

        print(f"Status: {response.status} {response.reason}")
        
        if response.status == 200:
            data = response.read()
            print("Received Data from post request:")
            print(data.decode("utf-8"))
        else:
            print(f"File Not Found: {response.status}")

    except Exception as e:
        print(f"Error sending post request: {e}")
    finally:
        connection.close()



