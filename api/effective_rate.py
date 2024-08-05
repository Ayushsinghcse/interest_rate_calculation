from .models import bstat, Sdrate
from operator import itemgetter

def effective_rate_calc_diff(entering_amount, slabs_list, roi_list):
    total_interest = 0
    i = 0
    current_amount = entering_amount
    first_rate_value = roi_list[0]
    # print(slabs_list, roi_list)
    while(float(slabs_list[i])<=entering_amount):
        i+=1 
        if slabs_list[i]=='$':
            break
    # print(slabs_list[i], roi_list[i])
    total_interest += first_rate_value*float(slabs_list[0])
    current_amount-=float(slabs_list[0])
    # print(total_interest, current_amount)
    total_interest += current_amount*roi_list[i]
    # print(total_interest)
    effective_rate = total_interest/entering_amount
    val = "{:.3f}".format(round(effective_rate, 2))
    return val


def effective_rate_calc_federal(entering_amount, slabs_list, roi_list):
    SBI_RATE = 6.50
    no_slabs = len(slabs_list)
    actual_amount = entering_amount
    i=0
    total_interest = 0
    while(entering_amount>0 or i<no_slabs):
        slabs_value = slabs_list[i]
        # print(slabs_value)
        if not slabs_value or slabs_value=='' or slabs_value is None or slabs_value==' ':
            return -1
        if slabs_value=="xxx" or slabs_value=="xx" or slabs_value=="XXXX":
            return -1
            break
        if(slabs_value=='$'):
            # print(slabs_value, roi_list[i])
            amount_interest = entering_amount*(SBI_RATE-roi_list[i])
            total_interest += amount_interest 
            entering_amount =0 
            break

        if(entering_amount>float(slabs_value)):
            last_slab_value=0
            if(i!=0):
                last_slab_value = slabs_list[i-1]

            #excess amount edge case:
            amount_for_the_current_slab = float(slabs_value)-float(last_slab_value)
            # print(slabs_value, roi_list[i])
            calcultated_amount_interest = amount_for_the_current_slab*(SBI_RATE-roi_list[i])
            total_interest += calcultated_amount_interest
            entering_amount -= amount_for_the_current_slab
        else:
            total_interest += entering_amount*(SBI_RATE-roi_list[i])
            entering_amount=0
            break 
        i+=1
        # print(entering_amount)
        # print(total_interest)
    effective_rate = total_interest/actual_amount
    val = "{:.3f}".format(round(effective_rate, 2))
    return val




def effectiveRate_calculation(entering_amount, slabs_list, roi_list):
    no_slabs = len(slabs_list)
    actual_amount = entering_amount
    i=0
    total_interest = 0
    while(entering_amount>0 or i<no_slabs):
        slabs_value = slabs_list[i]
        # print(slabs_value)

        if not slabs_value or slabs_value=='' or slabs_value is None or slabs_value==' ':
            return -1

        if slabs_value=="x":
            return -1
            break
        if(slabs_value=='$'):
            # print(slabs_value, roi_list[i])
            amount_interest = entering_amount*roi_list[i]
            total_interest += amount_interest 
            entering_amount =0 
            break

        if(entering_amount>float(slabs_value)):
            last_slab_value=0
            if(i!=0):
                last_slab_value = slabs_list[i-1]

            #excess amount edge case:
            amount_for_the_current_slab = float(slabs_value)-float(last_slab_value)
            # print(slabs_value, roi_list[i])
            calcultated_amount_interest = amount_for_the_current_slab*roi_list[i]
            total_interest += calcultated_amount_interest
            entering_amount -= amount_for_the_current_slab
        else:
            total_interest += entering_amount*roi_list[i]
            entering_amount=0
            break 
        i+=1
        # print(entering_amount)
        # print(total_interest)
    effective_rate = total_interest/actual_amount
    val = "{:.3f}".format(round(effective_rate, 2))
    return val


def user_amount_display(amount=100000):
    bank_effective_rate = []

    bstat_objects = bstat.objects.all().filter(active=True)
    for i in bstat_objects:
        sdrates_objects = Sdrate.objects.filter(bcode=i.bcode)
        latest_val = len(sdrates_objects)-1
        if latest_val<0:
            continue
        bank_dict = {}
        # print(sdrates_objects[latest_val].s1)
        slab_list, rate_list = [], []
        s1 , r1 = sdrates_objects[latest_val].s1, sdrates_objects[latest_val].r1
        s2 , r2 = sdrates_objects[latest_val].s2, sdrates_objects[latest_val].r2
        s3 , r3 = sdrates_objects[latest_val].s3, sdrates_objects[latest_val].r3
        s4 , r4 = sdrates_objects[latest_val].s4, sdrates_objects[latest_val].r4
        s5 , r5 = sdrates_objects[latest_val].s5, sdrates_objects[latest_val].r5
        s6 , r6 = sdrates_objects[latest_val].s6, sdrates_objects[latest_val].r6
        s7 , r7 = sdrates_objects[latest_val].s7, sdrates_objects[latest_val].r7
        s8 , r8 = sdrates_objects[latest_val].s8, sdrates_objects[latest_val].r8
        s9 , r9 = sdrates_objects[latest_val].s9, sdrates_objects[latest_val].r9
        s10 , r10 = sdrates_objects[latest_val].s10, sdrates_objects[latest_val].r10
        s11 , r11 = sdrates_objects[latest_val].s11, sdrates_objects[latest_val].r11
        s12 , r12 = sdrates_objects[latest_val].s12, sdrates_objects[latest_val].r12
        s13 , r13 = sdrates_objects[latest_val].s13, sdrates_objects[latest_val].r13
        s14 , r14 = sdrates_objects[latest_val].s14, sdrates_objects[latest_val].r14
        s15 , r15 = sdrates_objects[latest_val].s15, sdrates_objects[latest_val].r15
        slab_list.append(s1), rate_list.append(r1)
        slab_list.append(s2), rate_list.append(r2)
        slab_list.append(s3), rate_list.append(r3)
        slab_list.append(s4), rate_list.append(r4)
        slab_list.append(s5), rate_list.append(r5)
        slab_list.append(s6), rate_list.append(r6)
        slab_list.append(s7), rate_list.append(r7)
        slab_list.append(s8), rate_list.append(r8)
        slab_list.append(s9), rate_list.append(r9)
        slab_list.append(s10), rate_list.append(r10)
        slab_list.append(s11), rate_list.append(r11)
        slab_list.append(s12), rate_list.append(r12)
        slab_list.append(s13), rate_list.append(r13)
        slab_list.append(s14), rate_list.append(r14)
        slab_list.append(s15), rate_list.append(r15)
        # print(slab_list, rate_list)
        # if i.name=="CSB Bank":
        effective_rate_value = 0
        # if i.name=="Federal Bank":
        #     effective_rate_value = effective_rate_calc_federal(amount, slab_list, rate_list)
        if((i.name=='CSB Bank' and amount>250000000) or i.name=='RBL Bank'):
            effective_rate_value = effective_rate_calc_diff(amount, slab_list, rate_list)
        elif i.active!=True:
            effective_rate_value=-1
        else:
            effective_rate_value = effectiveRate_calculation(amount, slab_list, rate_list)
        if effective_rate_value!=-1:
            bank_dict['name'] = i.display_name
            bank_dict['mobile_name'] = i.mobile_display_name
            bank_dict['type'] = i.type 
            bank_dict['bank_url'] = i.sd_url
            bank_dict['bank_id'] = i.bcode
            bank_dict['major_bank'] = i.major_bank
            bank_dict['effective_rate'] = effective_rate_value
            bank_dict['interest_payout'] = i.payout_freq
            bank_effective_rate.append(bank_dict)

    # highest_effective_rate_banks = sorted(bank_effective_rate, key=itemgetter('effective_rate'), reverse=True)
    bank_effective_rate.sort(key=itemgetter('effective_rate'), reverse=True)

    # for key, values in highest_effective_rate_banks.items():
    #     rate = values/100
    #     interest = amount*rate
    #     print(key, values, interest)
    return bank_effective_rate


def all_banks_sd():
    all_banks_data = {}
    bstat_object = bstat.objects.all().filter(active=True)
    for i in bstat_object:
        bank_rates = {}
        sdrate_obj = Sdrate.objects.filter(bref=i.bref)
        latest_val = len(sdrate_obj)-1
        if latest_val<0:
            continue

        bank_rates['name'] = i.display_name
        bank_rates['mobile_name'] = i.mobile_display_name
        bank_rates['bref'] =sdrate_obj[latest_val].bref
        bank_rates['bcode']=sdrate_obj[latest_val].bcode
        bank_rates['effdate']=sdrate_obj[latest_val].effdate
        bank_rates['url'] = i.sd_url
        ratings = []
        ratings1,ratings2,ratings3,ratings4,ratings5,ratings6,ratings7,ratings8 = {},{},{},{},{},{},{},{}
        ratings1['amount']=(sdrate_obj[latest_val].s1)
        ratings1['ratings']=(sdrate_obj[latest_val].r1)
        ratings2['amount']=(sdrate_obj[latest_val].s2)
        ratings2['ratings']=(sdrate_obj[latest_val].r2)
        ratings3['amount']=(sdrate_obj[latest_val].s3)
        ratings3['ratings']=(sdrate_obj[latest_val].r3)
        ratings4['amount']=(sdrate_obj[latest_val].s4)
        ratings4['ratings']=(sdrate_obj[latest_val].r4)
        ratings5['amount']=(sdrate_obj[latest_val].s5)
        ratings5['ratings']=(sdrate_obj[latest_val].r5)
        ratings6['amount']=(sdrate_obj[latest_val].s6)
        ratings6['ratings']=(sdrate_obj[latest_val].r6)
        ratings7['amount']=(sdrate_obj[latest_val].s7)
        ratings7['ratings']=(sdrate_obj[latest_val].r7)
        ratings8['amount']=(sdrate_obj[latest_val].s8)
        ratings8['ratings']=(sdrate_obj[latest_val].r8)
        ratings.append(ratings1)
        ratings.append(ratings2)
        ratings.append(ratings3)
        ratings.append(ratings4)
        ratings.append(ratings5)
        ratings.append(ratings6)
        ratings.append(ratings7)
        ratings.append(ratings8)
        ratings9,ratings10,ratings11,ratings12,ratings13,ratings14,ratings15 = {},{},{},{},{},{},{}

        ratings9['amount']=(sdrate_obj[latest_val].s9)
        ratings9['ratings']=(sdrate_obj[latest_val].r9)
        ratings10['amount']=(sdrate_obj[latest_val].s10)
        ratings10['ratings']=(sdrate_obj[latest_val].r10)
        ratings11['amount']=(sdrate_obj[latest_val].s11)
        ratings11['ratings']=(sdrate_obj[latest_val].r11)
        ratings12['amount']=(sdrate_obj[latest_val].s12)
        ratings12['ratings']=(sdrate_obj[latest_val].r12)
        ratings13['amount']=(sdrate_obj[latest_val].s13)
        ratings13['ratings']=(sdrate_obj[latest_val].r13)
        ratings14['amount']=(sdrate_obj[latest_val].s14)
        ratings14['ratings']=(sdrate_obj[latest_val].r14)
        ratings15['amount']=(sdrate_obj[latest_val].s15)
        ratings15['ratings']=(sdrate_obj[latest_val].r15)
        ratings.append(ratings9)
        ratings.append(ratings10)
        ratings.append(ratings11)
        ratings.append(ratings12)
        ratings.append(ratings13)
        ratings.append(ratings14)
        ratings.append(ratings15)
        bank_rates['ratings'] = ratings
        all_banks_data[i.display_name] = bank_rates

    return all_banks_data