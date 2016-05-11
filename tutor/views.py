from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import View
from django.conf.urls import patterns, include, url
from couchbase.bucket import Bucket
from couchbase.views.iterator import View as CView
from couchbase.views.params import Query
from couchbase.n1ql import N1QLQuery, N1QLError
from couchbase.exceptions import CouchbaseError, NotFoundError
from uuid import uuid4
from tutor.cardbuilder import CardBuilder
from tutor.rules import RulesProvider


class TutorGroupsList(LoginRequiredMixin, View):
    LOGIN_URL = 'loginsys.views.login'
    template_name = 'tutor/tutor_groups_list.html'
    tutor_uid = 'user_sakuratutor'
    c = Bucket('couchbase://localhost/nihongo')

    def get(self, request):
        c = self.c
        user_uid = 'user_' + request.user.username
        print(user_uid)
        try:
            tutor_doc = c.get(user_uid)
        except Exception as e:
            raise Http404(e)
        tutor_uid = tutor_doc.key
        tutor_doc = tutor_doc.value

        invite_requests = []

        groups_list = []
        a_groups_list = []
        r_groups_list = []

        nq = N1QLQuery('SELECT *, META().id FROM `nihongo` WHERE doc_type=$doc_type and user_id=$tutor_uid', tutor_uid = user_uid, doc_type='invite_request')
        for row in c.n1ql_query(nq):
            ir = row['nihongo']
            ir['id'] = row['id']
            invite_requests.append(ir)

        for ir in invite_requests:
            group = c.get(ir['group_id']).value
            group['confirmed'] = ir['confirmed']
            r_groups_list.append(group)


        c_view = CView(c, "nihongo", "all_groups")
        for row in c_view:
            group = row.value
            group['id'] = row.docid
            #print(row.value)
            if row.key == user_uid:
                groups_list.append(group)
            else:
                a_groups_list.append(group)


        """nq = N1QLQuery('SELECT *, META().id FROM `nihongo` WHERE doc_type=$doc_type and tutor_uid=$tutor_uid', tutor_uid = user_uid, doc_type='group_doc')

        for row in c.n1ql_query(nq):
            #print(row)
            group = row['nihongo']
            group['id'] = row['id']
            groups_list.append(group)"""

        #print(tutor_doc)

        return render(request, self.template_name, { 'tutor_uid' : tutor_uid,
            'tutor_doc' : tutor_doc, 'groups_list' : groups_list, 'a_groups_list' : a_groups_list,
            'r_groups_list' : r_groups_list
        })


    def post(self, request):
        c = self.c
        user_uid = 'user_' + request.user.username
        if 'create_group' in request.POST:
            print("CREATING NEW GROUP")
            group_name = request.POST.get('group_name', 'Sample Name')
            description = request.POST.get('group_description', 'Sample Description')
            group_id = 'group_' + group_name + '_' + str(uuid4()).replace('-', '_')
            group = {'doc_type' : 'group_doc', 'tutor_uid' : user_uid, 'group_name' : group_name, 'description' : description}
            group['doc_channels'] = [group_id]
            group['decks_list'] = []
            try:
                c.upsert(group_id, group)
            except CouchbaseError as e:
                raise Http404('couchbaseeror')
            print(group)
        elif 'delete_group' in request.POST:
            print("DELTEING GROUP")
            group_id = request.POST['group_id']
            try:
                c.delete(group_id)
            except CouchbaseError as e:
                raise Http404(e)


        else:
            print("NOTHING HAPPENS")


        return HttpResponseRedirect(reverse('tutor:tutor_groups'))



def request_invite(request, user_id, group_id):
    default = 'request for invite from' + user_id
    request_text = request.POST.get('request_text', default)
    c = Bucket('couchbase://localhost/nihongo')
    invite_request = {'doc_type' : 'invite_request', 'user_id' : user_id, 'group_id' : group_id}
    invite_request['request_text'] = request_text
    invite_request['confirmed'] = "pending"
    ireq ='ireq_'  + str(uuid4()).replace('-', '_')
    c.upsert(ireq, invite_request)
    return HttpResponseRedirect(reverse('tutor:tutor_groups'))


class GroupDecksList(LoginRequiredMixin, View):
    template_name = 'tutor/group_decks_list.html'
    #group_id = 'g_sakura'
    #constgroup = 'sakura'
    #def __init__(self):
        #self.template_name = 'tutor/group_decks_list.html'

    def get(self, request, group_id):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")

        c = Bucket('couchbase://localhost/nihongo')
        group = c.get(group_id).value
        group_decks = group.get('decks_list')
        decks_list = []
        for d in group_decks:
            try:
                deck = c.get(d)
                decks_list.append(deck)
            except CouchbaseError:
                pass
        return render(request, self.template_name, {
             'decks_list' : decks_list,  'group' : group.get('group_name'), 'group_id' : group_id
        })

    def post(self, request, group_id):
        c = Bucket('couchbase://localhost/nihongo')
        success = 'dunno'
        constgroup = group_id.rsplit('_', 1)[0]
        print(constgroup)
        print('adding new deck')
        try:
            description = request.POST['description']
            print(description)
            ckey = 'deck_' + constgroup + '_' + str(uuid4()).replace('-', '_')

            newdeck = {'doc_type' : 'deck', 'description' : description, 'deck_name' : description}
            newdeck['cards_list'] = []
            c.insert(ckey, newdeck)
            group = c.get(group_id).value
            print(group.get('decks_list'))
            group.get('decks_list').append(ckey)
            c.upsert(group_id, group)
            success = 'success'
        except (BaseException, CouchbaseError) as e:
            success = 'error'
            print(e)

        group = c.get(group_id).value
        group_decks = group.get('decks_list')
        decks_list = []
        for d in group_decks:
            try:
                deck = c.get(d)
                decks_list.append(deck)
            except CouchbaseError:
                pass
        return HttpResponseRedirect(reverse('tutor:group_decks', kwargs={'group_id' : group_id}))


class GroupDecksDelete(LoginRequiredMixin, View):
    template_name = 'tutor/group_decks_list.html'
    constgroup = 'sakura'
    #def __init__(self):
        #self.template_name = 'tutor/group_decks_list.html'

    def post(self, request, group_id, deck_id):
        c = Bucket('couchbase://localhost/nihongo')
        success = 'dunno'
        print('deleting deck')
        try:
            c.delete(deck_id)
            group = c.get(group_id).value
            print(group.get('decks_list'))
            group.get('decks_list').remove(deck_id)
            c.upsert(group_id, group)
            success = 'success'
        except (BaseException, CouchbaseError) as e:
            success = 'error'
            print(e)

        group = c.get(group_id).value
        group_decks = group.get('decks_list')
        decks_list = []
        for d in group_decks:
            try:
                deck = c.get(d)
                decks_list.append(deck)
            except CouchbaseError:
                pass
        return HttpResponseRedirect(reverse('tutor:group_decks', kwargs={'group_id' : group_id}))




class DeckDetail(LoginRequiredMixin, View):

    def get(self, request, group_id, deck_id):
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

        rulesProvider = RulesProvider()

        task_types = rulesProvider.provideTaskTypeList()
        #return HttpResponse(response)
        return render(request, 'tutor/deck_detail.html', { 'group_id' : group_id,
            'deck_id' : deck_id, 'deck' : deck.value, 'cards_set' : cards_set, 'task_types' : task_types,
        })




class AddCardToDeck(View):

    def post(self, request):
        pass

class DeckEdit(LoginRequiredMixin, View):
    #template_name = 'tutor/deck_detail.html'

    def post(self, request, group_id, deck_id, *args, **kwargs):
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
            return HttpResponseRedirect(reverse('tutor:deck_detail', kwargs={'group_id' : group_id,'deck_id' : deck_id}))
        if 'edit_card' in request.POST:
            try:
                card_id = request.POST['card_id']
                return HttpResponseRedirect(reverse('tutor:edit_card', kwargs={'group_id' : group_id, 'deck_id' : deck_id, 'card_id' : card_id}))
            except BaseException as e:
                print(e)
                raise Http404()
        if 'create_card' in request.POST:
            print("CREATING A NEW CARD IN DECK")
            try:
                task_type = request.POST['task_type']
                card_id = 'card_'  + str(uuid4()).replace('-', '_')
                print("SUCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSss")
                return HttpResponseRedirect(reverse('tutor:edit_card', kwargs={'group_id' : group_id, 'deck_id' : deck_id, 'card_id' : card_id, 'is_new' : True, 'task_type' : task_type}))
            except (BaseException, CouchbaseError) as e:
                print(e)
                raise Http404(e)

        else:
            print("nothing happened")
            return HttpResponseRedirect(reverse('tutor:deck_detail', kwargs={'group_id' : group_id,'deck_id' : deck_id}))
            #return HttpResponseRedirect(reverse('tutor:edit_card', kwargs={'group_id' : group_id, 'card_id' : card_id}))



class EditCard(LoginRequiredMixin, View):
    template_name = 'tutor/edit_card.html'
    c = Bucket('couchbase://localhost/nihongo')
    def get(self, request, group_id, deck_id, card_id, is_new = False, task_type = False):
        c = self.c
        if 'cancel_changes' in request.GET:
            #print("CANCEL CHANGES")
            return HttpResponseRedirect(reverse('tutor:deck_detail', kwargs={'group_id' : group_id,'deck_id' : deck_id}))

        rulesProvider = RulesProvider()
        availablePages = rulesProvider.provideTemplateList()
        task_types = rulesProvider.provideTaskTypeList()

        #deck['cards_list'].append(card_id)
        #c.upsert(deck_id, deck)
        #print(task_types)
        #for template in available:
            #print(template)

        try:
            card = c.get(card_id).value

        except NotFoundError:


            card = {'content' : [], 'card_info' : {'lvl' : 'N5', 'task_type' : task_type}}
        card_sides = card.get('content')
        card_info = card.get('card_info')
        pages = []
        template_dict = {}
        sides_number = 0
        info_dict = {}

        for info in card_info:
            info_dict[info] = card_info.get(info)
        template_dict['card_info'] = info_dict
        template_dict['available_pages'] = availablePages
        sides_list= []
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

            side_dict['page_name'] = 'tutor/' + side.get('item_type') + '.html'
            sides_list.append(side_dict)

            #template_dict[side.get('item_type')] = side_dict
            page = {}
            page['pageName'] = 'tutor/' + side.get('item_type') + '.html'
            page['cardside'] = side.get('cardside')
            pages.append(page)
        sides_list = sorted(sides_list, key = lambda side:side['cardside'])

        #print(pages)
        template_dict['task_type'] = task_type
        template_dict['task_types'] = task_types
        template_dict['sides_list'] = sides_list
        template_dict['sides_number'] = sides_number
        template_dict['card'] = card
        template_dict['card_id'] = card_id
        template_dict['deck_id'] = deck_id
        if is_new:
            template_dict['is_new'] = is_new
        template_dict['group_id'] = group_id
        return render(request, self.template_name, template_dict)
    #This method gets changes in card structure and updates DB

    def post(self, request, group_id, deck_id, card_id, is_new = False):
        post_par = []
        c = Bucket('couchbase://localhost/nihongo')
        for param in request.POST:
            pass
            #print(param + " " + request.POST[param])

        #words = request.POST.getlist("word[]")
        cardBuilder = CardBuilder();
        pages = request.POST.getlist("pages[]")
        card_to_save = cardBuilder.processPOST(pages, request.POST)

        is_new = request.POST.get('is_new', False)
        if is_new:
            deck = c.get(deck_id).value
            print(deck.get('cards_list'))
            deck['cards_list'].append(card_id)
            c.upsert(deck_id, deck)


        #print(cardBuilder.processPOST(pages, request.POST))
        c.upsert(card_id, card_to_save)

        #for word in words:
         #   print(word)

        return HttpResponseRedirect(reverse('tutor:edit_card', kwargs={'group_id' : group_id, 'deck_id' : deck_id,'card_id' : card_id}))

class CreateCard(View):
    pass




def get_chunk(request):
    print("IM BEING CALLED")
    rulesProvider = RulesProvider()
    availablePages = rulesProvider.provideTemplateList()
    task_types = rulesProvider.provideTaskTypeList()
    template_name = 'tutor/chunks/' + request.GET['template_name']
    fill_dict = {}
    chunk_id = request.GET.get('chunk_id', False)
    cardside = request.GET['cardside']
    lvl = request.GET.get('lvl', False)
    sides_number = request.GET.get('sides_number', False)
    #for param in request.GET:
        #print(param + " " + request.GET[param])#
    return render(request, template_name, {'fill_dict' : fill_dict, 'chunk_id' : chunk_id, 'sides_number' : sides_number,
                                           'available_pages' : availablePages, 'cardside' : cardside, 'lvl' : lvl, 'task_types' : task_types})






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