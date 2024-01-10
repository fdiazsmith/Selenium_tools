import cmd
import threading
import importlib
import traceback
from open import start_session
from Capture import Exporter
import Capture
import sys
from google_uploader import Driveuploader

CLIENT_SECRET = 'client_secret_972796584910-lq1gu7ieunjqae1scop0emp1k7l608cq.apps.googleusercontent.com.json'
DEFAULT_FOLDER_ID = '16tkrLp8clxL1HP3J9XYG_KN9JwuN6CYw'


class CommandInterface(cmd.Cmd):
    """ Command line interface for interacting with the Exporter. """

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.intro = (
            "Declaree extraction started\n"
            f"Executor URL: {self.driver.command_executor._url}\n"
            f"Session ID: {self.driver.session_id}\n"
            "Type help or ? to list commands.\n"
        )
        self.prompt = '> '
        self.exporter = Exporter(self.driver)
        self.drive = None
        self.folder_id = None

    def do_login(self, line):
        """ Log in to the application. """
        username = input("Username: ")
        password = input("Password: ")
        self.exporter.log_in(username, password)
    
    def do_export(self, line):
        """ Export data to a specified Google Drive folder. """
        folder_id = input("Google Folder ID: ")
        if not folder_id:
            print("No folder ID specified. using default folder.")
            folder_id = DEFAULT_FOLDER_ID
        self.folder_id = folder_id
        self.setup_drive()
        try:
            self.exporter.get_data()
        except Exception as e:
            self.print_exception(e)
    
    def print_exception(self, e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = traceback.extract_tb(exc_traceback)
        filename, line, func, text = traceback_details[-1]

        print(f"An exception occurred at file {filename}, line {line}, funtion {func},   text {text}, Reason: {e}")
    
    def do_continue(self, line):
        """ Export data to a specified Google Drive folder. """
        line_number = int(input("what was the last line number: "))
        if not line_number:
            print("No folder ID specified. using default folder.")
            line_number = -1
        
        if self.folder_id is None:
            folder_id = input("Google Folder ID: ")
            if not folder_id:
                print("No folder ID specified. using default folder.")
                folder_id = DEFAULT_FOLDER_ID
            self.folder_id = folder_id
            self.setup_drive()
        
        try:
            self.exporter.get_data(line_number)
        except Exception as e:
            self.print_exception(e)

    def setup_drive(self):
        """ Setup Google Drive uploader with given folder ID. """
       
        self.drive = Driveuploader(CLIENT_SECRET)
        
        self.drive.set_folder_id(self.folder_id)
        self.exporter.drive = self.drive

    def do_reload(self, line):
        """ Reload the Exporter module. """
        importlib.reload(Capture)
        self.exporter = getattr(Capture, 'Exporter')(self.driver)
        self.exporter.drive = self.drive

    def do_ask(self, line):
        """ Ask for the user's name and greet them. """
        name = input("What's your name? ")
        print(f"Nice to meet you, {name}!")

    def do_exit(self, line):
        """ Exit the application, uploading the expenses file before quitting. """
        print("Exiting...")
        self.exporter.drive.upload_file("expenses.csv", "export/expenses.csv", "text/csv")
        self.driver.quit()
        return True

def start_cli():
    """ Start the command line interface. """
    driver = start_session()
    CommandInterface(driver).cmdloop()

def main():
    """ Main function to handle threading and CLI execution. """
    try:
        cli_thread = threading.Thread(target=start_cli, daemon=True)
        cli_thread.start()

        while cli_thread.is_alive():
            cli_thread.join(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user...")
    finally:
        print("Exiting...")

if __name__ == '__main__':
    main()
