from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
# from django.contrib.admin.widgets import AdminDateWidget
# Create your models here.
# auto_increament function is used to generate a new id
# for the Sdrate model object. This function takes no arguments
# and returns an integer
def auto_increament() -> int:
    """
    This function generates a new id for the Sdrate model object.
    It takes no arguments and returns an integer.
    """
    sdrates_obj = Sdrate.objects.all()  # all Sdrate objects
    length = len(sdrates_obj)  # length of the Sdrate objects list
    val = sdrates_obj[length-1].rateid + 1  # new id is the last id + 1
    return val


def fdrate_inc() -> int:  


    fdrate_obj = Fdrate.objects.all()
    length = len(fdrate_obj)
    if length==0:
        return 0
    val = fdrate_obj[length-1].fdrate_id + 1
    return val


def id_inc() -> int:
    """
    This function returns the next id for the Sdrate model object.
    It takes no arguments and returns an integer.

    It gets all the Sdrate objects and their length.
    The new id is the last id + 1.
    """
    sdrate = Sdrate.objects.all()  # all Sdrate objects
    length = len(sdrate)  # length of the Sdrate objects list
    val = length + 1  # new id is the last id + 1
    return val

def id_inc1() -> int:

    sdrate = bstat.objects.all()  # all Sdrate objects
    length = len(sdrate)  # length of the Sdrate objects list
    val = length + 1  # new id is the last id + 1
    return val

def id_inc2() -> int:
    fdrate = Fdrate.objects.all()
    length = len(fdrate)
    val = length+1
    return val
def auto_fill_slab(value):
    """
    This function takes a slab value as input,
    and returns the value in numeric format.

    If the last character of the input is a letter,
    it is used to determine the multiplier to convert
    the value to numeric format.
    """
    if value:
        last_val = value[-1].lower()  # last character of the input


        if last_val.isalpha():  # if last character is a letter
            val = float(value[:-1])  # remove the last char from input

            if last_val == 'k':  # if letter is k
                val *= 1000.0  # multiply the value by 1000
            elif last_val == 'l':  # if letter is l
                val *= 100000.0  # multiply the value by 100000
            else:  # if letter is c
                val *= 10000000.0  # multiply the value by 10000000

            amount = "{:.1f}".format(val)  # convert to string with precision 1
            return amount  # return the amount

        return value  # return the original value if no conversion is required

def validate_slabs(value):
    """
    This function validates the slab values entered by the user.
    It takes the slab value as input and raises a ValidationError if the input is not valid.
    """
    if value=='xx' or value=='xxx' or value=='XXXX' or value=='$':
        return value
    num = value[:-1]
    flag = True
    dotcnt=0
    for i in num:
        # If the character is a dot and we have not encountered a dot before
        if i=='.' and dotcnt==0:
            # Increment the dot count
            dotcnt+=1
            # Continue with the next iteration of the loop
            continue
        # Try to convert the character to an integer  
         
          
           
           
        try:
            int(i)
        # If the character is not an integer
        except ValueError:
            # Set the flag to False
            flag=False
    # If the flag is False, it means that the input contains an invalid character
    if not flag:
        # Raise a ValidationError
        raise ValidationError("enter the valid amount")
    # If the flag is True, it means that the input is valid
    if flag:
        last_val = value[-1].lower()
        # print(last_val)
    # If the last character is not "#", continue with the validation
    if last_val!="#":
        # If the last character is k, l or c, return the value
        if last_val=='k' or last_val=='l' or last_val=='c':
            return value
        # If the last character is not a letter, return the value
        elif not last_val.isalpha():
            return value
        # If the last character is not k, l or c, raise a ValidationError
        else:
            raise ValidationError("please only enter letter k, l or c")


def validate_tenor(value):
    if value=='' or value==' ' or value=='0':
        raise ValidationError("please enter valid tenor")
    print(value)
    wrong_format, timecnt =True,0
    for i in value:
        if i==" ":
            continue
        validate_value, validate_time = "0123456789","dmyDMY"
        if i not in validate_value and i not in validate_time:
            wrong_format=False
            break
        if i in validate_time:
            timecnt+=1
    if wrong_format and timecnt>0:
        return value
    else:
        raise ValidationError("please enter tenor in days, months or years only")


class Sdrate(models.Model):
    your_ref_choices = (
    ("Bank of Baroda","Bank of Baroda"),('Bank of India',"Bank of India"),('Bank of Maharashtra',"Bank of Maharashtra"),('Canara Bank',"Canara Bank"),('Central Bank of India',"Central Bank of India"),('Indian Bank',"Indian Bank"),
    ('Indian Overseas Bank',"Indian Overseas Bank"),('Punjab and Sind Bank',"Punjab and Sind Bank"),('Punjab National Bank',"Punjab National Bank"),('State Bank of India',"State Bank of India"),('UCO Bank',"UCO Bank"),
    ('Union Bank of India',"Union Bank of India"),('Axis Bank',"Axis Bank"),('Bandhan Bank',"Bandhan Bank"),('CSB Bank',"CSB Bank"),('City Union Bank',"City Union Bank"),('DCB Bank',"DCB Bank"),('Dhanlaxmi Bank',"Dhanlaxmi Bank"),
    ('Federal Bank',"Federal Bank"),('HDFC Bank',"HDFC Bank"),('ICICI Bank',"ICICI Bank"),('IDBI Bank',"IDBI Bank"),('IDFC First Bank',"IDFC First Bank"),('IndusInd Bank',"IndusInd Bank"),('Jammu & Kashmir Bank',"Jammu & Kashmir Bank"),
    ('Karnataka Bank',"Karnataka Bank"),('Karur Vysya Bank',"Karur Vysya Bank"),('Kotak Mahindra Bank',"Kotak Mahindra Bank"),('Nainital Bank',"Nainital Bank"),('RBL Bank', "RBL Bank"),('South Indian Bank',"South Indian Bank"),('Tamilnad Mercantile Bank',"Tamilnad Mercantile Bank"),
    ('Yes Bank',"Yes Bank"),('Fincare Small Finance',"Fincare Small Finance"), ('Au Small Finance',"Au Small Finance"),('Capital Small Finance',"Capital Small Finance"),('Equitas Small Finance', "Equitas Small Finance"), ('ESAF Small Finance',"ESAF Small Finance"),('Jana Small Finance',"Jana Small Finance"),
    ('North East Small Finance',"North East Small Finance"),('Shivalik Small Finance',"Shivalik Small Finance"),('Suryoday Small Finance',"Suryoday Small Finance"),('Ujjivan Small Finance',"Ujjivan Small Finance"),('Unity Small Finance',"Unity Small Finance"),
    ('Utkarsh Small Finance',"Utkarsh Small Finance"),('Barclays',"Barclays"),('DBS',"DBS"),('Deutsche Bank',"Deutsche Bank"),('Doha',"Doha"),('HSBC',"HSBC"),('StandardChartered', "StandardChartered"),('abc bank',"abc bank"),('Post Office',"Post Office"),
    )

    id = models.IntegerField(primary_key=True, default=id_inc)
    bank_name = models.CharField(max_length=100, choices=your_ref_choices, null=True)
    bref = models.CharField(max_length=10, default='')
    
    bcode = models.IntegerField(default=999)
    rateid = models.IntegerField(default=auto_increament)
    date = models.DateField(null=True)
    effdate = models.CharField(max_length=25,null=True)
    s1 = models.CharField(max_length=45,default=None,null=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r1 = models.FloatField(default=None,null=True)
    s2 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r2 = models.FloatField(default=None,null=True, blank=True)
    s3 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r3 = models.FloatField(default=None,null=True, blank=True)
    s4 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r4 = models.FloatField(default=None,null=True, blank=True)
    s5 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r5 = models.FloatField(default=None,null=True, blank=True)
    s6 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r6 = models.FloatField(default=None,null=True, blank=True)
    s7 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r7 = models.FloatField(default=None,null=True, blank=True)
    s8 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r8 = models.FloatField(default=None,null=True, blank=True)
    s9 = models.CharField(max_length=45, default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r9 = models.FloatField(default=None,null=True, blank=True)
    s10 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r10 = models.FloatField(default=None,null=True, blank=True)
    s11 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r11 = models.FloatField(default=None,null=True, blank=True)
    s12 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r12 = models.FloatField(default=None,null=True, blank=True)
    s13 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r13 = models.FloatField(default=None,null=True, blank=True)
    s14 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r14 = models.FloatField(default=None,null=True, blank=True)
    s15 = models.CharField(max_length=45,default=None,null=True, blank=True, validators=[validate_slabs], help_text="only enter amounts in k(thousands), l(lacks), c(crores) if its a last slab just put $")
    r15 = models.FloatField(default=None,null=True, blank=True)
    floatrate = models.FloatField(default=0.0)

    class Meta:
        db_table = "sdrate"

    def save(self, *args, **kwargs):
        """
        Override the save method to add a unique bank code and reference
        for each instance of the model.

        The last instance of the model is fetched, and the bank code and
        reference of that instance is used to update the current instance.

        The slab fields are also converted to numeric format using the 
         
        

        auto_fill_slab function.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        last_instance = Sdrate.objects.filter(bank_name=self.bank_name)
        length = len(last_instance) - 1
        if length>=0:
            becode_add = last_instance[length].bcode
            self.bcode = becode_add
            bref_add = last_instance[length].bref
            self.bref = bref_add
        date_format = self.date.strftime("%d-%b-%y")
        self.effdate = date_format
        self.s1 = auto_fill_slab(self.s1)
        self.s2 = auto_fill_slab(self.s2)
        self.s3 = auto_fill_slab(self.s3)
        self.s4 = auto_fill_slab(self.s4)
        self.s5 = auto_fill_slab(self.s5)
        self.s6 = auto_fill_slab(self.s6)
        self.s7 = auto_fill_slab(self.s7)
        self.s8 = auto_fill_slab(self.s8)
        self.s9 = auto_fill_slab(self.s9)
        self.s10 = auto_fill_slab(self.s10)
        self.s11 = auto_fill_slab(self.s11)
        self.s12 = auto_fill_slab(self.s12)
        self.s13 = auto_fill_slab(self.s13)
        self.s14 = auto_fill_slab(self.s14)
        self.s15 = auto_fill_slab(self.s15)

        super(Sdrate, self).save(*args, **kwargs)



class bstat(models.Model):
    id = models.IntegerField(primary_key=True, default=id_inc1)
    name = models.CharField(max_length=100, null=True, default=None)
    bref = models.CharField(max_length=10, null=True, default=None)
    bcode = models.IntegerField()
    type = models.CharField(max_length=50, null=True)
    display_name = models.CharField(max_length=100, null=True)
    founded_yr = models.CharField(max_length=10)
    hqcity = models.CharField(max_length=50)
    hqstate = models.CharField(max_length=50)
    active = models.BooleanField()
    sd_url = models.CharField(max_length=500, null=True)
    fd_url = models.CharField(max_length=500, null=True)
    major_bank = models.BooleanField(null=True)
    payout_freq = models.CharField(max_length = 20, null=True)
    mobile_display_name = models.CharField(max_length=80, null=True, blank=True)
    maximum_fd_limit = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "bstat"



class Fdrate(models.Model):
    # your_ref_choices = (
    # ("Bank of Baroda","Bank of Baroda"),('Bank of India',"Bank of India"),('Bank of Maharashtra',"Bank of Maharashtra"),('Canara Bank',"Canara Bank"),('Central Bank of India',"Central Bank of India"),('Indian Bank',"Indian Bank"),
    # ('Indian Overseas Bank',"Indian Overseas Bank"),('Punjab and Sind Bank',"Punjab and Sind Bank"),('Punjab National Bank',"Punjab National Bank"),('State Bank of India',"State Bank of India"),('UCO Bank',"UCO Bank"),
    # ('Union Bank of India',"Union Bank of India"),('Axis Bank',"Axis Bank"),('Bandhan Bank',"Bandhan Bank"),('CSB Bank',"CSB Bank"),('City Union Bank',"City Union Bank"),('DCB Bank',"DCB Bank"),('Dhanlaxmi Bank',"Dhanlaxmi Bank"),
    # ('Federal Bank',"Federal Bank"),('HDFC Bank',"HDFC Bank"),('ICICI Bank',"ICICI Bank"),('IDBI Bank',"IDBI Bank"),('IDFC First Bank',"IDFC First Bank"),('IndusInd Bank',"IndusInd Bank"),('Jammu & Kashmir Bank',"Jammu & Kashmir Bank"),
    # ('Karnataka Bank',"Karnataka Bank"),('Karur Vysya Bank',"Karur Vysya Bank"),('Kotak Mahindra Bank',"Kotak Mahindra Bank"),('Nainital Bank',"Nainital Bank"),('RBL Bank', "RBL Bank"),('South Indian Bank',"South Indian Bank"),('Tamilnad Mercantile Bank',"Tamilnad Mercantile Bank"),
    # ('Yes Bank',"Yes Bank"),('Fincare Small Finance',"Fincare Small Finance"), ('Au Small Finance',"Au Small Finance"),('Capital Small Finance',"Capital Small Finance"),('Equitas Small Finance', "Equitas Small Finance"), ('ESAF Small Finance',"ESAF Small Finance"),('Jana Small Finance',"Jana Small Finance"),
    # ('North East Small Finance',"North East Small Finance"),('Shivalik Small Finance',"Shivalik Small Finance"),('Suryoday Small Finance',"Suryoday Small Finance"),('Ujjivan Small Finance',"Ujjivan Small Finance"),('Unity Small Finance',"Unity Small Finance"),
    # ('Utkarsh Small Finance',"Utkarsh Small Finance"),('Barclays',"Barclays"),('DBS',"DBS"),('Deutsche Bank',"Deutsche Bank"),('Doha',"Doha"),('HSBC',"HSBC"),('StandardChartered', "StandardChartered"),
    # ("Shriram","Shriram"), ("Bajaj","Bajaj"), ('ICICI HFC', 'ICICI HFC'), ('LIC HFL','LIC HFL'), ('Mahindra', 'Mahindra'), ('Sundaram', 'Sundaram'))


    # id = models.IntegerField(primary_key=True, default=id_inc2)
    # bcode = models.IntegerField()
    order = models.IntegerField(null=True)
    bref = models.CharField(max_length=10)
    # bank_name = models.CharField(max_length=100, null=True, choices=your_ref_choices)
    # effective_date = models.DateField(null=True)
    effstartdate = models.CharField(max_length=15)
    # effective_end_date = models.DateField(null=True, blank=True)
    effenddate = models.CharField(max_length=15, null=True)
    specialrate = models.CharField(max_length=5, null=True)
    tenorstart = models.CharField(max_length=15, validators=[validate_tenor], help_text="please enter tenor in days, months or years only 'eg.1y10m10d' ")
    tenorend = models.CharField(max_length=15, validators=[validate_tenor], help_text="please enter tenor in days, months or years only 'eg.1y10m10d'")
    startincl = models.CharField(max_length=7,help_text="if tenor starts from this date then put 'y' if not then put 'gt'(greater than)")
    endincl = models.CharField(max_length=7,help_text="if tenor ends from this date then put 'y' if not then put 'lt'(less than)")
    baserate = models.FloatField()
    seniorextra = models.FloatField(blank=True, null=True, help_text="if there is no addsenior, put 0 or leave it null")
    superextra = models.FloatField(blank=True, null=True, help_text="if there is no addsupsenior, put 0 or leave it null")
    # notes = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = "fdrate"

    def clean(self):
        start_date = self.tenorstart
        end_date = self.tenorend
        total_startdate = 0
        total_end_date = 0
        number = "0123456789"
        num=0
        for i in start_date:
            if i in number:
                num = num*10 + int(i)
            elif i=='y' or i=='Y':
                total_startdate += num*365
                num=0 
            elif i=='m' or i=='M':
                total_startdate += num*30
                num=0
            elif i=='d' or i=='D':
                total_startdate += num
                num=0
        for i in end_date:
            if i in number:
                num = num*10 + int(i)
            elif i=='y' or i=='Y':
                total_end_date += num*365
                num=0 
            elif i=='m' or i=='M':
                total_end_date += num*30
                num=0
            elif i=='d' or i=='D':
                total_end_date += num
                num=0
        if total_startdate > total_end_date:
            raise ValidationError("Start date cannot be greater than end date")
        
    
    def save(self, *args, **kwargs):
        """
        Override the save method to add a unique bank code and reference
        for each instance of the model.

        The last instance of the model is fetched, and the bank code and
        reference of that instance is used to update the current instance.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        # if self.id is None:
        #     self.id = id_inc2()

        last_instance = Fdrate.objects.filter(bref=self.bref)
        length = len(last_instance)-1
        
        if length>=0:
            bref_val = last_instance[length].bref 
            self.bref = bref_val
            # becode_add = last_instance[length].bcode
            # self.bcode = becode_add
            bref_add = last_instance[length].bref
            self.bref = bref_add
        # date_format = self.effective_date.strftime("%d-%b-%y")
        # self.effdate = date_format
        # if self.effective_end_date is not None:
        #     date_format_end = self.effective_end_date.strftime("%d-%b-%y")
        #     self.effenddate = date_format_end
        
        self.baserate = float("{:.5f}".format(float(self.baserate)))
        if self.seniorextra is not None:
            self.seniorextra = float("{:.5f}".format(float(self.seniorextra)))
        if self.superextra is not None:
            self.superextra = float("{:.5f}".format(float(self.superextra)))

        super(Fdrate, self).save(*args, **kwargs)

class Ratings(models.Model):
    bref = models.CharField(max_length=10)
    updatedate = models.CharField(max_length=10)
    Agency = models.CharField(max_length=50)
    Rating = models.CharField(max_length=6, null=True)
    Outlook = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "ratings"


class RatingAgencies(models.Model):
    Agency = models.CharField(max_length=50)
    parent = models.CharField(max_length=20, blank=True, null=True)
    DisplayPriority = models.IntegerField()

    class Meta:
        db_table = "rating_agencies"