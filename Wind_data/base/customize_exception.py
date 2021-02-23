def base_exception_print(self):
    if self.code is None:
        print(self.message)
    else:
        print(self.message + '[' + str(self.code) + ']')


class CustomizeException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message
        base_exception_print(self)






