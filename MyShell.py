import os
import time
import shutil
import re
import subprocess
print("MyShell [Version 1.2]")
print("By RealIceCone")
print("")

process = None
def stop_script():  # Used by the run command
    global process
    if process and process.poll() is None:  # Still running
        process.terminate()
        process.wait()
        print("Script terminated.")
    else:
        print("No script is currently running.")

def run_script(): # Also used by the run command!
    global process
    script_path = os.path.join(path, filename)
    try:
        process = subprocess.Popen(["python", script_path])
    except Exception as e:
        print(f"Failed to run script: {e}")

def ping(host): # This is for the command "ping"
    try:
        subprocess.run(["ping", host], check=True)
    except subprocess.CalledProcessError: # If ping failed
        print(f"Ping failed: {host} is unreachable.") # print this!
    except Exception as e: # Other error
        print(f"Error pinging host: {e}") # Print this

def ipconfig_command():
    try:
         result = subprocess.run(["ipconfig"], capture_output=True, text=True)
         print(result.stdout)
    except Exception as e:
        print(f"Error running ipconfig: {e}")




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
    
    elif com.lower().startswith("cat "):
        cat = com[3:].strip()
        try:
            with open(os.path.join(path, cat), "r") as f:
                print(f.read())
                print("")
        except FileNotFoundError:
            print(f"File not found: {cat}")
            print("")
        except Exception as e:
              print(f"Error reading file: {e}")
              print("")
    elif com.lower().startswith("run "):
        filename = com[3:].strip()
        run_script()
    elif com.lower() == "stop":
        stop_script()
    elif com.lower().startswith("touch "):
        filename = com[5:].strip()
        try:
            open(os.path.join(path, filename), "a").close()
        except Exception as e:
             print(f"Error creating file: {e}")
    elif com.lower().startswith("mkdir "):
        foldername = com[5:].strip()
        try:
            os.mkdir(os.path.join(path, foldername))
        except FileExistsError:
            print("Folder already exists.")
        except Exception as e:
            print(f"Error creating folder: {e}")
    elif com.lower().startswith("rmdir "):
        foldername = com[5:].strip()
        try:
            os.rmdir(os.path.join(path, foldername))
        except FileNotFoundError:
            print("Folder not found.")
        except OSError:
            print("Folder is not empty.")
        except Exception as e:
            print(f"Error removing folder: {e}")
    elif com.lower().startswith("del "):
        filename = com[3:].strip()
        try:
            os.remove(os.path.join(path, filename))
        except FileNotFoundError:
            print("File not found.")
        except IsADirectoryError:
            print("That is a directory, use rmdir instead.")
        except Exception as e:
            print(f"Error deleting file: {e}")
    elif com.lower().startswith("copy "):
        dest = input("Where to? ")
        src = com[4:].strip()
        try:
            shutil.copy(os.path.join(path, src), os.path.join(path, dest))
        except FileNotFoundError:
            print("Source file not found.")
        except Exception as e:
            print(f"Error copying file: {e}")
    elif com.lower().startswith("move "):
        src = com[4:].strip()
        dest = input("Where to? ")
        try:
            shutil.move(os.path.join(path, src), os.path.join(path, dest))
        except FileNotFoundError:
            print("Source file not found.")
        except Exception as e:
            print(f"Error moving file: {e}")
    elif com.lower().startswith("ping "):
        host = com[4:].strip()
        ping(host)
    elif com.lower() == "ipconfig":
        ipconfig_command() # Call the ipconfig function
    else:
        print(f"'{com}' is not recognized as an internal command.") # https://github.com/RealIceCone/MyShell <-- My github if you could not tell
