# MyShell
### A command line made in python
So it's easy to make commands, I guess 🤷.

# Install
Just install and open it — not that hard 😭🥀 (Only works on Windows, btw.)

# How to use
Once you open it, you can run commands 😱. I know, crazy, right?

version 1.0 is very bad and only has these commands: 
- exit
- dir
- cd

### How to make your own commands 😱
Here’s an example of a command:
   
    if com.lower().startswith("wait "):
        try: 
            seconds = float(com[5:])
            print(f"Waiting for {seconds} seconds...")
            time.sleep(seconds)
        except ValueError:
            print("Invalid time value. Usage: wait <seconds>")

That's it — I just gave you an example. I'm not here to teach you Python 😭🥀💀.

# Roadmap
- Add more commands
- Command aliases
- Better error handling

  # Requirements
- Python 3.8 or higher
- Windows
