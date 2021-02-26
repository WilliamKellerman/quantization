class ClassTestDemo:
    public_param = True
    __private_param = True

    static_param = 0

    def __init__(self, param):
        self.param = param

    def show(self):
        print(ClassTestDemo.static_param, self.static_param, self.param)

    @classmethod
    def show_public_private(cls):
        print(ClassTestDemo.public_param, ClassTestDemo.__private_param)


def class_test():
    # 对象两个变量分别赋值
    demo_1 = ClassTestDemo(1)
    demo_2 = ClassTestDemo(2)
    demo_1.static_param = 3
    demo_2.static_param = 4

    # 通过class对静态变量赋值
    ClassTestDemo.static_param = 1

    # 通过打印发现，如果对象操作过静态变量，则class对静态变量的赋值无法作用到对象上
    demo_1.show()
    demo_2.show()


def public_private_test():
    # 在class外部对class两个静态变量进行赋值
    ClassTestDemo.public_param = False
    ClassTestDemo.__private_param = False

    # 根据打印得出结论，外部对class私人静态变量的赋值是无法生效的
    ClassTestDemo.show_public_private()


# class_test()
public_private_test()
