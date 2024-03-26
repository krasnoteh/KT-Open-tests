#импорт разного
import subprocess
import os
import random
import sys
import json
import time
import os.path

#задержка при завершении/ошибке чтобы консоль не закрывалась
def stop():
    #raise KeyError(f"err")
    time.sleep(10000)
    quit()
    
#автоопределение ос
def OsCheck():
    global extention
    if os.name == "nt":
        extention = ".exe"
        print("Инициализация KrasnoTeh OpenTests v 2.0 - windows")
    else:
        extention = ""
        print("Инициализация KrasnoTeh OpenTests v 2.0 - linux")

#работает с бинарниками
class AppWrapper():
    def __init__(self, path_to_binary):
        self.path_to_binary = path_to_binary
    def exists(self):
        return os.path.isfile(self.path_to_binary)
    def load(self):
        self.process = subprocess.Popen(self.path_to_binary, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    def send_request(self, request):
        self.stdout, stderr = self.process.communicate(input=request)
        if stderr:
            print("Ошибка в исполняемом файле")
            print(stderr)
    
#формирует тест
class TestGenerator():
    def __init__(self):
        self.request = ""
    def add_int(self, a):
        self.request = self.request + str(a) + ' '
    def add_string(self, s):
        self.request = self.request + s + ' '
    def enter(self):
        self.request+= '\n'
    def print_request(self):
        print(self.request)
        
#загружает и проверяет конфиг
class ConfigLoader():
    def __init__(self):
        if not os.path.isfile("config.json"):
            print("конфигурационный файл не найден.")
            print("убедитесь, что 'config.json' находится в директории этого скрипта")
            stop()
        with open("config.json") as config_file:
            self.config = json.load(config_file)
        expected_keys = {
            "mode": str,
            "path_to_project": str,
            "task": str,
            "path_to_tested_binary": str,
            "number_of_tests": int,
            "test_size": int,
            "maximal_value": int,
            "stop_after_incorrelation": bool,
            "trim_outputs": bool
        }
        for key, expected_type in expected_keys.items():
            if key not in self.config:
                print(f"Не найдена необходимая переменная '{key}' в конфигурационном файле")
                stop()
            if not isinstance(self.config[key], expected_type):
                print(f"Переменная '{key}' в конфигурационном файле имеет неверный тип. Ожидалось {expected_type.__name__}")
                stop()
        supported_modes = {
            "correlate",
            "generate",
            "test"
        }
        if self.config["mode"] not in supported_modes:
            print("Сейчас поддерживаются режимы:")
            for mode in supported_modes:
                print(mode)
            print("(Указан '" + self.config["mode"] + "')")
        
        
#проверяет, можно ли начать выполнение задачи
def Validate(config):
    if not os.path.isdir(config["path_to_project"]):
        print("Не найден директорий проекта по адресу:")
        print(config["path_to_project"])
        stop()
    task_path = config["path_to_project"] + '/' + config["task"]
    if not os.path.isdir(task_path):
        print("Не найден директорий задачи по адресу:")
        print(task_path)
        stop()
    if not os.path.isfile(config["path_to_tested_binary"]):
        print("Не найден проверяемый бинарный файл по адресу:")
        print(config["path_to_tested_binary"])
        stop()
    found_correct = os.path.isfile(task_path + '/' + "correct" + extention)
    found_pattern = os.path.isfile(task_path + '/' + "pattern.py")
    found_frozen = os.path.isfile(task_path + '/' + "frozen_tests.json")
    if (not found_correct and not found_pattern and not found_frozen):
        print("По заданным параметрам не найдено ни одного ресурса для тестирования.")
        print("Поиск велся в:")
        print(task_path + '/')
        stop()
    if (not found_frozen and config["mode"] == "test"):
        print("Для данного режима не найден необходимый файл тестов 'frozen_tests.json'")
        if (found_correct and found_pattern):
            print("Однако найдены необходимые файлы для запуска генерации тестов или коррелятора")
            print("Вы можете перезапустить скрипт с параметром режима 'generate' или 'correlate'")
        else:
            print("Поиск велся по:")
            print(task_path + '/' + "frozen_tests.json")
        stop()
    if (not (found_correct and found_pattern) and (config["mode"] == "generate" or config["mode"] == "correlate")):
        print("Для данного режима не найден один из файлов 'correct" + extention + "' и 'pattern.py'")
        if (found_frozen):
            print("Однако найден необходимый файлы для запуска проверки по готовым тестам")
            print("Вы можете перезапустить скрипт с параметром режима 'test'")
        stop()
        
#загружает файл теста frozen_tests.json и проверяет его на корректность
class TestLoader():
    def __init__(self, path_to_frozen_tests):
        with open(path_to_frozen_tests) as test_file:
            self.tests = json.load(test_file)
        if "tests" not in self.tests:
            print("в frozen_tests.json должен быть параметр 'tests'")
            stop()
        if not isinstance(self.tests["tests"], list):
            print("Параметр 'tests' в frozen_tests.json должен иметь тип 'list'")
            stop()
        for test in self.tests["tests"]:
            if "request" not in test or \
            "answer" not in test or \
            not isinstance(test["request"], str) or \
            not isinstance(test["answer"], str):
                print("в frozen_tests.json найден нечитаемый тест:")
                print(test)
                print("В тесте должны быть параметры 'request' и 'answer' типа 'str'")
                stop()

#выполняет сравнение двух строк, выводит сообщение о несовпадении
def CompareResults(request, string_1, string_2, use_trim):
    if use_trim:
        string_1 = string_1.strip()
        string_2 = string_2.strip()
        request = request.strip()
    if string_1 == string_2:
        return True
    else:
        print("==Несоответствие======")
        print("==Тест================")
        print(request)
        print("==Правильный ответ===")
        print(string_1)
        print("==Ответ программы====")
        print(string_2)
        print("=====================")
            
    
OsCheck() 
c = ConfigLoader()
config = c.config
Validate(config)

if (config["mode"] == "test"):
    t = TestLoader(config["path_to_project"] + '/' + config["task"] + '/' + "frozen_tests.json")
    incorrect_counter = 0
    for i, test in enumerate(t.tests["tests"]):
        process = AppWrapper(config["path_to_tested_binary"])
        process.load()
        process.send_request(test["request"])
        if not CompareResults(test["request"], test["answer"], process.stdout, config["trim_outputs"]):
            incorrect_counter+=1
        if incorrect_counter > 0 and config["stop_after_incorrelation"]:
            print("Проверка остановлена")
            stop()
        if (i % ((len(t.tests["tests"]) // 10)+1) == 0):
            print("проверено ", i + 1, " тестов")
    if (incorrect_counter == 0):
        print("Все тесты пройдены")
    else:
        print("Пройдено успешно:", config["number_of_tests"] - incorrect_counter)
        print("Ошибок:", incorrect_counter)
            
if (config["mode"] == "generate"):
    print("идет генерация...")
    sys.path.insert(1, config["path_to_project"] + '/' + config["task"] + '/' )
    import pattern
    tests_object = {
        "task_name" : config["task"],
        "autor" : "autogenerated by KrasnoTeh OpenTests v 2.0",
        "tests" : []
    }
    for i in range(config["number_of_tests"]):
        t = TestGenerator()
        pattern.test_pattern(t, config["test_size"], config["maximal_value"])
        process = AppWrapper(config["path_to_project"] + '/' + config["task"] + '/' + "correct" + extention)
        process.load()
        process.send_request(t.request)
        current_test = {
            "request" : t.request,
            "answer" : process.stdout
        }
        tests_object["tests"].append(current_test)
    with open(config["path_to_project"] + '/' + config["task"] + "/frozen_tests.json", "w") as outfile: 
        json.dump(tests_object, outfile, indent=2)
    print("генерация завершена")
    print("результат сохранен в", config["path_to_project"] + '/' + config["task"] + "/frozen_tests.json")
        
if (config["mode"] == "correlate"):
    sys.path.insert(1, config["path_to_project"] + '/' + config["task"] + '/' )
    import pattern
    incorrect_counter = 0
    for i in range(config["number_of_tests"]):
        t = TestGenerator()
        pattern.test_pattern(t, config["test_size"], config["maximal_value"])
        correct_process = AppWrapper(config["path_to_project"] + '/' + config["task"] + '/' + "correct" + extention)
        correct_process.load()
        correct_process.send_request(t.request)
        tested_process = AppWrapper(config["path_to_tested_binary"])
        tested_process.load()
        tested_process.send_request(t.request)
        if not CompareResults(t.request, correct_process.stdout, tested_process.stdout, config["trim_outputs"]):
            incorrect_counter+=1
        if incorrect_counter > 0 and config["stop_after_incorrelation"]:
            print("Проверка остановлена")
            stop()
        if (i % ((config["number_of_tests"] // 10)+1) == 0):
            print("проверено ", i + 1, " тестов")
    if (incorrect_counter == 0):
        print("Все тесты пройдены")
    else:
        print("Пройдено успешно:", config["number_of_tests"] - incorrect_counter)
        print("Ошибок:", incorrect_counter)
        
stop()
