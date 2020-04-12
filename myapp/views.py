from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from myapp.models import Playersinfo
import datetime
import requests
from bs4 import BeautifulSoup
from lxml import html
from .forms import PlayerForm

# Create your views here.
def dailygames(m,d,y):
    global games
    games = []
    URL = 'https://www.basketball-reference.com/boxscores/?month='+ m +'&day=' + d + '&year='+ y
    # URL = 'https://www.basketball-reference.com/boxscores/?month=10&day=26&year=2019'
    print (URL)
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('div',{'class':'game_summaries'})
    for row in table.findAll('div'):
        game = {}
        game['topScorer'] = row.find('table',{'class':'stats'}).tbody.tr.select('td')[1].a.text
        game['topScorerPoints'] = row.find('table',{'class':'stats'}).tbody.tr.select('td')[2].text
        for trow in row.findAll('table', {'class':'teams'}):
            game['loser'] = trow.tbody.find('tr', {'class', 'loser'}).td.a.text
            game['loserScore'] = trow.tbody.find('tr', {'class', 'loser'}).find('td',{'class':'right'}).text
            game['winner'] = trow.tbody.find('tr', {'class', 'winner'}).td.a.text
            game['winnerScore'] = trow.tbody.find('tr', {'class', 'winner'}).find('td',{'class':'right'}).text
            games.append(game)
    return games

def home(request):
    date = datetime.datetime.now()
    players = Playersinfo.objects.all()[:100]
    return render(request, 'home.html', {'players':players, 'date':date})

def boxscore(request):
    date = datetime.datetime.now()
    today_month = str(date.month)
    today_day = str(date.day - 4)
    today_year = str(date.year)
    # games = dailygames(today_month,today_day, today_year)
    #no nba games playing current because of coronavirus. Using dummy data.
    games = dailygames('01','01', '2020')
    return render(request, 'boxscore.html', {'date':date, 'games':games})

def player(request, player_id):
    player = get_object_or_404(Playersinfo, pk = player_id)
    # player = Playersinfo.objects.get(pk = player_id)
    player_id = player_id
    return render(request, 'player.html', {'player_id': player_id, 'player': player})


def PlayerRequestForm(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            playerone_id = form.cleaned_data['player']
            return HttpResponseRedirect('comparisons/'+ str(playerone_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerForm()



def comparison(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            playerone = form.cleaned_data['player']
            playertwo = form.cleaned_data['player_two']
            return HttpResponseRedirect('comparisons/'+ str(playerone)+'&'+ str(playertwo), {'playerone_id': playerone, 'playertwo_id': playertwo})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerForm()

    return render(request, 'comparison.html', {'form': form})

def currentSeasonStats(player):
    player = get_object_or_404(Playersinfo, name = player)
    p_url = 'https://www.basketball-reference.com' + player.url
    page = requests.get(p_url)
    tree = html.fromstring(page.content)
    player_obj = {
        "Points": tree.xpath('//h4[@data-tip="Points"]/parent::div/p[1]/text()')[0],
        "Rebounds": tree.xpath('//h4[text()="TRB"]/../p[1]/text()')[0],
        "Assists": tree.xpath('//h4[text()="AST"]/../p[1]/text()')[0],
        "Field Goal": tree.xpath('//h4[text()="FG%"]/../p[1]/text()')[0],
        "3pt Field Goal": tree.xpath('//h4[text()="FG3%"]/../p[1]/text()')[0],
        "Free Throw": tree.xpath('//h4[text()="FT%"]/../p[1]/text()')[0]
    }
    return player_obj

def careerStats(player):
    player = get_object_or_404(Playersinfo, name = player)
    p_url = 'https://www.basketball-reference.com' + player.url
    page = requests.get(p_url)
    tree = html.fromstring(page.content)
    player_career ={
        "Points": tree.xpath('//h4[@data-tip="Points"]/parent::div/p[2]/text()')[0],
        "Rebounds": tree.xpath('//h4[text()="TRB"]/../p[2]/text()')[0],
        "Assists": tree.xpath('//h4[text()="AST"]/../p[2]/text()')[0],
        "Field Goal": tree.xpath('//h4[text()="FG%"]/../p[2]/text()')[0],
        "3pt field goal": tree.xpath('//h4[text()="FG3%"]/../p[2]/text()')[0],
        "Free Throw": tree.xpath('//h4[text()="FT%"]/../p[2]/text()')[0],
        "Nicknames": tree.xpath('//div[@itemtype="https://schema.org/Person"]/p[2]/text()')[0]
    }
    return player_career

def comparisons(request, playerone_name, playertwo_name):
    print(playerone_name)
    print(playertwo_name)
    player = get_object_or_404(Playersinfo, name = playerone_name)
    player_two = get_object_or_404(Playersinfo, name = playertwo_name)

    p1_current = currentSeasonStats(playerone_name)
    p2_current = currentSeasonStats(playertwo_name)
    p1_careerstats = careerStats(playerone_name)
    p2_careerstats = careerStats(playertwo_name)
    form = PlayerForm(request.POST, initial={'player': player.name})
    PlayerRequestForm(request)

    return render(request, 'comparisons.html', {'player':player, 'playertwo': player_two, 'p1_current': p1_current, 'p2_current': p2_current, 'p1_careerstats': p1_careerstats, 'p2_careerstats': p2_careerstats,'form': form})
