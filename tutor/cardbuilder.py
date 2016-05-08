

class CardBuilder:


    def __init__(self):
        pass

    def processPOST(self, pages, params):
        card_to_save = {}
        card_content = []

        for page in pages:
            print(page)
            methodName = page.split('_s', 2)[0]
            cardside = page.split('_s', 2)[1]
            methodToCall = getattr(self, methodName)
            card_content.append(methodToCall(params, cardside))

        card_to_save['content'] = card_content
        card_to_save['card_info'] = self.card_info(params)
        card_to_save['features'] = self.features(params)
        card_to_save['doc_channels'] = self.doc_channels(params)
        card_to_save['doc_type'] = 'flashcard'
        card_to_save['doc_name'] = 'Карточка созданная в nihongo tutor'

        return card_to_save


    def singlekanji(self, params, cardside):
        card_side = {}
        card_side['cardside'] = cardside
        card_side['item_type'] = "singlekanji"
        #ind = 'bigkanji_' + cardside
        card_side['bigkanji'] = params['bigkanji_s' + cardside]

        return card_side

    def kanjifront(self, params, cardside):
        card_side = {}
        card_side['cardside'] = cardside
        card_side['kanji'] = params['kanji_s' + cardside]
        kun = []
        card_side['item_type'] = "kanjifront"
        kun.append(params['kuns_s' +  cardside])
        card_side['kun'] = kun
        card_side['on'] = [params['ons_s'  + cardside]]
        param_words = params.getlist('word_s' + cardside + '[]')
        param_word_kuns = params.getlist('word_kun_s' + cardside + '[]')
        words = []
        for param_word, param_word_kun in zip(param_words, param_word_kuns):
            new_word = {}
            new_word['word'] = param_word
            new_word['word_kun'] = param_word_kun
            words.append(new_word)
        card_side['words'] = words;

        return card_side


    def kanjiback(self, params, cardside):
        card_side = {}
        card_side['cardside'] = cardside
        card_side['item_type'] = "kanjiback"
        card_side['kanjitrans'] = params['kanjitrans_s' + cardside]
        card_side['kanjiromaji'] = params['kanjiromaji_s' + cardside]

        return card_side

    def card_info(self, params):
        card_info = {}
        lvl = params['lvl_select']
        card_info['task_type'] = params.get('task_type_select', 'kanji_card')
        card_info['lvl'] = lvl

        return card_info

    def doc_channels(self, params):
        doc_channels = []
        doc_channels.append('sakura')
        return doc_channels

    def features(self, params):
        features = []
        features.append('bad')

        return features

