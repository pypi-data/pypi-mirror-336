import datetime
import threading
import time
import ulid
from typing import Callable, Any


class Records:
    def __init__(self):
        self.records: list[ulid] = []  # Track completed work

    def add(self, record):
        self.records.append(record)

    def __repr__(self):
        return f"<Records count={len(self.records)}>"

    def __len__(self):
        return len(self.records)


class Worker(threading.Thread):
    """
    Managed Worker Thread.
    - Has identity (ULID/UUID)
    - Tracks its state and work metrics
    - Can switch between execution contexts (ThreadSwitch)
    """

    def __init__(self, factory: Any, work_queue: Any):
        """
        Args:
            factory (Any): Reference to the ThreadFactory managing this worker.
            work_queue (Any): Queue holding this worker's tasks.
            thread_id (str): Optional. ULID/UUID for tracking this thread.
        """
        super().__init__()
        self.factory = factory
        self.work_queue = work_queue
        self.thread_id = str(ulid.ULID())  # Replace with ULID if needed
        self.state = 'IDLE'  # Other states: ACTIVE, STEALING, TERMINATING
        self.daemon = True  # Kill thread on program exi
        self.records = Records()
        self.shutdown_flag = threading.Event()

    def run(self):
        """
        Main loop for thread execution.
        """
        while not self.shutdown_flag.is_set():
            try:
                # Try to get work from its own queue first
                task = self.work_queue.dequeue()  # Assuming your queue throws on empty
                self.state = 'ACTIVE'
                self._execute_task(task)

            except Exception as e:
                # No work found, try to steal
                self.state = 'STEALING'
                stolen_task = self.factory.steal_work(exclude_worker=self)
                if stolen_task:
                    self.state = 'ACTIVE'
                    self._execute_task(stolen_task)
                else:
                    # No work, go idle
                    self.state = 'IDLE'
                    time.sleep(0.01)  # Backoff / wait (tunable)

    def _execute_task(self, task: Callable):
        """
        Execute the given task and track completion.
        """
        try:
            task()  # Execute callable work
            self.completed_work += 1
        except Exception as e:
            print(f"Worker {self.thread_id}: Task execution failed - {e}")

    def stop(self):
        """
        Trigger graceful shutdown.
        """
        self.shutdown_flag.set()

    def thread_switch(self, new_queue: Any):
        """
        Switch this worker to a new execution context (queue).
        """
        self.work_queue = new_queue
        self.state = 'SWITCHED'

    def __repr__(self):
        return f"<Worker id={self.thread_id} state={self.state} completed={self.completed_work}>"

    def get_creation_datetime(self) -> datetime.datetime:
        """
        Return the creation time of this worker using ULID timestamp.

        Returns:
            datetime: Timestamp of worker creation.
        """
        return ulid.ULID.from_str(self.thread_id).datetime

    def get_creation_timestamp(self) -> float:
        """
        Return the creation time of this worker using ULID timestamp (epoch time in seconds).

        Returns:
            float: Timestamp in seconds since epoch.
        """
        return ulid.ULID.from_str(self.thread_id).timestamp