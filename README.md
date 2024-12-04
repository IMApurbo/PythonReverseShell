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
