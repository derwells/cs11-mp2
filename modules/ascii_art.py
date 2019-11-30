class Ascii():
    def __init__(self):
        self.error = """ .d88b.  888d888 888d888 .d88b.  888d888 
d8P  Y8b 888P"   888P"  d88""88b 888P"   
88888888 888     888    888  888 888     
Y8b.     888     888    Y88..88P 888     
"Y8888   888     888     "Y88P"  888"""    
        self.error = self.error.split('\n')
        self.success = """.d8888b  888  888  .d8888b .d8888b .d88b.  .d8888b  .d8888b  
88K      888  888 d88P"   d88P"   d8P  Y8b 88K      88K      
"Y8888b. 888  888 888     888     88888888 "Y8888b. "Y8888b. 
     X88 Y88b 888 Y88b.   Y88b.   Y8b.          X88      X88 
 88888P'  "Y88888  "Y8888P "Y8888P "Y8888   88888P'  88888P'"""
        self.success = self.success.split('\n')