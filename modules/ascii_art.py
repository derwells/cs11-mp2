class Ascii():
    """
    Contains ASCII art to be used in Interface. :attr:`title`,
    :attr:`success`, and :attr:`error` sourced from:
    http://patorjk.com/software/taag/.

    Attribues:
        title (list): Title shown in start and difficulty menu.
        success (list): Text indicator if word is valid.
        error (list): Text indicator if word is invalid.
        binary_sm (list): Decorative text.
        jumbled_char (list): Decorative text.
    """

    def __init__(self):
        self.title = """ _ _ _ _____ _____ ____  _____ _____ _____ _____ 
| | | |     | __  |    \|  |  |  _  |     |  |  |
| | | |  |  |    -|  |  |     |     |   --|    -|
|_____|_____|__|__|____/|__|__|__|__|_____|__|__|"""
        self.title = self.title.split('\n')
        self.success = """ ___ _   _  ___ ___ ___  ___ ___ 
/ __| | | |/ __/ __/ _ \/ __/ __|
\__ \ |_| | (_| (_|  __/\__ \__ \\
|___/\__,_|\___\___\___||___/___/"""
        self.success = self.success.split('\n')
        self.error = """  ___ _ __ _ __ ___  _ __ 
 / _ \ '__| '__/ _ \| '__|
|  __/ |  | | | (_) | |   
 \___|_|  |_|  \___/|_|   """    
        self.error = self.error.split('\n')
        self.binary_sm = [
            "001001010011101010001101010010000010101",
			"110101101000111010011010000010010111010",
			"100011010000111101110000101010100101111",
			"000101011100000001100011011101000000111"
        ]
        self.jumbled_char = [
            "nmOVctcxFLxck3tgzbQE8fcvMrMlFeEtIbceiOK",
            "WlbJmc7oxClEfwFim5XjsXoeDEzJZYV0BDiSOQP",
            "gMIZzBqHy5sChTipMhJLzE8Pnn3EsKsV3j4GDer",
            "0OKsFJgTyc5O4cfH5RuHSGJVEn143BIXqZ8l56v",
            "fIBwwFtTSC8xuxJtc7S3nT3lCYP0JQk8oaWN0R4",
            "L5DBl4NdAey3GqpdTtot2mU82QO50Xva7U2r2GF",
            "MQ98jcmAiK46Tmi9GiQR23UkhuCvzdPOQ5WtnGL",
            "uBSTytmD60dS5q7CHRM8tZPqml5VlPX9ujrumdm",
            "Ys004jxcXACSpKGU47aiuESnJ1IBA9qH4sQZRSE",
            "9vXhG7JfBttIS4Fnqj9HJh1CW49Mtar3sCcClAF",
            "IssdhXRZjU6L7VzeuGH7xMIxS6K379lWu8OhYWG",
            "LxgDzQXB3Tsaty7GzPUhG1RIxcARv3mhzc8fSUB",
            "ZXczIqRCUxIZrtoRdYJw3F8KMDmpSBncB6EVnfW",
            "1kd68WEJYS58PpMSDwuHygWZCwNt6ZXFaz50ItR",
            "f2hQTPMarqQjZ4KILBHtd46h7DoYLu72fASOIgy",
            "GeCJE1wudjgDIufKV5nMF0gKsVMwMJQBRPPo0ic",
            "a6neV5HgGDQ91xrcANchStCk0IHltvbx1CpYBF8",
            "wKfHZVigJKBjL5MrW6TVYUOj3nzrr2Uc58LtvkY",
            "2W9IfxKuihbdzUxl4aqXfa9EgHluqaYcKqhMlFh",
            "ybsPmtGuPe7P08xugzjsDApx2EQw1f4MahWQlam"

        ]