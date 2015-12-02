
class User():
    def comparePasswd(self,passwd):
        if self.passwd == passwd:
            return True
        else:
            return False

    def __init__(self):
        """index变量是指明了当前用户现在看到了哪里"""
        self.name = None
        self.connection = None
        self.logged = False
        self.isAdmin = False
        self.state = 0
        self.index = -1
