"""
Handles the management of the terminal functionality
"""

from subprocess import Popen
from subprocess import CalledProcessError
from subprocess import PIPE
from contextlib import contextmanager


class TermManager:
    """
    Interfaces with terminal process
    """

    process: Popen = None
    command: str
    is_term_active: bool

    def __init__(self, command: str = None):
        if command is not None:
            self.start_process(command)
            self.is_term_active = True
        else:
            self.is_term_active = False

    def stop_process(self):
        try:
            self.process.stdin.close()
            self.process.stdout.close()
            self.process.wait()
            self.is_term_active = False

            return 0
        except:
            return 1

    def start_process(self, command: str):
        """
        starts the process and raises exception in case of failure
        """
        try:
            self.process = Popen(
                command,
                stdin=PIPE,
                stdout=PIPE,
                shell=True,
                text=True,
            )
            self.is_term_active = True

        except CalledProcessError as called_process_error:
            raise called_process_error

    def send(self, command: str):
        """
        Send input to the process
        """
        try:
            self.process.stdin.write(f"{command}\n")
            self.process.stdin.flush()

            return 0
        except:
            return 1

    @property
    def current_line(self):
        if self.process is not None:
            try:
                return self.process.stdout.readline()
            except Exception as e:
                return ""
