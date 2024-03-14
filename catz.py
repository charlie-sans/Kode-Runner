print('hello world')
import time
code = r'''
class capture_output:

    def __init__(self, process, capture_stream: Optional[IO] = None, output_stream: Optional[IO] = None):
        self.capture_logs = []
        self.subprocess = process
        self.capture_stream = capture_stream
        self.output_stream = output_stream
        self.thread = Thread(target=self._run_capture)
        self.thread.start()

    def _run_capture(self):
        if self.capture_stream is not None:
            while True:
                line = self.capture_stream.readline().decode('utf-8')

                if line != '':
                    self.output_stream.write(line)
                    self.output_stream.flush()
                    self.capture_logs.append(line)

                if self.subprocess.poll() is not None:
                    break

    def output(self):
        self.thread.join()
        return '\n'.join(self.capture_logs)
'''

for line in code.split('\n'):
   print(line)
   time.sleep(0.1)
