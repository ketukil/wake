"""
This very nice piece of code keeps your machine wide awake while you are doing important work
"""

import sys
import ctypes
from dataclasses import dataclass
from PIL import Image
from pystray import Menu, MenuItem, Icon
from win10toast import ToastNotifier


@dataclass
class ExecutionState:
    """
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx
    """
    # Clear states
    RESET = 0x00000000

    # Informs the system that the state being set should remain in effect until
    # the next call that uses ES_CONTINUOUS and one of the other state flags is
    # cleared.
    CONTINUOUS = 0x80000000

    # Forces the system to be in the working state by resetting the system
    # idle timer.
    SYSTEM_REQUIRED = 0x00000001

    # Forces the display to be on by resetting the display idle timer.
    DISPLAY_REQUIRED = 0x00000002

    # This value is not supported. If ES_USER_PRESENT is combined with other
    # esFlags values, the call will fail and none of the specified states will
    # be set.
    USER_PRESENT = 0x00000004

    # Enables away mode. This value must be specified with ES_CONTINUOUS.
    # Away mode should be used only by media-recording and media-distribution
    # applications that must perform critical background processing on desktop
    # computers while the computer appears to be sleeping.
    AWAY_MODE_REQUIRED = 0x00000040


class SleeplessWindows:
    """_summary_
    """

    def __init__(self):
        pass

    def wake(self):
        """_summary_
        Set SetThreadExecutionState CONTINUOUS, SYSTEM_REQUIRED, DISPLAY_REQUIRED
        """
        print("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            ExecutionState.CONTINUOUS |
            ExecutionState.SYSTEM_REQUIRED |
            ExecutionState.DISPLAY_REQUIRED)

    def sleep(self):
        """_summary_
        Set SetThreadExecutionState to CONTINUOUS
        """
        print("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            ExecutionState.CONTINUOUS)

    def reset(self):
        """_summary_
        Reset SetThreadExecutionState
        """
        print("Reset Windows Thread Execution State")
        ctypes.windll.kernel32.SetThreadExecutionState(
            ExecutionState.RESET)


# -----------------------------------------------------------------------------
# ----------------------------- Button callbacks ------------------------------
# -----------------------------------------------------------------------------


def btn_wake_handler():
    """Stay awake
    """
    sleeplessWindow.wake()
    toast("System will stay awake",  time=3)


def btn_sleep_handler():
    """Go to sleep
    """
    sleeplessWindow.sleep()
    toast("System can go to sleep", time=3)


def btn_exit_handler():
    """Reset states and exit
    """
    sleeplessWindow.reset()
    trey.stop()


def toast(msg: str, time: int):
    """Toast notification wrapper that ignores TypeError until library gets fixed

    Args:
        msg (str): What every you want to throw as a message
    """
    try:
        toaster.show_toast(APP_NAME, msg, icon_path=None, duration=time, threaded=True)
    except TypeError:
        pass


if __name__ == "__main__":
    APP_NAME: str = 'Snorwinx'
    ICON_PATH: str = 'snrlx.png'
    try:
        APP_ICON = Image.open(ICON_PATH)
    except FileNotFoundError:
        APP_ICON = None

    toaster = ToastNotifier()
    sleeplessWindow = SleeplessWindows()

    tray_menu = Menu(
        MenuItem("Stay Awake", btn_wake_handler),
        MenuItem("Go to Sleep", btn_sleep_handler, default=True),
        MenuItem(Menu.SEPARATOR, None),
        MenuItem("Exit", btn_exit_handler)
    )

    trey = Icon('name', APP_ICON, APP_NAME, menu=tray_menu)

    print("Running trey icon...")
    trey.run()

    print("Trey icon stopped. Exiting ...")
    sys.exit()
