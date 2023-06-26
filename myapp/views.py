from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from myapp.models import Playersinfo, Debate, DebateStatus
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import datetime
import re
import requests
from bs4 import BeautifulSoup
from lxml import html
from .forms import PlayerForm, DebateStatusBar
from .debates import DebateForm

# Create your views here.

# Scraping Daily Games to show score
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
        # game['topScorer'] = row.find('table',{'class':'stats'}).tbody.tr.select('td')[1].a.text
        # game['topScorerPoints'] = row.find('table',{'class':'stats'}).tbody.tr.select('td')[2].text
        for trow in row.findAll('table', {'class':'teams'}):
            game['loser'] = trow.tbody.find('tr', {'class', 'loser'}).td.a.text
            game['loserScore'] = trow.tbody.find('tr', {'class', 'loser'}).find('td',{'class':'right'}).text
            game['winner'] = trow.tbody.find('tr', {'class', 'winner'}).td.a.text
            game['winnerScore'] = trow.tbody.find('tr', {'class', 'winner'}).find('td',{'class':'right'}).text
            games.append(game)
    return games

def boxscore(request):
    date = datetime.datetime.now()
    today_month = str(date.month)
    today_day = str(date.day-1)
    today_year = str(date.year)
    print(today_year)
    games = dailygames(today_month,today_day,today_year)
    #no nba games playing current because of coronavirus. Using dummy data.
    # games = dailygames('1','15','2021')
    return render(request, 'boxscore.html', {'date':date, 'games':games})

# --------------------------------------------


def home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        agree_percents = []
        #displaying statuses and debate charts not including the current_user
        all_status = DebateStatus.objects.exclude(user_id=user_id)
        all_debates = Debate.objects.all().exclude(user_id=user_id)
        for s in all_status:
            if s.opinion_total != 0:
                agree_percents.append(round(100*(s.agree/s.opinion_total)))
            else:
                agree_percents.append(0)

    else:
        all_status = DebateStatus.objects.all()
        all_debates = Debate.objects.all()
        agree_percents =[]

    return render(request, 'home.html', {"all_status": all_status, "all_debates":all_debates, "agree_percents": agree_percents})

def index(request, letter):
    # Letters user can click on to filter through players by last name
    alphabet =[]
    for i in range(ord('A'), ord('Z')+1):
        alphabet.append(chr(i))
    #finds players last name by the letter the user clicks on
    players = Playersinfo.objects.filter(name__startswith=letter)
    return render(request, 'index.html', {'players':players, 'alphabet':alphabet})



def player(request, player_id):
    player = get_object_or_404(Playersinfo, pk = player_id)
    # player = Playersinfo.objects.get(pk = player_id)
    player_id = player_id
    return render(request, 'player.html', {'player_id': player_id, 'player': player})




# def PlayerRequestForm(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = PlayerForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             playerone_id = form.cleaned_data['player']
#             return HttpResponseRedirect('comparisons/'+ str(playerone_id))
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = PlayerForm()






def scrapeComment(xp, regex, tree):
    elm = tree.xpath(xp)
    soup = BeautifulSoup(str(elm[0]), "lxml")
    final_elm = re.findall(regex, str(soup))
    if final_elm:
        return final_elm
    else:
        return " "


def validatescrape(elm):
    if elm:
        return elm[1]
    else:
        return ""


def currentSeasonStats(player):
    player = get_object_or_404(Playersinfo, name = player)
    print("Hey Player obj is here")
    print(player.url)
    p_url = 'https://www.basketball-reference.com' + player.url
    page = requests.get(p_url)
    tree = html.fromstring(page.content)
    birth_date = player.birthdate
    birth_year = re.search('(?<=, )[\d].+', birth_date)
    # current_year = int(datetime.now().year)
    age = 2021 - int(birth_year.group(0))

    print(tree)

    player_obj = {}
    if age < 41:
        salary = tree.xpath('//div[contains(@id, "all_contracts")]/comment()[1]')
        # soup = BeautifulSoup(str(salary[0]), "lxml")
        # current_salary = scrapeComment('//div[contains(@id, "all_contracts")]/comment()[1]', '(?<=\<span class=\"salary\-pl\">\$)[\d.,]+', tree)

        player_obj = {
            # "Points": tree.xpath('//h4[@data-tip="Points"]/parent::div/p[1]/text()')[0],
            "Points": tree.xpath('//span[@data-tip="Points"]/parent::div/p[1]/text()')[0],
            "Rebounds": tree.xpath('//strong[text()="TRB"]/ancestor::div/p[1]/text()')[0],
            "Assists": tree.xpath('//strong[text()="AST"]/ancestor::div/p[1]/text()')[0],
            "Block": tree.xpath('//tr[@id="per_game.2021"]/td[@data-stat="blk_per_g"]/text()')[0],
            "Steals": tree.xpath('//tr[@id="per_game.2021"]/td[@data-stat="stl_per_g"]/text()')[0],
            "Field Goal": tree.xpath('//strong[text()="FG%"]/ancestor::div/p[1]/text()')[0],
            "3pt Field Goal": tree.xpath('//strong[text()="FG3%"]/ancestor::div/p[1]/text()')[0],
            "Free Throw": tree.xpath('//strong[text()="FT%"]/ancestor::div/p[1]/text()')[0],
            # "Current Salary": "$" + current_salary[0],
        }
        print("this");
        print(salary);
    print(player_obj);
    return player_obj


def careerStats(player):
    player = get_object_or_404(Playersinfo, name = player)
    p_url = 'https://www.basketball-reference.com' + player.url
    page = requests.get(p_url)
    tree = html.fromstring(page.content)
    print(tree)
    # career_salary = scrapeComment('//div[contains(@id, "all_all_salaries")]/comment()[1]', '(?<=\" data-stat=\"salary\" >\$)[\d,.]+',tree)
    exp_str = tree.xpath('//strong[contains(text(),"Experience:")]/../text()')

    player_career ={
        "Points": tree.xpath('//span[@data-tip="Points"]/parent::div/p[2]/text()')[0],
        "Rebounds": tree.xpath('//strong[text()="TRB"]/ancestor::div/p[2]/text()')[0],
        "Assists": tree.xpath('//strong[text()="AST"]/ancestor::div/p[2]/text()')[0],
        "Block": tree.xpath('//tr[@id="per_game.2021"]/td[@data-stat="blk_per_g"]/text()')[0],
        "Steals": tree.xpath('//tr[@id="per_game.2021"]/td[@data-stat="stl_per_g"]/text()')[0],
        "Field Goal": tree.xpath('//strong[text()="FG%"]/ancestor::div/p[2]/text()')[0],
        "3pt Field Goal": tree.xpath('//strong[text()="FG3%"]/ancestor::div/p[2]/text()')[0],
        "Free Throw": tree.xpath('//strong[text()="FT%"]/ancestor::div/p[2]/text()')[0],
        # "Nicknames": tree.xpath('//div[@itemtype="https://schema.org/Person"]/p[2]/text()')[0],
        # "Career Salary": "$" + career_salary[0],
        "Experience": validatescrape(exp_str)
    }
    # print(exp_str[1])
    return player_career

def playerAccolades(player):
    accolades = []
    player = get_object_or_404(Playersinfo, name = player)
    p_url = 'https://www.basketball-reference.com' + player.url
    page = requests.get(p_url)
    tree = html.fromstring(page.content)
    accolades = tree.xpath('//ul[@id="bling"]/li/a/text()')
    if len(accolades) > 0:
        return accolades
    else:
        return []


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

            try:
                player = Playersinfo.objects.get(name=playerone)
                player_two = Playersinfo.objects.get(name=playertwo)
                return HttpResponseRedirect('comparisons/'+ str(playerone)+'&'+ str(playertwo), {'playerone_id': playerone, 'playertwo_id': playertwo})
            except Playersinfo.DoesNotExist:
                error = "The Players you are looking for can not be found. Please try again"
                return render(request, 'comparison.html', {'form': form, 'error': error})
                # raise Http404("Player does not exist")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlayerForm()

    return render(request, 'comparison.html', {'form': form})


def comparisons(request, playerone_name, playertwo_name):
    print(playerone_name)
    print(playertwo_name)

    #getting player objects and returning a 404 error page
    # player = get_object_or_404(Playersinfo, name = playerone_name)
    # player_two = get_object_or_404(Playersinfo, name = playertwo_name)

    try:
        player = Playersinfo.objects.get(name=playerone_name)
        player_two = Playersinfo.objects.get(name=playertwo_name)
    except Playersinfo.DoesNotExist:
        return HttpResponseRedirect('/comparison')
        raise Http404("Player does not exist")
    
    try:
        p1_current = currentSeasonStats(playerone_name)
        p2_current = currentSeasonStats(playertwo_name)
    except:
        p1_current = "N/A"
        p2_current = "N/A"
    
    try:
        p1_careerstats = careerStats(playerone_name)
        p2_careerstats = careerStats(playertwo_name)
    except:
        p1_careerstats = "N/A"
        p2_careerstats = "N/A"
    p1_accolades = playerAccolades(playerone_name)
    p2_accolades = playerAccolades(playertwo_name)
    form = PlayerForm()

    years = []
    current_year = datetime.date.today().year
    print(current_year)

    for year in range(2000,int(current_year)+1):
        years.append(year)
    print(years)

    # for year in range(1970,2019):
    #     years.append(year)
    # print(years)

    return render(request, 'comparisons.html', {'player':player, 'playertwo': player_two, 'p1_current': p1_current, 'p2_current': p2_current, 'p1_careerstats': p1_careerstats, 'p2_careerstats': p2_careerstats, 'p1_accolades': p1_accolades, 'p2_accolades': p2_accolades, 'years':years, 'form': form})


def createDebate(request):
    if request.method == "POST":
        print('vote sent')
        user_id = request.POST['user']
        if user_id == 'None':
            return HttpResponseRedirect('/accounts/login')
        else:
            user = User.objects.get(id=user_id)
            debate = Debate()
            debate.user = user
            debate.p1_id = request.POST['p1_id']
            debate.p2_id = request.POST['p2_id']
            debate.p1_name = request.POST['p1_name']
            debate.p2_name = request.POST['p2_name']
            debate.p1_vote = 0
            debate.p2_vote = 0
            debate.p1_user_id = request.POST['p1_user_id']
            debate.p2_user_id = request.POST['p2_user_id']
            debate.user_pick = request.POST['user_pick']

            if debate.user_pick == '1':
                debate.p1_vote += 1
            else:
                debate.p2_vote+=1

            debate.save()

            return HttpResponseRedirect('accounts/profile')
    else:
        return HttpResponseRedirect('accounts/profile')

def deleteDebate(request):
    if request.method == "POST":
        id = request.POST['debate_id']
        debate = Debate.objects.get(id=id)
        debate.delete()
        print('Debate Deleted')
        return HttpResponseRedirect('accounts/profile')


def submitStatus(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        ds = DebateStatus()
        ds.status = request.POST['status']
        if request.POST['open_debate']== "True":
            ds.open_debate = True
        else:
            ds.open_debate = False
        ds.user = User.objects.get(id=user_id)
        ds.save()
        return HttpResponseRedirect('accounts/profile')


def statusCount(request, status_id, approval):
    if approval == "agree":
        status = DebateStatus.objects.get(id=status_id)
        status.agree += 1
        status.opinion_total += 1
        status.save()
        print("agree added")
        return HttpResponseRedirect('/')
    elif approval == "disagree":
        status = DebateStatus.objects.get(id=status_id)
        status.disagree += 1
        status.opinion_total += 1
        status.save()
        print("disagree added")
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('accounts/profile')


def advanceStats(request, playername, year):

    print(playername, year)
    return render(request, 'advanceStats.html')
