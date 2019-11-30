class Ascii():
    def __init__(self):
        self.error = """  ___ _ __ _ __ ___  _ __ 
 / _ \ '__| '__/ _ \| '__|
|  __/ |  | | | (_) | |   
 \___|_|  |_|  \___/|_|   """    
        self.error = self.error.split('\n')
        self.success = """ ___ _   _  ___ ___ ___  ___ ___ 
/ __| | | |/ __/ __/ _ \/ __/ __|
\__ \ |_| | (_| (_|  __/\__ \__ \\
|___/\__,_|\___\___\___||___/___/"""
        self.success = self.success.split('\n')