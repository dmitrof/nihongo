

class RulesProvider:
    template_list={}
    task_type_list = {}
    def __init__(self):
        self.template_list = {"singlekanji" : "Только кандзи", "kanjifront" : "Кандзи, кана и примеры", "kanjiback" : "Перевод и транскрипция"}
        #self.template_list["1of4_question"] = "Тест с 4 опциями"
        self.task_type_list = {"no_task" : "no_task", "kanji_card" : "Карточка кандзи", "vocab_test" : "Тест на лексику", "text_test" : "Тест на чтение"}
        pass

    def provideTemplateList(self):
        return self.template_list

    def provideTaskTypeList(self):
        return self.task_type_list