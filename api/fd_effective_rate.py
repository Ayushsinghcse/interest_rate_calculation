from .models import Fdrate, bstat, Ratings, RatingAgencies
from operator import itemgetter
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db.models import Case, When, Value, IntegerField
def convert_into_days(values):
    slab_date = datetime.today()
    num=0
    float_value = False
    number = '0123456789'
    for i in values:
        if i==' ':
            continue
        elif i=='.':
            float_value=True
        if i in number:
            if float_value:
                num = num * (float(i)/10)
            else:
                num = num*10 + int(i)
        elif i=='y' or i=='Y':
            if float_value:
                num = int(num*12)
            slab_date += relativedelta(years=num)
            num=0 
        elif i=='m' or i=='M':
            itr = num//12
            rem = num%12
            for i in range(itr):
                slab_date += relativedelta(months=12)
            slab_date += relativedelta(months=rem)
            num=0
            num=0
        elif i=='d' or i=='D':
            slab_date += relativedelta(days=num)
            num=0
    current_date = datetime.today()

    return (slab_date-current_date).days+1
        

def complete_tenor(tenor):
    """
    Takes a tenor in the format of "XyZd" or "XyZm" or "XyZ" where X is an integer
    and y,Z are characters representing years, months and days respectively.
    Returns a formatted string with the correct spelling
    """
    number = '0123456789'
    float_value = False
    num = float(0)
    tenor_format = ''
    for i in tenor:
        if i==' ':
            # If the character is a space, skip to the next character
            continue
        elif i=='.':
            float_value=True
        elif i in number:
            # If the character is a digit, multiply the previous number by 10 and add the current number
            if float_value:
                num = num + (float(i)/10)
            else:
                num = num*10 + float(i)
        elif i=='d' or i=='D':
            # If the character is 'd', append the number of days to the string and reset the number
            if num%1==0:
                num = int(num)
            tenor_format = tenor_format + str(num) + ' d '
            num = 0

        elif i=='m' or i=='M':
            # If the character is 'm', append the number of months to the string and reset the number
            if num%1==0:
                num = int(num)
            tenor_format = tenor_format + str(num) + ' mo '
            num = 0

        elif i=='y' or i=='Y':
            # If the character is 'y', append the number of years to the string and reset the number
            if num%1==0:
                num = int(num)
            tenor_format = tenor_format + str(num) + ' yr '
            num = 0

    return tenor_format


def user_fdrate_display():
    bstat_object = bstat.objects.all().filter(active=True)
    all_fdrate_objects = {}
    top_fdrate_objects = []
    # print(all_fdrate_objects)
    for i in bstat_object:
        # print(i)
        nbfcs_rating = {}
        fdrate = Fdrate.objects.filter(bref=i.bref).values_list('effstartdate', flat=True)
        length = len(fdrate)-1
        if length<=0:
            continue
        latest_date = datetime.strptime(fdrate[length],'%d-%b-%y')
        lat_date = fdrate[length]
        for date in fdrate: 
            if latest_date < datetime.strptime(date,'%d-%b-%y'):
                latest_date = datetime.strptime(date,'%d-%b-%y')
                lat_date = date
        fdrate = Fdrate.objects.filter(bref=i.bref,effstartdate=lat_date)
        max_val_find = 0
        max_fdrate = 0
        rate_list = []
        for info in fdrate:
            todays_date = datetime.today().strftime('%d-%b-%y')
              
               
                
                
            current_date = datetime.strptime(todays_date,'%d-%b-%y')
            if info.effenddate is not None:
                if current_date > datetime.strptime(info.effenddate,'%d-%b-%y'):
                    continue
            add_dict = {}
            add_dict['bcode']=i.bcode
            add_dict['name']=i.display_name
            add_dict['mobile_name']=i.mobile_display_name
            add_dict['major_flag']=i.major_bank
            add_dict['type']=i.type
            add_dict['url']=i.fd_url
            add_dict['bref']=info.bref
            add_dict['specialrate']=info.specialrate
            add_dict['effdate']=info.effstartdate
            add_dict['effenddate']=info.effenddate
            add_dict['tenorstart']=complete_tenor(info.tenorstart)
            add_dict['tenorend']=complete_tenor(info.tenorend)
            add_dict['tenorstartday']=convert_into_days(info.tenorstart)
            add_dict['tenorendday']=convert_into_days(info.tenorend)
            add_dict['startincl']=info.startincl
            add_dict['endincl']=info.endincl
            add_dict['fdrate']=info.baserate
            add_dict['addsenior']=info.seniorextra+info.baserate
            add_dict['addsupsenior']=info.superextra+add_dict['addsenior']
            add_dict['max_fd_limit'] = i.maximum_fd_limit
            
            if i.type=='NBFC':
                credit_val = Ratings.objects.filter(bref=i.bref).values_list('updatedate',flat=True)
                length = len(credit_val)
                if length<=0:
                    continue
                latest_date = datetime.strptime(credit_val[length-1],'%d-%b-%y')
                lat_date = credit_val[length-1]
                for date in credit_val: 
                    if latest_date < datetime.strptime(date,'%d-%b-%y'):
                        latest_date = datetime.strptime(date,'%d-%b-%y')
                        lat_date = date

                ratings = list(RatingAgencies.objects.all().values_list("Agency", "DisplayPriority"))
                ratings.sort(key=itemgetter(1))
                for rating in ratings:
                    credit = list(Ratings.objects.filter(bref=i.bref,updatedate=lat_date,Agency=rating[0]).values_list("Agency", "Rating", "Outlook"))
                    if len(credit)>0:
                        add_dict['Agency']=credit[0][0]
                        add_dict['Rating']=credit[0][1]
                        add_dict['Outlook']= credit[0][2]
                        nbfcs_rating[f'{i.bref}']=[credit[0][0],credit[0][1], credit[0][2]]
                        break


            rate_list.append(add_dict)
            if info.baserate>fdrate[max_fdrate].baserate:
                max_fdrate = max_val_find
            max_val_find += 1
        
        all_fdrate_objects[i.display_name]=rate_list
        
        top_bank_fd = {}
        top_bank_fd['bcode']=i.bcode
        top_bank_fd['name']=i.display_name
        top_bank_fd['mobile_name']=i.mobile_display_name
        top_bank_fd['type']=i.type
        top_bank_fd['major_flag']=i.major_bank
        top_bank_fd['url']=i.fd_url
        top_bank_fd['bref']=fdrate[max_fdrate].bref
        top_bank_fd['specialrate']=fdrate[max_fdrate].specialrate
        top_bank_fd['effdate']=fdrate[max_fdrate].effstartdate
        top_bank_fd['effenddate']=fdrate[max_fdrate].effenddate
        top_bank_fd['tenorstart']=complete_tenor(fdrate[max_fdrate].tenorstart)
        top_bank_fd['tenorend']=complete_tenor(fdrate[max_fdrate].tenorend)
        top_bank_fd['tenorstartday']=convert_into_days(fdrate[max_fdrate].tenorstart)
        top_bank_fd['tenorendday']=convert_into_days(fdrate[max_fdrate].tenorend)
        top_bank_fd['startincl']=fdrate[max_fdrate].startincl
        top_bank_fd['endincl']=fdrate[max_fdrate].endincl
        top_bank_fd['fdrate']=fdrate[max_fdrate].baserate
        top_bank_fd['addsenior']=fdrate[max_fdrate].seniorextra+fdrate[max_fdrate].baserate
        top_bank_fd['addsupsenior']=fdrate[max_fdrate].superextra+top_bank_fd['addsenior']
        top_bank_fd['max_fd_limit'] = i.maximum_fd_limit
        if i.type=='NBFC':
            top_bank_fd['Agency']=nbfcs_rating[f'{i.bref}'][0]
            top_bank_fd['Rating']=nbfcs_rating[f'{i.bref}'][1]
            top_bank_fd['Outlook']=nbfcs_rating[f'{i.bref}'][2]


        top_fdrate_objects.append(top_bank_fd)
    return_dict = {}
    top_fdrate_objects.sort(key=itemgetter('fdrate'), reverse=True)
    # print(len(top_bank_fd))
    # print(len(all_fdrate_objects))
    return_dict['top_fd'] = top_fdrate_objects
    return_dict['all_fd'] = all_fdrate_objects
    return return_dict

    

# user_fdrate_display()

def all_banks_fd():
    bstat_object = bstat.objects.all().filter(active=True)
    all_fdrate_objects = []
    # print(all_fdrate_objects)
    for i in bstat_object:
        # print(i)
        fdrate = Fdrate.objects.filter(bref=i.bref).values_list('effstartdate', flat=True)
        length = len(fdrate)-1
        if length<=0:
            continue
        latest_date = datetime.strptime(fdrate[length],'%d-%b-%y')
        lat_date = fdrate[length]
        for date in fdrate: 
            if latest_date < datetime.strptime(date,'%d-%b-%y'):
                latest_date = datetime.strptime(date,'%d-%b-%y')
                lat_date = date
        fdrate_object = Fdrate.objects.filter(bref=i.bref,effstartdate=lat_date)
        for info in fdrate_object:
            add_dict = {}
            add_dict['bcode']=i.bcode
            add_dict['name']=i.display_name
            add_dict['mobile_name']=i.mobile_display_name
            add_dict['type']=i.type
            add_dict['url']=i.fd_url
            add_dict['bref']=info.bref
            add_dict['specialrate']=info.specialrate
            add_dict['effdate']=info.effstartdate
            add_dict['effenddate']=info.effenddate
            add_dict['tenorstart']=complete_tenor(info.tenorstart)
            add_dict['tenorend']=complete_tenor(info.tenorend)
            add_dict['tenorstartday']=convert_into_days(info.tenorstart)
            add_dict['tenorendday']=convert_into_days(info.tenorend)
            add_dict['startincl']=info.startincl
            add_dict['endincl']=info.endincl
            add_dict['fdrate']=info.baserate
            add_dict['addsenior']=info.seniorextra+info.baserate
            add_dict['addsupsenior']=info.superextra+add_dict['addsenior']
            if i.type=='NBFC':
                credit_val = Ratings.objects.filter(bref=i.bref).values_list('updatedate',flat=True)
                length = len(credit_val)-1
                if length<=0:
                    continue
                latest_date = datetime.strptime(credit_val[length],'%d-%b-%y')
                lat_date = credit_val[length]
                for date in credit_val: 
                    if latest_date < datetime.strptime(date,'%d-%b-%y'):
                        latest_date = datetime.strptime(date,'%d-%b-%y')
                        lat_date = date

                
                credit = Ratings.objects.filter(bref=i.bref,updatedate=lat_date)
                counter = 1
                for cr in credit:
                    add_dict[f'Agency{counter}']=cr.Agency
                    add_dict[f"Rating{counter}"]=cr.Rating
                    add_dict[f"Outlook{counter}"]=cr.Outlook
                    counter+=1
            all_fdrate_objects.append(add_dict)
    return all_fdrate_objects