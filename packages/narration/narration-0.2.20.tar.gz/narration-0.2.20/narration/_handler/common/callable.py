import threading
from typing import Callable

import blinker

RecordSignal = blinker.Signal
CallableThreadCreate = Callable[[], None]
CallableThreadDestroy = Callable[[threading.Thread], None]
