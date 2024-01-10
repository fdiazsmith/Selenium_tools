# Declaree
This uses selenium to automate the process of downloading receipts from declaree and uploading them to a google drive folder.


## Installation Guide

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**

   Open your terminal and run the following command:

   ```bash
   git clone https://github.com/username/repository.git
   ```

   Replace `https://github.com/username/repository.git` with the URL of your Git repository.

2. **Navigate to the project directory**

   ```bash
   cd repository
   ```

   Replace `repository` with the name of your project directory.

3. **Create a virtual environment**

   On macOS:

   ```bash
   python3 -m venv venv
   ```

   On Windows:

   ```bash
   py -m venv venv
   ```

4. **Activate the virtual environment**

   On macOS:

   ```bash
   source venv/bin/activate
   ```

   On Windows:

   ```bash
   .\venv\Scripts\activate
   ```

5. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

Now, you should have all the dependencies installed in your virtual environment and you're ready to run the project.

Remember to replace the placeholders with your actual project details.


## creatinga binary
First, install PyInstaller. You can do this with pip:
```bash
pip install pyinstaller
```

Once PyInstaller is installed, navigate to the directory containing your Python script and run the following command:
```bash
pyinstaller --onefile your_script.py
```

Replace `your_script.py` with the name of your Python script.
This will create a standalone executable in the dist directory. You can run this executable without having Python installed.



## creatinga binary
First, install PyInstaller. You can do this with pip:
```bash
pip install pyinstaller
```

Once PyInstaller is installed, navigate to the directory containing your Python script and run the following command:
```bash
pyinstaller --onefile your_script.py
```

Replace `your_script.py` with the name of your Python script.
This will create a standalone executable in the dist directory. You can run this executable without having Python installed.