                    while True:
                          print("zhgt")
                          print("hellp") 
                          response += part
                          print(response)
                          part = client.recv(1024) 
                          if part.decode("utf-8") == '':
                            break  