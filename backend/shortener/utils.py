import string
import random

def string_generator(length:int):
    all = string.ascii_lowercase+string.ascii_uppercase+string.digits
    key = "".join(random.choice(all) for i in range(length))
    print(key)

    return key

def key_generator():
    return string_generator(8)


