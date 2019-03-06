class ProgramError(Exception):

    def __init__(self, message):
        super(ProgramError, self).__init__(message)


class ProcessError(Exception):

    def __init__(self, command, returncode):
        self.message = ("Statement:%s, RetCode:%d" % (command, returncode))
        super(ProcessError, self).__init__(self.message)
        self.command = command
        self.returncode = returncode

    def getMsg(self):
        return self.message
