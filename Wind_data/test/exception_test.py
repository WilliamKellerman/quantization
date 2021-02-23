from customize_exception import CustomizeException


def test_customize_exception():
    y = 1
    if y > 0:
        raise CustomizeException(404, 'Invalid response, status_code=')
    else:
        raise CustomizeException(None, 'Invalid response: Result is None')


def test_catch_customize_exception():
    try:
        test_customize_exception()
    except CustomizeException as e:
        raise Exception(e.message + str(e.code))


test_catch_customize_exception()
# test_customize_exception()
