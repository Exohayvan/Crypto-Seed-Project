import time, math
from collections import deque

class AverageCounter:
    def __init__(self, intervals):
        self.intervals = intervals
        self.cycle_timestamps = deque()

    def add_cycle(self):
        current_time = time.time()
        self.cycle_timestamps.append(current_time)
        self._remove_old_cycles()

    def _remove_old_cycles(self):
        current_time = time.time()
        while self.cycle_timestamps and (current_time - self.cycle_timestamps[0] > max(self.intervals)):
            self.cycle_timestamps.popleft()

    def get_averages(self):
        current_time = time.time()
        averages = {}
        for interval in self.intervals:
            count = sum(1 for ts in self.cycle_timestamps if current_time - ts <= interval)
            average = count / (interval / 60)
            averages[interval] = math.floor(average)
        return averages
    

def main():
    counter = AverageCounter([1 * 60, 15 * 60, 30 * 60, 60 * 60])

    # Run the script in a loop
    while True:
        # ... your script logic here ...
        time.sleep(1)  # Simulate some work

        counter.add_cycle()
        averages = counter.get_averages()
        print(f"1-min average: {averages[1 * 60]}, 15-min average: {averages[15 * 60]}, 30-min average: {averages[30 * 60]}, 60-min average: {averages[60 * 60]}")

if __name__ == "__main__":
    main()
