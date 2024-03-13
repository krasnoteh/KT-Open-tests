import subprocess
import os
import random
import sys
import json
import time
import os.path

class Tester_correlator():
    def __init__(self, path_to_exe_1, path_to_exe_2):
        self.request = ""
        self.path_to_exe_1 = path_to_exe_1
        self.path_to_exe_2 = path_to_exe_2
        self.process_1 = subprocess.Popen(self.path_to_exe_1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.process_2 = subprocess.Popen(self.path_to_exe_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
    def add_int(self, a):
        self.request = self.request + str(a) + ' '
    def add_string(self, s):
        self.request = self.request + s + ' '
    def enter(self):
        self.request+= '\n'
    def print_request(self):
        print(self.request)
    def test(self):
        stdout_1, stderr = self.process_1.communicate(input=self.request)
        stdout_2, stderr = self.process_2.communicate(input=self.request)
        if stderr:
            print("Ошибка в исполняемом exe файле")
            print(stderr)
        if (stdout_1 == stdout_2):
            pass
        else:
            print()
            print("=========== Найдено несоответствие ===========")
            print("Тест:")
            print(self.request)
            print()
            print("Правильный ответ:")
            print(stdout_1)
            print()
            print("Ответ программы:")
            print(stdout_2)
            print()
            
def stop():
    time.sleep(1000)
    quit()

try:
    with open("config.json") as config_file:
        config = json.load(config_file)
except Exception:
    print("конфигурационный файл не найден.")
    print("убедитесь, что 'config.json' находится в директории этого скрипта")
    stop()

try:
    mode = config["mode"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'mode'")
    stop()
    
try:
    labwork = config["labwork"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'labwork'")
    stop()
    
try:
    task = config["task"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'task'")
    stop()
    
try:
    exe_name = config["exe_name"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'exe_name'")
    stop()
    
try:
    number_of_tests = config["number_of_tests"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'number_of_tests'")
    stop()
    
try:
    test_size = config["test_size"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'test_size'")
    stop()
    
try:
    maximal_value = config["maximal_value"]
except Exception:
    print("в файле конфигурации нет необходимого параметра 'maximal_value'")
    stop()
    
if (mode != "correlate" and mode != "generate" and mode != "test"):
    print("в файле конфигурации 'mode' установлен неверно. Сейчас доступны режимы:")
    print("correlate")
    print("generate")
    print("test")
    stop()

    
print("выбран режим ", mode)

if mode == "correlate":
    correct_exe_path = "TestData" + "/" + "labwork" + str(labwork) + "/" + "task_" + task + "/" + "correct.exe"
    if not os.path.isfile(correct_exe_path):
        print("по заданным параметрам нет корректного exe файла")
        print("параметры поиска: ", correct_exe_path)
        stop()
    if not os.path.isfile(exe_name):
        print("не найден тестируемый exe файл")
        print("убедитесь, что файл находится в директории этого скрипта и имеет название "\
              , exe_name, " (устанавливается в config.json)")
        stop()
        
    pattern_path = "TestData" + "/" + "labwork" + str(labwork) + "/" + "task_" + task + "/" + "pattern.py"
    if not os.path.isfile(pattern_path):
        print("не найден файл паттерна для проверки")
        print("параметры поиска: ", pattern_path)
        stop()
        
    sys.path.insert(1, "TestData" + "/" + "labwork" + str(labwork) + "/" + "task_" + task + "/")
    
    
    t = Tester_correlator(correct_exe_path, exe_name)
    import pattern

    pattern.test_pattern(t, test_size, maximal_value)
            
    print("пример сгенерированного теста: ")
    t.print_request()
    
    print("начало тестирования")
    for i in range(number_of_tests):
        t = Tester_correlator(correct_exe_path, exe_name)
        pattern.test_pattern(t, test_size, maximal_value)
        t.test()
        if (i % (number_of_tests // 10) == 0):
            print("пройдено ", i, " тестов")
    
    print("все тесты пройдены")
    stop()