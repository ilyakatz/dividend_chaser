#!/usr/bin/env python
from chaser import Chaser
import os

if __name__ == '__main__':
    print("i'm running")
    chaser = Chaser(os.environ["USER_NAME"], os.environ["PASSWORD"])
    chaser.positions()
    chaser.positions()