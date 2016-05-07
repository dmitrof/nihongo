from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.conf.urls import patterns, include, url
from couchbase.bucket import Bucket
from couchbase.views.iterator import View as CView
from couchbase.views.params import Query
from couchbase.n1ql import N1QLQuery, N1QLError
from couchbase.exceptions import CouchbaseError
from uuid import uuid4
from tutor.cardbuilder import CardBuilder
from tutor.rules import RulesProvider

class GroupDecksList(View):
    template_name = 'tutor/group_decks_list.html'
    group_id = 'g_sakura'
    constgroup = 'sakura'
    #def __init__(self):
        #self.template_name = 'tutor/group_decks_list.html'

    def get(self, request, *args, **kwargs):
        c = Bucket('couchbase://localhost/nihongo')
        group = c.get('g_sakura').value
        group_decks = group.get('decks_list')
        decks_list = []
        for d in group_decks:
            try:
                deck = c.get(d)
                decks_list.append(deck)
            except CouchbaseError:
                pass
        return render(request, self.template_name, {
            'pr': "hello, костыль", 'decks_list' : decks_list,  'group' : group.get('group_name')
        })

    def post(self, request,  *args, **kwargs):
        c = Bucket('couchbase://localhost/nihongo')
        success = 'dunno'
        print('adding new deck')
        try:
            description = request.POST['description']
            print(description)
            ckey = 'd_' + self.constgroup + '_' + str(uuid4()).replace('-', '_')

            newdeck = {'doc_type' : 'deck', 'description' : description}
            newdeck['cards_list'] = [];
            c.insert(ckey, newdeck)
            group = c.get(self.group_id).value
            print(group.get('decks_list'))
            group.get('decks_list').append(ckey)
            c.upsert(self.group_id, group)
            success = 'success'
        except (BaseException, CouchbaseError) as e:
            success = 'error'
            print(e)

        group = c.get(self.group_id).value
        group_decks = group.get('decks_list')
        decks_list = []
        for d in group_decks:
            try:
                deck = c.get(d)
                decks_list.append(deck)
            except CouchbaseError:
                pass
        return render(request, 'tutor/group_decks_list.html', {
            'decks_list' : decks_list,  'group' : group.get('group_name'), 'success' : success
        })
        #return HttpResponse('ok')

class GroupDecksDelete(View):
    template_name = 'tutor/group_decks_list.html'
    group_id = 'g_sakura'
    constgroup = 'sakura'
    #def __init__(self):
        #self.template_name = 'tutor/group_decks_list.html'

    def post(self, request, deck_key,  *args, **kwargs):
        c = Bucket('couchbase://localhost/nihongo')
        success = 'dunno'
        print('deleting deck')
        try:
            c.delete(deck_key)
            group = c.get(self.group_id).value
            print(group.get('decks_list'))
            group.get('decks_list').remove(deck_key)
            c.upsert(self.group_id, group)
            success = 'success'
        except (BaseException, CouchbaseError) as e:
            success = 'error'
            print(e)

        group = c.get(self.group_id).value
        group_decks = group.get('decks_list')
        decks_list = []
        for d in group_decks:
            try:
                deck = c.get(d)
                decks_list.append(deck)
            except CouchbaseError:
                pass
        return render(request, 'tutor/group_decks_list.html', {
            'decks_list' : decks_list,  'group' : group.get('group_name'), 'success' : success
        })




class DeckDetail(View):

    def get(self, request, deck_id, *args, **kwargs):
        response = "hello, {}".format(deck_id)
        b = Bucket('couchbase://localhost/nihongo')
        deck = b.get(deck_id)
        cards_list = deck.value.get('cards_list')
        cards_set = []
        for c in cards_list:
            try:
                card = b.get(c)
                cards_set.append(card)
            except CouchbaseError:
                pass

        #return HttpResponse(response)
        return render(request, 'tutor/deck_detail.html', {
            'deck_id' : deck_id, 'deck' : deck.value, 'cards_set' : cards_set
        })




class AddCardToDeck(View):

    def post(self, request):
        pass

class DeckEdit(View):
    template_name = 'tutor/deck_deatil.html'

    def post(self, request, deck_id, *args, **kwargs):
        c = Bucket('couchbase://localhost/nihongo')
        success = 'dunno'
        if 'delete_card' in request.POST:
            try:
                card_id = request.POST['card_id']
                print(card_id)
                deck = c.get(deck_id).value
                print(deck.get('cards_list'))
                deck.get('cards_list').remove(card_id)
                c.upsert(deck_id, deck)
                success = 'success'
            except (BaseException, CouchbaseError) as e:
                success = 'error'
                print(e)
            return HttpResponseRedirect(reverse('tutor:deck_detail', kwargs={'deck_id' : deck_id}))
        if 'edit_card' in request.POST:
            try:
                card_id = request.POST['card_id']
                return HttpResponseRedirect(reverse('tutor:edit_card', kwargs={'card_id' : card_id}))
            except BaseException as e:
                print(e)


class Edit_Card(View):
    template_name = 'tutor/edit_card.html'

    def get(self, request, card_id):
        rulesProvider = RulesProvider()
        availablePages = rulesProvider.provideTemplateList()
        #for template in available:
            #print(template)
        c = Bucket('couchbase://localhost/nihongo')
        card = c.get(card_id).value
        card_sides = card.get('content')
        pages = []
        template_dict = {}
        sides_number = 0
        info_dict = {}
        card_info = card.get('card_info')
        for info in card_info:
            info_dict[info] = card_info.get(info)
        template_dict['card_info'] = info_dict
        template_dict['available_pages'] = availablePages
        sides_set = {}
        for side in card_sides:
            side_dict = {}
            sides_number += 1
            for key in side:
                value = side.get(key)
                if not isinstance(value, str):pass
                    #value = str(value)
                side_dict[key] = value
            #side_dict['cardside'] += str((int(side_dict['cardside']) + 1))
            #side_dict['cardside'] += 1
            sides_set[side.get('item_type')] = side_dict
            template_dict[side.get('item_type')] = side_dict
            page = {}
            page['pageName'] = 'tutor/' + side.get('item_type') + '.html'
            page['cardside'] = side.get('cardside')
            pages.append(page)

        pages = sorted(pages, key = lambda page:page['cardside'])

        print(pages)

        template_dict['sides_set'] = sides_set
        template_dict['sides_number'] = sides_number
        template_dict['card'] = card
        template_dict['card_id'] = card_id
        template_dict['pages'] = pages
        return render(request, self.template_name, template_dict)
    #This method gets changes in card structure and updates DB
    def post(self, request, card_id):
        post_par = []
        c = Bucket('couchbase://localhost/nihongo')



        for param in request.POST:
            print(param + " " + request.POST[param])

        #words = request.POST.getlist("word[]")
        cardBuilder = CardBuilder();
        pages = request.POST.getlist("pages[]")
        print(cardBuilder.processPOST(pages, request.POST))

        #for word in words:
         #   print(word)

        return HttpResponseRedirect(reverse('tutor:edit_card', kwargs={'card_id' : card_id}))



def get_chunk(request):
    print("IM BEING CALLED")
    rulesProvider = RulesProvider()
    availablePages = rulesProvider.provideTemplateList()
    template_name = 'tutor/chunks/' + request.GET['template_name']
    fill_dict = request.GET.get('fill_dict', False)
    chunk_id = request.GET['chunk_id']

    print(chunk_id)
    #for param in request.GET:
        #print(param + " " + request.GET[param])
    return render(request, template_name, {'fill_dict' : fill_dict, 'chunk_id' : chunk_id, 'available_pages' : availablePages})


    """if 'name' in request.POST:
            return HttpResponse('збс')
        else:
            return HttpResponse('не норм')"""




"""card = c.get(card_id).value
        card_content = card.get('content')
        for param in request.POST:
            for i, side in enumerate(card_content):
                if side.get(param) != None:
                    side[param] = request.POST[param]
                    card_content[i] = side



        card['content'] = card_content
        c.upsert(card_id, card)"""













# Create your views here.
#cards_set = CView(c, 'nihongo', 'cards_list')
        #cards_list = []
#for row in cards_set:
        #cards_list.append(row)
#nq = N1QLQuery('SELECT * FROM `nihongo` WHERE META().id=$ds', ds = decks)
 #       decks_list = []
 #       for row in c.n1ql_query(nq):
 #           decks_list.append(row)
#for row in result_set:
         #   decks_list.append(row)