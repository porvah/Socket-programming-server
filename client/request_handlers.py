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
        extension = ".jpg"  
    else:
        raise ValueError("Unsupported content type")
    
    filename = f"{base_name}{extension}"
    return filename

#get_request
def client_get(file_path, host_name, port_number=80):
    connection = http.client.HTTPConnection(host_name, port_number)

    try:
        connection.request("GET", file_path)
        response = connection.getresponse()

        print(f"Status: {response.status} {response.reason}")
        if response.status == 200:
            data = response.read()
            content_type = response.getheader("Content-Type")
            base_name = os.path.splitext(os.path.basename(file_path))[0] if file_path else "output"
            file_name = get_filename(base_name, content_type)

            save_directory = "/client/get_request_files" 
            file_path = os.path.join(save_directory, file_name)

            save_file(file_path, data)
        else:
            print(f"Failed to get File: {response.status}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

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



