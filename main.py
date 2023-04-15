import os
from datetime import datetime
import regex_hw.regexMain as regexHW


def logger(oldFunction):
    path = 'main.log'
        
    def newFunction(*args, **kwargs):
        with open('main.log', 'a') as logFile:
            line = ''
            line = f'{datetime.now()}: func={oldFunction.__name__}, args={args}, kwargs={kwargs}, '
            res = oldFunction(*args, **kwargs)
            line += f'res={res}\n'
            logFile.write(line)
            return res
        
    return newFunction

def plogger(path):
    
    def __logger(oldFunction):
        def new_function(*args, **kwargs):
            with open(path, 'a') as logFile:
                line = ''
                line = f'{datetime.now()}: func={oldFunction.__name__}, args={args}, kwargs={kwargs}, '
                res = oldFunction(*args, **kwargs)
                line += f'res={res}\n'
                logFile.write(line)
                return res

        return new_function
        
    return __logger



def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @plogger(path)
        def hello_world():
            return 'Hello World'

        @plogger(path)
        def summator(a, b=0):
            return a + b

        @plogger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'



if __name__ == '__main__':
    test_1()
    test_2()
    regexHW.run()