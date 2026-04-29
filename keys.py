from config import config, load_key

class Keys:
    def __init__(self):
        self.master     = load_key(config, "master")
        self.killswitch = load_key(config, "killswitch")

keys = Keys()