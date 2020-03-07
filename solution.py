import json


class Solution:

    name = ""
    link = ""
    compiler = ""
    send_date = ""
    code = ""
    time = 0
    memory = 0  # KiB

    def __init__(self, name, text, link, compiler, send_date, time, memory, code):
        self.name = name
        self.text = text
        self.compiler = compiler
        self.send_date = send_date
        self.time = time
        self.memory = memory
        self.code = code
        self.link = link

    def __str__(self):
        return "{}\n{}\n{}\n{} ms\n{} KiB\n\n{}\n\n)".format(self.name, self.compiler, self.send_date,
                                                     self.time, self.memory, self.code)
