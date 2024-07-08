import os
import webbrowser
import asyncio
import sys 

# Steps:
# 1. Reverse requirements.txt
# 2. make and build an EXE file
# 3. Create a py file that automate the running of django default server [ = This File]
# 4. Convert [ = This File] to an EXE with icon option 

# Actions:
# pip install -r requirements.txt
# pyinstaller --name=CourseManagementSystem .\CoursesManagementSystem\manage.py [PATH to manage.py] [--name=PARENT_FILE_NAME]
# example to above command (pyinstaller --name="Courses Management System - Arabic VersionFinal" .\manage.py)
# pyinstaller.exe --onefile --noconsole --icon=.\XXX.ico .\automate_runserver_command.py [PATH to file responsible to runserver]
# After all, Do not forget to move:
# 1. Rename the generated exe from the first step to "CourseManagementSystem.exe"
# 2. "middleware" folder, templates folder and static folder each to its right place
# 3. And make sure you migrate to the latest sql (restore sql).


# RUNSERVER
async def runserver():

    BASE_DIR = ''
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True 
        application_path = os.path.dirname(sys.executable)
        # pyinstaller will move EXE file to a folder named as dist  
        BASE_DIR = application_path
    elif __file__:
        application_path = os.path.dirname(__file__)
        BASE_DIR = os.path.join(application_path, 'dist')

    # path = "D:\Your\Django\Project\Full\Path\SimpleBlog"
    path = f"{BASE_DIR}\\Courses Management System - Arabic VersionFinal" # absolute_directory_path
    os.chdir(path)


    # os.system("py manage.py runserver")
    # The name of XXX.exe application to run
    os.system("CourseManagementSystem.exe runserver localhost:8000 --noreload")

# OPEN BROWSER
def openproject():
    webbrowser.open_new_tab("http://127.0.0.1:8000")

# EXECUTE PROGRAM
async def main():
    task1 = asyncio.create_task(runserver())
    openproject()
    await task1



asyncio.run(main())
