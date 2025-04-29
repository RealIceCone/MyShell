import os
import time
import re
print("MyShell [Version 1.1]")
print("By RealIceCone")
print("")

username = os.getlogin()
path = f"C:\\Users\\{username}"

# Dictionary to store variables
variables = {}

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
    
    elif com.lower() == "clear" or com.lower() == "cls": # I do not need to explain what this does
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
    
    elif com.lower().startswith("set "):
        # Set a variable (e.g., set myvar=value)
        parts = com[4:].split("=", 1)  # Split the input into variable name and value (Can't do a split tho)
        if len(parts) == 2:
            variables[parts[0].strip()] = parts[1].strip()
            print(f"Variable {parts[0].strip()} set to {parts[1].strip()}")
        else:
            print("Invalid format. Use: set myvar=value")
    
    elif com.lower().startswith("echo "):
        echo_str = com[5:].strip()
        # Replace any variables in the echo string (Can't replace an variable life with an echo don't worry!)
        for var in variables:
            echo_str = re.sub(r'\$' + re.escape(var), variables[var], echo_str)
        print(echo_str)

    else:
        print(f"'{com}' is not recognized as an internal command. You can report this on my github!") # https://github.com/RealIceCone/MyShell/tree/Python <-- My github if you could not tell