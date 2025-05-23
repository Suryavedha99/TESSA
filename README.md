# TESSA: Task-Optimized Engine for System Support and Automation

TESSA (Task-Optimized Engine for System Support and Automation) is a Natural Language Processing (NLP)-based command-line tool designed to automate local file management. It enables users to perform system-level operations such as move, copy, delete, rename, and create through intuitive natural language commands. This project serves as a functional prototype and foundational step toward developing a cross-platform, intelligent file management assistant capable of operating at a software/system level. 

Below, we have provided detailed setup instructions, required package installations, supported command structures, and a sample session to demonstrate TESSA’s functionality and ease of use.

---

## Installation & Setup

Ensure Python 3 is installed on your system. Then run the following commands in your terminal to install dependencies and set up the NLP model:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

---

## Running the Program

After setup, execute the script using:

```bash
python tessa.py
```

The file system agent will initialize and wait for your commands in a terminal-based interface.

---

## Supported Commands

TESSA recognizes natural language commands that involve six core file operations. It parses each command using NLP and executes the corresponding action if sufficient information is available.

| Command Type | Description | Example |
|--------------|-------------|---------|
| `move`       | Move file/folder from one location to another | move folder `X` from desktop to documents |
| `copy`       | Copy file/folder from source to destination | copy file `Y.pdf` from downloads to desktop |
| `delete`     | Delete a specified file or folder | delete file `temp.txt` from downloads |
| `rename`     | Rename a file or folder | rename file `old.txt` to `new.txt` |
| `create`     | Create a new folder or file | create folder `project` in documents |
| `list`       | List contents of a directory | list files in downloads |

---

## Sample Session

Below is an example of how a typical interaction with TESSA looks in the terminal:

<div style="background-color:#f9f9f9; border:1px solid #ccc; padding:10px; font-family:monospace; white-space:pre; font-size:14px;">

<span style="color:blue;">Loading NLP model...</span><br>
<span style="color:blue;">File System Agent initialized for Windows</span><br>
<span style="color:blue;">Home directory: C:\Users\YourName</span><br>
<span style="color:blue;">File System Agent is ready!</span><br>

<span style="color:blue;">You can now use natural language commands like:</span><br>
<span style="color:blue;"> - 'move folder projects from desktop to documents'</span><br>
<span style="color:blue;"> - 'copy file report.pdf from downloads to desktop'</span><br>
<span style="color:blue;"> - 'create folder new_project in documents'</span><br>
<span style="color:blue;"> - 'delete file temp.txt from downloads'</span><br>
<span style="color:blue;"> - 'list files in downloads'</span><br>
<span style="color:blue;">Type 'exit' to quit.</span><br><br>

What would you like me to do? <span style="color:black;">> create folder test_project in documents</span><br>
<span style="color:blue;">Successfully created folder 'test_project' in C:\Users\YourName\Documents</span><br>

What would you like me to do? <span style="color:black;">> move folder test_project from documents to desktop</span><br>
<span style="color:blue;">Successfully moved 'test_project' from C:\Users\YourName\Documents to C:\Users\YourName\Desktop</span><br>

What would you like me to do? <span style="color:black;">> exit</span><br>
<span style="color:blue;">Goodbye!</span>
</div>

---

## Future Scope

- Integration with voice-based input for hands-free interaction  
- Development of a GUI for non-terminal users  
- Cloud sync and cross-platform support for mobile environments



© 2025 Suryavedha Pradhan, Vishnu Vardhan Chundu, Shreyas Achal. This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
