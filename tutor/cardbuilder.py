

class CardBuilder:


    def __init__(self):
        pass

    def processPOST(self, pages, params):
        card_content = []

        for page in pages:
            print(page)
            methodName = page.split('_', 2)[0]
            cardside = page.split('_', 2)[1]
            methodToCall = getattr(self, methodName)
            card_content.append(methodToCall(params, cardside))

        return card_content


    def singlekanji(self, params, cardside):
        card_side = {}
        card_side['cardside'] = cardside

        #ind = 'bigkanji_' + cardside
        card_side['bigkanji'] = params['bigkanji_' + cardside]

        return card_side

    def kanjifront(self, params, cardside):
        card_side = {}
        card_side['cardside'] = cardside
        card_side['kanji'] = params['kanji_' + cardside]
        kun = []
        card_side['item_type'] = "kanjifront"
        kun.append(params['kuns_' +  cardside])
        card_side['kun'] = kun
        card_side['on'] = [params['ons_'  + cardside]]
        param_words = params.getlist('word_' + cardside + '[]')
        param_word_kuns = params.getlist('word_kun_' + cardside + '[]')
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
        card_side['kanjitrans'] = params['kanjitrans_' + cardside]
        card_side['romaji'] = params['romaji' + carside]

        return card_side
