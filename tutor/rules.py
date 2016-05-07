

class RulesProvider:
    templateList=[]
    def __init__(self):
        self.templateList = {"singlekanji" : "Только кандзи", "kanjifront" : "Кандзи, кана и примеры", "kanjiback" : "Перевод и транскрипция"}
        #self.templateList["1of4_question"] = "Тест с 4 опциями"
        pass

    def provideTemplateList(self):
        return self.templateList

