#!/usr/bin/env python
from chaser import Chaser
import os

if __name__ == '__main__':
    chaser = Chaser(os.environ["USER_NAME"], os.environ["PASSWORD"])
    chaser.positions()