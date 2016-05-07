

class CardBuilder:

    def __init__(self):
        pass

    def processPOST(self, pages, params):
        new_content = {}
        for page in pages:
            print(page)
            methodToCall = getattr(self, page)
            new_content[page] = methodToCall(params)
        return new_content


    def singlekanji(self, params):
        card_side = {}
        card_side['cardside'] = params['singlekanji_cardside']
        card_side['item_type'] = "single"
        card_side['bigkanji'] = params['bigkanji']
        return card_side

    def kanjifront(self, params):
        card_side = {}
        card_side['cardside'] = params['kanjifront_cardside']
        card_side['kanji'] = params['kanji']
        kun = []
        card_side['item_type'] = "kanjifront"
        kun.append(params['kuns'])
        card_side['kun'] = kun
        card_side['on'] = [params['ons']]
        param_words = params.getlist('word[]')
        param_word_kuns = params.getlist('word_kun[]')
        words = []
        for param_word, param_word_kun in zip(param_words, param_word_kuns):
            new_word = {}
            new_word['word'] = param_word
            new_word['word_kun'] = param_word_kun
            words.append(new_word)
        card_side['words'] = words;

        return card_side


    def kanjiback(self, params):
        card_side = {}
        card_side['cardside'] = params['kanjiback_cardside']
        card_side['item_type'] = "kanjiback"
        card_side['kanjitrans'] = params['kanjitrans']
        card_side['romaji'] = params['romaji']

        return card_side
