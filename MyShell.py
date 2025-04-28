import os
import time

username = os.getlogin()
path = f"C:\\Users\\{username}"

while True:
    com = input(f"{path}>").strip()

    if com.lower() == "exit":
        print("Goodbye!")
        time.sleep(1)
        break

    elif com.lower() == "dir":
        try:
            items = os.listdir(path)
            for item in items:
                print(item)
        except Exception as e:
            print(f"Error: {e}")
    elif com.lower() == "clear" or com.lower() == "cls":
        os.system('cls' if os.name == 'nt' else 'clear')

    elif com.lower().startswith("cd "):
       
        target = com[3:].strip()  
        
        
        if target == "..":
            path = os.path.dirname(path)
        else:
            
            new_path = os.path.join(path, target)
            if os.path.isdir(new_path):
                path = new_path
            else:
                print(f"The system cannot find the path specified: {target}")

    
    else:
        print(f"'{com}' is not recognized as an internal command. You can report this on my github!")
