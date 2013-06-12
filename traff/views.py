# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.core.management import call_command


from StringIO import StringIO
from subprocess import Popen,PIPE
import sys
import datetime,calendar
from time import strftime, localtime
from calendar import monthrange,month_name


from traff.models import Day,DayTime

def index(request):
    day_list = Day.objects.all()
    template = loader.get_template('index.html')

    context = Context({"day_list" : day_list,})

    year=datetime.date.today().year
    month=datetime.date.today().month
    monthName=calendar.month_name[month]
    monthList=[]
    for i in range(1,13):
        monthList.append(calendar.month_name[i])

    dayOfMonth=[]
    traffOfDay=[]
    

    def fillDataList():
        dayOfMonth.append(d)
        traffOfDay.insert(d,(round(float(day.dayTraffic)/(1024*1024*1024),2)))

    for day in day_list:
        d=day.date.day
        m=day.date.month
        
        if 'month' in request.GET:
            if(calendar.month_name[m] == request.GET['month']):
                fillDataList()
                monthName=calendar.month_name[m]
                lastDate=day
        elif calendar.month_name[m] == monthName:
            fillDataList()
            lastDate=day
    dayOfMonth.sort(key=int)


    context['dayOfMonth'] = dayOfMonth
    context['monthName'] = monthName
    context['monthList'] = monthList
    context['traffOfDay'] = traffOfDay
    

    timeInterval=[]
    timeValue=[]
    def findTimeToDay():
        for day in day_list:
            if day.date == newDate:
                break
                
        daytime_list = DayTime.objects.filter(day=day.id)
        traffic=0
        for time in daytime_list:
            
            if time.time.hour not in timeInterval:
                timeInterval.append(time.time.hour)
                timeValue.append(traffic)
                traffic=0
            else:
                traffic += (round(float(time.traff)/(1024*1024),2)) 
        


    daylyView = 0
    if 'daylyView' in request.GET:
        requestDay = request.GET['daylyView']
        if(day!=""):
            daylyView = 1
            newDate = lastDate.date.replace(day=int(float(requestDay)))
            findTimeToDay()
            
    
    context['daylyView'] = daylyView
    context['timeInterval'] = timeInterval
    context['timeValue'] = timeValue


    return HttpResponse(template.render(context))



def cuptureTraffic(request):
    usage=[]
    try:
        ipt = Popen("iptables -L OUTPUT -vnx".split(' '),stdout=PIPE)
        grep = Popen("grep 130.83.177.137".split(' '),stdout=PIPE,stdin=ipt.stdout)
        ipt.stdout.close()
        #usage = grep.communicate()[0]
        #ipt.wait()
        usage =  grep.stdout.readline().split(' ')

        while True:
            try:
                usage.remove("")
            except ValueError:
                break
        print usage[1]

        resetIPt = Popen("iptables -Z OUTPUT".split())

        # check if day already in the database
        dayList = Day.objects.all()
        d = Day(dayID=0,date=datetime.date.today(),dayTraffic=0)
        flag=0
        for day in dayList:
            if day.date == d.date:
                d = day
                currentTraff = d.dayTraffic
                d.dayTraffic = currentTraff+int(float(usage[1]))
                d.save()
                flag=1
        if flag == 0:
            #print "Usage: %s" % (usage[1])
            d.dayTraffic=int(float(usage[1]))
            d.save()


        # add traffic with timestamp
        if len(usage) > 1:
            traffic=usage[1]
            cTime = strftime('%H:%M:%S', localtime())
            DayTime(day=d,time=cTime,traff=usage[1]).save()
        else:
            print "Error while compute Traffic from IPTABLES"

    except OSError:
        print "Error"



    return HttpResponse("cuptureTraffic")




def createDummyDB(request):
    # for i in range(1,30,2):
    #     d = Day(dayID=0,date=datetime.date(2013, 07, i),dayTraffic=2*i)
    #     d.save()
    # for i in range(2,30,2):
    #     d = Day(dayID=0,date=datetime.date(2013, 9, i),dayTraffic=2*i)
    #     d.save()
    return HttpResponse("dummy")


