'''Created by Jakub Zasada
    before you start try:

    python -m pip install --upgrade pip
    pip install click
    pip install peewee

    json file must be in the same directory with this file
    if you dont know how to run it just type:
        python script.py --help
'''
import json, os, click, datetime
from peewee import *

db_name = 'persons.db' #name of database which will be created
json_file = 'persons.json' #name of your json file

db = SqliteDatabase('%s' % db_name) #work with sqlite3

class PersonDB(Model): #sql database model
    gender = CharField()
    name_title = CharField()
    first_name = CharField()
    last_name = CharField()
    street_number = IntegerField()
    street_name = CharField()
    city = CharField()
    city_state = CharField()
    country = CharField()
    postcode = CharField()
    coord_lati = CharField()
    coord_long = CharField()
    timezone_offset = CharField()
    timezone_description = CharField()
    email = CharField()
    login_uuid = CharField()
    username = CharField()
    password = CharField()
    pass_salt = CharField()
    pass_md5 = CharField()
    pass_sha1 = CharField()
    pass_sha256 = CharField()
    birth = CharField()
    age = IntegerField()
    days_to_birthday = IntegerField()
    register_date = CharField()
    register_age = IntegerField()
    phone = CharField()
    phone_cell = CharField()
    id_name = CharField(null=True)
    id_value = CharField(null=True)
    nat = CharField()
    class Meta:
        database = db

class Data():
    def __init__(self):
        self.persons = []

    def check_days(self, dob, dude): 
        dob = dob.replace('T',' ')
        dob = dob[0:10]
        month_day = datetime.datetime.strptime(dob,'%Y-%m-%d').date()
        if month_day.month == 2 and month_day.day == 29:
            month_day = month_day.replace(month=3)
            month_day = month_day.replace(day=1)
        current = datetime.datetime.today().date()
        month_day = month_day.replace(year=current.year)
        if month_day.month < current.month or (month_day.month==current.month and month_day.day < current.day):
            month_day = month_day + datetime.timedelta(365)
            result = abs(month_day-current)
            dude.days_to_birthday = result.days
        else:
            result = abs(month_day - current)
            dude.days_to_birthday = result.days    

    def load_data(self, json_file):
        with open('%s' % json_file, encoding='utf-8-sig') as j:
            data = json.load(j)
            results = data['results']
            for person in results:
                dude = PersonDB()
                dude.gender = person['gender']
                dude.name_title = person['name']['title']
                dude.first_name = person['name']['first']
                dude.last_name = person['name']['last']
                dude.street_number = person['location']['street']['number']
                dude.street_name = person['location']['street']['name']
                dude.city = person['location']['city']
                dude.city_state = person['location']['state']
                dude.country = person['location']['country']
                dude.postcode = person['location']['postcode']
                dude.coord_lati = person['location']['coordinates']['latitude']
                dude.coord_long = person['location']['coordinates']['longitude']
                dude.timezone_offset = person['location']['timezone']['offset']
                dude.timezone_description = person['location']['timezone']['description']
                dude.email = person['email']
                dude.login_uuid = person['login']['uuid']
                dude.username = person['login']['username']
                dude.password = person['login']['password']
                dude.pass_salt = person['login']['salt']
                dude.pass_md5 = person['login']['md5']
                dude.pass_sha1 = person['login']['sha1']
                dude.pass_sha256 = person['login']['sha256']
                dude.birth = person['dob']['date']
                dob = dude.birth
                dude.age = person['dob']['age']
                dude.register_date = person['registered']['date']
                dude.register_age = person['registered']['age']
                phone = person['phone']
                phone = phone.replace('-','')
                phone = phone.replace(' ','')
                phone = phone.replace('(','')
                phone = phone.replace(')','')
                dude.phone = phone
                cell = person['cell']
                cell = cell.replace('-','')
                cell = cell.replace(' ','')
                cell = cell.replace('(','')
                cell = cell.replace(')','')
                dude.phone_cell = cell
                dude.id_name = person['id']['name']
                dude.id_value = person['id']['value']
                dude.nat = person['nat']
                self.check_days(dob, dude)
                self.persons.append(dude)
                dude.save()
            print('success')              

class DataLoad():
    def female_and_male(self):
        genders = []
        female = 0
        male = 0
        for person in PersonDB.select():
            if person.gender == 'female':
                female+=1
            else:
                male+=1
            genders.append(person.gender)
        all_len = len(genders)
        female = int((female*100)/all_len)
        male = int((male*100)/all_len)
        print('female: ',female,'%')
        print('male: ',male,'%')

    def average_age(self):
        age_all = 0
        for ile, person in enumerate(PersonDB.select()):
            age_all = age_all + person.age
        print('Average age: ', int(age_all/(ile+1)))

    def average_age_gender(self, gender):
        age_all = 0
        ile = 0
        for person in PersonDB.select():
            if person.gender == str(gender):
                age_all = age_all + person.age
                ile+=1
            else: pass
        print('Average age of %s:' % gender, int(age_all/(ile)))        
    
    def popular_city(self,n):
        cities = {}
        for person in PersonDB.select():
            if person.city in cities:
                cities[person.city]+=1
            else:
                cities[person.city] = 1
        sort_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
        counter = 0
        for city in sort_cities:
            print(city[0],':',city[1])
            counter+=1
            if counter >= n:
                break

    def popular_password(self,n):
        passwords = {}
        for person in PersonDB.select():
            if person.password in passwords:
                passwords[person.password]+=1
            else:
                passwords[person.password] = 1
        sort_password = sorted(passwords.items(), key=lambda x: x[1], reverse=True)
        counter = 0
        for passwd in sort_password:
            print(passwd[0],':',passwd[1])
            counter+=1
            if counter >= n:
                break        
                                          
    def birth_from(self, date_from, date_to):
        date_from = datetime.datetime.strptime(date_from,'%Y-%m-%d').date()
        date_to = datetime.datetime.strptime(date_to,'%Y-%m-%d').date()
        for person in PersonDB.select():
            person_date = person.birth
            person_date = person_date.replace('T',' ')
            person_date = person_date[0:10]
            person_date = datetime.datetime.strptime(person_date, '%Y-%m-%d').date()
            if person_date >= date_from and person_date <= date_to:
                print(person_date, person.first_name, person.last_name)

    def most_safe_pass(self,n):
        passwords = {}
        for person in PersonDB.select():
            if person.password in passwords:
                pass   
            else:
                passwords[person.password] = 0 
                if any(char.islower() for char in person.password):
                    passwords[person.password]+=1
                if any(char.isupper() for char in person.password):
                    passwords[person.password]+=2
                if any(char.isdigit() for char in person.password):
                    passwords[person.password]+=1 
                if len(person.password) >= 8:
                    passwords[person.password]+=5 
                if any(not(char.isdigit()) and not (char.islower()) and not(char.isupper()) for char in person.password):
                    passwords[person.password]+=3               
        sorted_passwords = sorted(passwords.items(), key=lambda x: x[1], reverse=True)
        counter = 0
        for password in sorted_passwords:
            print(password[0],':',password[1])
            counter+=1
            if counter >= n:
                break           

def start(option, number, date_from, date_to):
    if (os.path.isfile('./%s' % db_name) == True) or option != 0:
        db.connect
        data_from_db = DataLoad()
        if option == 1:
            data_from_db.female_and_male()     
        if option == 2:
            data_from_db.average_age()
        if option == 3:
            data_from_db.average_age_gender('female')
        if option == 4:
            data_from_db.average_age_gender('male')
        if option == 5:
            data_from_db.popular_city(number)  
        if option == 6:
            data_from_db.popular_password(number) 
        if option == 7:
            data_from_db.birth_from(date_from, date_to)
        if option == 8:
            data_from_db.most_safe_pass(number)
    else:
        db.connect
        db.create_tables([PersonDB], safe=True)
        print('DB has been created')
        data = Data()
        data.load_data(json_file)

@click.group()
def comands():
    pass

@comands.command()
def load_json():
    start(0, 0,'','')

@comands.command()
def genders():
    start(1, 0,'','')

@comands.command()
def average_age():
    start(2, 0,'','')

@comands.command()
def average_age_female():
    start(3, 0,'','')  

@comands.command()
def average_age_male():
    start(4, 0,'','')  

@comands.command()
@click.option('--number',default=1)
def most_popular_city(number):
    start(5, number,'','') 

@comands.command()
@click.option('--number',default=1)
def most_popular_password(number):
    start(6, number,'','')                

@comands.command()
@click.option('--date-from',default='1900-01-01')
@click.option('--date-to',default='2020-12-31')
def birth_betwen(date_from, date_to):
    start(7, 1,date_from,date_to) 

@comands.command()
@click.option('--number',default=1)
def most_safe_password(number):
    start(8, number,'','')         

if __name__ == '__main__':
    comands()          