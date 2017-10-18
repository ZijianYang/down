# -*- coding: utf-8 -*-
"""进度"""
import sys


class ProgressBar:
    """进度"""
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width
    def move(self, message):
        """移动"""
        self.count += 1
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        print(message)
        progress = int(self.width * self.count / self.total)
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress)+ '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()

"""
bar = ProgressBar(total = 10)
for i in range(10):
    bar.move('We have arrived at: ' + str(i + 1))
    time.sleep(1)
"""