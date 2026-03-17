import random
import time

def build_key():
    random.seed(int(time.time() / 60))
    key = random.randbytes(32)
    return key.hex()
