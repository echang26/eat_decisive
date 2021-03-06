from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from eat_decisive.models import LatestQuery, QueryForm
#from django.db import models
from rauth import OAuth1Service, OAuth1Session
from xml.dom.minidom import parse, parseString, getDOMImplementation
from bs4 import BeautifulSoup
import os
import json
import re
import random
import requests
import xml.etree.ElementTree as ET
import random
from urlparse import urlparse
import urllib2

#import settings

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

CONSUMER_KEY = get_env_variable('CONSUMER_KEY')
CONSUMER_SECRET = get_env_variable('CONSUMER_SECRET')

MOST_READ_US = 'https://www.goodreads.com/book/most_read'

request_token = ''
request_token_secret = ''
user_id = ''
session = ''
username = ''

url = 'http://www.goodreads.com'
page = requests.get(MOST_READ_US)

accepted = False

goodreads = OAuth1Service(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    name='goodreads',
    request_token_url='http://www.goodreads.com/oauth/request_token',
    authorize_url='http://www.goodreads.com/oauth/authorize',
    access_token_url='http://www.goodreads.com/oauth/access_token',
    base_url='http://www.goodreads.com/'
    )

class Book:
    def __init__(self, title, author, average_rating, url):
        self.title = title.encode('ascii', 'ignore')
        self.author = author.encode('ascii', 'ignore')
        self.average_rating = average_rating.encode('ascii', 'ignore')
        self.url = url.encode('ascii', 'ignore')
    def __str__(self):
        return "Book's title is %s, author is %s, average rating is %s, link is %s" % (self.title, self.author, self.average_rating, self.url) 
    def __repr__(self):
        return self.__str__()


def index(request):
    context_dict = {}  
    if len(list(LatestQuery.objects.all())) >= 1:
        recently_searched = [str(thing) for thing in LatestQuery.objects.order_by('-id')[:5]]
#        for thing in recently_searched:
#            print "and this" + thing
        context_dict['recentsearches'] = recently_searched
    return render(request, 'eat_decisive/index.html', context_dict)

def submit_query(request):
    context_dict = {}
    fail_message = None
    if request.method == 'POST':
        food_choices = request.POST['searched']
        #the entered foods were not separated by asterisks or something else is wrong with the query. 
        #We now define a fail message to communicate to the user.
        if len(food_choices.split('*')) <= 1:
            fail_message = "We're sorry...your stomach has us stumped. Did you enter foods separated by asterisks? Please try again."
            context_dict['fail_message'] = fail_message
        else:
            # form was successful
#            print "searched foods are", food_choices
            form = QueryForm(request.POST)
            if form.is_valid():
#                searched = form.searched()
#                latest = LatestQuery(searched = searched)
#                latest.save()
                form.save()
                context_dict['form'] = form
                # Save the new category to the database.
#                form.save(commit=True)
            edited_foods = [item.strip() for item in food_choices.split('*')]
            chosen_food = random.choice(edited_foods)
            # randomly choose a food from the list provided
            final_message = "Hooray! Your decision is..." + chosen_food
            # communicate the decision
#            print final_message

            context_dict['answer'] = final_message
    return render(request, 'eat_decisive/getdecision.html', context_dict)

def readdecisive(request):
    context_dict = {}
    return render(request, 'eat_decisive/readdecisive.html', context_dict)

def get_user_info():
    user_info = {}
    get_user = session.get('/api/auth_user.xml')
    xml_id = parseString(get_user.content)
    user_id = xml_id.getElementsByTagName('user')[0].attributes['id'].value
    username = xml_id.getElementsByTagName('name')
    user_info['user_id'] = str(user_id)
    user_info['username'] = username[0].firstChild.nodeValue
    return user_info

def readdecisivemember(request):
    global request_token, request_token_secret, user_id, session, username
    context_dict = {}
    url = request.get_full_path()
    parsed_url = urlparse(url)
    if parsed_url.query == '':
        context_dict['welcome'] = "Welcome, indecisive reader!"
    elif 'authorize=1' in parsed_url.query:
        session = goodreads.get_auth_session(request_token, request_token_secret, method='GET')
        userinfo = get_user_info()
        user_id = userinfo['user_id']
        username = userinfo['username']
        context_dict['welcome'] = "Welcome, " + username + "!"
#        ACCESS_TOKEN = session.access_token
#        ACCESS_TOKEN_SECRET = session.access_token_secret
#        print "your access token is ", ACCESS_TOKEN
    return render(request, 'eat_decisive/readdecisivemember.html', context_dict)

def goodreads_login(request):
    global request_token, request_token_secret
    request_token, request_token_secret = goodreads.get_request_token(header_auth=True)
    authorize_url = goodreads.get_authorize_url(request_token)
    accepted = True
    print "WOO! Redirect url is ", authorize_url
#    print 'Visit this URL in your browser: ' + authorize_url
#    accepted = 'n'
#    while accepted.lower() == 'n':
        # you need to access the authorize_link via a browser,
        # and proceed to manually authorize the consumer
#        accepted = raw_input('Have you authorized me? (y/n) ')
    return HttpResponseRedirect(authorize_url)
'''
def goodreads_redirect(request):
    url = request.get_full_path() + '/'
    print "redirect url is ", url
    return HttpResponseRedirect(url)
'''
def random_popular_book(request):
    book_soup = BeautifulSoup(page.content)
    book_links = book_soup.find_all("a", class_="bookTitle")
    popular_book_titles = [book.find('span').get_text() for book in book_links]
    popular_book_urls = [url + link.get('href') for link in book_links]
    book_dict = {}
    for idx in range(len(popular_book_urls)):
        book_dict[popular_book_titles[idx]] = popular_book_urls[idx]
    winning_book = random.choice(popular_book_titles)
    print "winning book is ", winning_book
    context_dict = {'winnerbook': winning_book, 'winnerurl': book_dict[winning_book]}
    return render(request, 'eat_decisive/popularbookgenerator.html', context_dict)

def get_shelf_books(user_id, shelf):
    global session
    get_request_link = 'http://www.goodreads.com/review/list/' + user_id + '?format=xml&shelf=' + shelf + '&per_page=200&key=' + CONSUMER_KEY + '&v=2'
    books_on_shelf = session.get(get_request_link)
    tree = ET.fromstring(books_on_shelf.content)
    books = []
    for libro in tree.findall('reviews/review/book'):
        books.append(Book(libro.find('title').text, libro.find('authors/author/name').text, libro.find('authors/author/average_rating').text, 'https://www.goodreads.com/book/show/'+ libro.find('id').text))
    return books    

def random_to_read(request):
    global user_id, username
    context_dict = {}
    books_to_read = get_shelf_books(user_id, 'to-read')
    random_book = random.choice(books_to_read)
    context_dict = {'name': username, 'title': random_book.title, 'author': random_book.author, 'url': random_book.url, 'average_rating': random_book.average_rating}
    return render(request, 'eat_decisive/whattoreadnext.html', context_dict)

def handler404(request):
    return render(request, '404.html')

def handler500(request):
    return render(request, '500.html')

def read_alternative(request):
    context_dict = {}
    return render(request, 'eat_decisive/readalternative.html', context_dict)

def read_result(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        starting_url = 'https://www.goodreads.com/' + username
        try:
            page = urllib2.urlopen(starting_url)
        except urllib2.HTTPError as e:
            if e.code == 404:
                context_dict = {}
                print "There was an error and the connection was refused."
                return render(request, 'eat_decisive/readalternativeerror.html', context_dict)
        except urllib2.URLError as e:
            print "The connection was refused."
            context_dict = {}
            return render(request, 'eat_decisive/readalternativeerror.html', context_dict)            
        else:        
            url = page.geturl()
            user_id = [int(s) for s in url if s.isdigit()]
            user_id = ''.join(map(str, user_id))
            print "user id is ", user_id
            homepage = 'https://www.goodreads.com/'
            to_read = 'https://www.goodreads.com/review/list/' + str(user_id) + '?shelf=to-read'
            html = urllib2.urlopen(to_read).read()
            book_soup = BeautifulSoup(html, "html.parser")
            all_books = []
            book_links = []
            for book in book_soup.find_all('a'):
                try:
                    if '/book/show/' in book['href']:
                        all_books.append(book['title'])
                        book_links.append(homepage + book['href'])
                except KeyError:
                    pass
            print "all books are ", all_books
            book_dict = {}
            for idx in range(len(book_links)):
                book_dict[all_books[idx]] = book_links[idx]
            winning_book = random.choice(all_books)
            print "winning book is ", winning_book
            print "winning book url is ", book_dict[winning_book]
            context_dict['name'] = username
            context_dict['winnerbook'] = winning_book
            context_dict['winnerurl'] = book_dict[winning_book]
    return render(request, 'eat_decisive/readalternativeresult.html', context_dict)

def read_error(request):
    context_dict = {}
    return render(request, 'eat_decisive/readalternativeerror.html', context_dict)

def foodgrades(request):
    context_dict = {}  
    return render(request, 'eat_decisive/dinedecisive.html', context_dict)

def foodgraderesults(request):
    context_dict = {}
    if request.method == 'POST':
        if len(request.POST['zipcode']) < 5:
            fail_message = "We're sorry...did you enter a valid zipcode? Please try again."
            context_dict['fail_message'] = fail_message
        #allow patrons to select their own boro by setting form data to boro 
        #and then setting roach_parameters['boro'] = request.POST['boro']
        else:
            roach_parameters = {'boro': 'MANHATTAN', 'violation_code': '04M', 'grade': 'A'}
            roach_parameters['zipcode'] = request.POST['zipcode']
            roach_query = requests.get("https://data.cityofnewyork.us/resource/xx67-kt59.json", params=roach_parameters)
            roach_data = roach_query.json()
            roach_restaurants = []
            for item in roach_data:
                if item['dba'] not in roach_restaurants:
                    roach_restaurants.append(item['dba'])
            context_dict['results'] = roach_restaurants
            if len(roach_restaurants) == 0:
                context_dict['nonefound'] = "Hooray! There were no restaurants found in your area."
    return render(request, 'eat_decisive/dinedecisiveresults.html', context_dict)