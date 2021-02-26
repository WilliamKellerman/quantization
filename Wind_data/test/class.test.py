class A:
    a1 = 0

    def __init__(self, a2):
        self.a2 = a2

    def show(self):
        print(A.a1, self.a1, self.a2)


def test_class():
    obj1 = A(1)
    obj2 = A(2)
    obj3 = A(3)

    obj1.a1 = 4
    obj2.a1 = 5
    obj3.a1 = 6

    A.a1 = 1
    # A.a2 = 2
    # A.a3 = 3
    obj1.show()
    obj2.show()
    obj3.show()


test_class()
