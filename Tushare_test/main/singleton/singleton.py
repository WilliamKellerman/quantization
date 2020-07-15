class Singleton(object):
    """
    单例模式工具类
    """
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


@Singleton
class TestSingletonCls(object):
    def __init__(self):
        pass


# 测试

cls1 = TestSingletonCls()
cls2 = TestSingletonCls()
print(id(cls1) == id(cls2))
