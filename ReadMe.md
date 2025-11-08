Code Mapper 🗺️

Generate a complete text map of your codebase for AI context windows.

Perfect for feeding your entire project to ChatGPT, Claude, or any AI assistant!



🚀 Quick Start

Option 1: Just Run It (Easiest)



Place codemapper.exe in your project folder

Double-click codemapper.exe

Done! Find your map in codemapper/output/code\_map.txt



Option 2: Use Command Line

bash# Open terminal in your project folder

codemapper.exe



\# Or specify a folder

codemapper.exe --src ./myproject



📋 What It Does



Scans your project files

Includes full content of text files (.php, .js, .py, etc.)

Registers binary files (images, PDFs) by name only

Skips common folders (node\_modules, .git, vendor)

Outputs everything into ONE text file



Example Output:

MAP: Generated 2025-11-08 10:30:15

--app/controllers/UserController.php

<?php

class UserController {

&nbsp;   // your code here...

}

----

--app/models/User.php

<?php

class User {

&nbsp;   // your code here...

}

----

--public/logo.png

--SUMMARY

Text:45 Binary:12 Skipped:156



💾 Save Your Settings (Configs)

Create a Default Config

bash# Run this once with your preferences

codemapper.exe --folders app,database --except-folders tests --savetoconfig



\# Now just run with no arguments - it remembers!

codemapper.exe

Create Named Configs

bash# Save different configs for different needs

codemapper.exe --folders app,src --savetoconfig frontend

codemapper.exe --folders api,database --savetoconfig backend



\# Use them

codemapper.exe --config frontend

codemapper.exe --config backend

Configs are saved in: codemapper/config/



🎯 Common Use Cases

1\. Scan Entire Project

bashcodemapper.exe

2\. Scan Specific Folders Only

bashcodemapper.exe --folders app,database,config

3\. Include Specific Files Only

bashcodemapper.exe --files config.php,routes.php,composer.json

4\. Exclude Folders or Files

bashcodemapper.exe --except-folders tests,logs,tmp

codemapper.exe --except-files .env,package-lock.json

5\. Multiple Source Folders

bashcodemapper.exe --src ./frontend --src ./backend

6\. Custom Output Location

bashcodemapper.exe --output D:/exports/myproject.txt



🛠️ All Commands

CommandDescriptioncodemapper.exeRun with default settings or saved config--src <folder>Source folder to scan (default: current folder)--folders <list>Only scan these folders: --folders app,src--files <list>Only include these files: --files config.php--except-folders <list>Skip these folders: --except-folders tests--except-files <list>Skip these files: --except-files .env--output <path>Custom output path--config <name>Load saved config: --config myproject--savetoconfig <name>Save current settings as config



🤖 Using with AI Assistants

ChatGPT / Claude / Gemini



Generate your code map: codemapper.exe

Open codemapper/output/code\_map.txt

Copy all content (Ctrl+A, Ctrl+C)

Paste into AI chat with your question



Example prompts:



"Here's my codebase. Help me refactor the authentication system."

"Review this code for security issues."

"Add a new feature to handle file uploads."

"Explain how the database models relate to each other."





📁 File Structure

After running, you'll have:

your-project/

├── codemapper.exe          ← The tool

├── codemapper/

│   ├── config/            ← Your saved configs

│   │   ├── default.json

│   │   └── myproject.json

│   └── output/            ← Generated maps

│       └── code\_map.txt



💡 Pro Tips

Tip 1: Use Default Config

Save your most common settings as default:

bashcodemapper.exe --folders app,src --except-folders tests --savetoconfig

Now just double-click codemapper.exe anytime!

Tip 2: Timestamp Your Maps

When prompted, choose y to add timestamp to filename:



code\_map\_110825-1430.txt (Nov 8, 2025 at 2:30 PM)



Tip 3: Quick Folder Access

After generating, choose folder to open the output directory directly.

Tip 4: Multiple Projects

Create named configs for each project:

bashcd project1

codemapper.exe --folders app --savetoconfig project1



cd project2

codemapper.exe --folders src --savetoconfig project2



🔧 Advanced Usage

Scan Only PHP Files in App Folder

bashcodemapper.exe --folders app --extensions .php

Scan Everything Except Tests and Logs

bashcodemapper.exe --except-folders tests,logs,storage/logs

Large Projects (Increase File Size Limit)

Edit your config file manually:

json{

&nbsp; "max\_file\_size\_mb": 50

}



🐍 For Developers (Python)

If you have Python installed, you can use the .py version:

bashpython codemapper.py --folders app,src

Build your own executable:

bashpip install pyinstaller

pyinstaller --onefile --name codemapper codemapper.py



❓ FAQ

Q: Where is the output saved?

A: By default in codemapper/output/code\_map.txt

Q: Can I use it on multiple projects?

A: Yes! Create named configs for each project.

Q: What files are included?

A: All text files (.php, .js, .py, .html, .css, .json, etc.). Binary files are registered by name only.

Q: What's automatically skipped?

A: node\_modules, .git, vendor, dist, build, .cache, and the codemapper folder itself.

Q: How do I reset to defaults?

A: Delete codemapper/config/default.json or run with explicit flags.

Q: Can I exclude specific files?

A: Yes! Use --except-files .env,secrets.json

Q: Does it work on Mac/Linux?

A: The Python version works everywhere. The .exe is Windows-only.



📝 Config File Example

codemapper/config/default.json:

json{

&nbsp; "src": \["."],

&nbsp; "folders": \["app", "database", "config"],

&nbsp; "except\_folders": \["tests", "storage/logs"],

&nbsp; "except\_files": \[".env", "package-lock.json"],

&nbsp; "text\_extensions": \[".php", ".js", ".py", ".html"],

&nbsp; "max\_file\_size\_mb": 10

}



📄 License

Free to use for personal and commercial projects.

