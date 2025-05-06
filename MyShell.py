import os
import time
import shutil
import re
import subprocess
from urllib.request import urlopen
print("MyShell [Version 1.3]")
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

def unset_command(args):
    if not args:
        print("Usage: unset [variable_name]")
        return
    var_name = args
    if var_name in variables:
        del variables[var_name]
        print(f"Unset variable: {var_name}")
    else:
        print(f"Variable not found: {var_name}")

def open_command(args):
    file_path = os.path.join(path, args.strip())
    try:
        os.startfile(file_path)
    except FileNotFoundError:
        print("File not found.")
    except OSError as e:
        print(f"Failed to open file: {e}")



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
    elif com.lower().startswith("unset "):
        args = com[5:].strip()
        unset_command(args)
    elif com.lower() == "env":
        print(variables)
    elif com.lower().startswith("curl "):
        url = com[4:].strip()
        response = urlopen(url)
        raw_data = response.read()
        try:
            decoded_data = raw_data.decode('utf-8')
        except UnicodeDecodeError:
            decoded_data = raw_data.decode('latin-1')
        
        print(decoded_data)
    elif com.lower().startswith("help "):
        help1 = com[4:].strip()
        if help1 == "curl":
            print("Fetch and display content from a web URL")
            print("")
            print("Usage:")
            print("     curl <URL>")
            print("Example:")
            print("      curl https://www.google.com")
            print("")
            print("Warning! If you try for example: google.com or www.google.com it will not work! You have to use https://")
            print("Usage:")
        elif help1 == "help":
            print("    help <command>")
            print("Example:")
            print("    help echo")
        elif help1 == "echo":
            print("print out stuff")
            print("")
            print("Usage:")
            print("    echo <something>")
            print("Examples:")
            print("    echo Hello World!")
            print("    echo $myvar")
            print("")
            print("To use variables you need to use the command 'set'. Do 'help set' for more info.")
        elif help1 == "set":
            print("")
            print("make variables")
            print("Usage:")
            print("     set <varname=value>")
            print("Example:")
            print("     set myvar=hey")
            print("")
    elif com.lower() == "help":
        print("Try 'help help' instead!")
    elif com.lower().startswith("./"):
        args = com[2:].strip()
        open_command(args)
        

    else:
        print(f"'{com}' is not recognized as an internal command.") # https://github.com/RealIceCone/MyShell <-- My github if you could not tell