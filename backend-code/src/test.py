import unittest
import json
import requests
from app import app
from threading import Thread
from time import sleep

# NOTE: Make sure you run 'pip3 install requests' in your virtualenv

# URL pointing to your local dev host
LOCAL_URL = 'http://localhost:5000'
CLASSBODY = {
        'name':'Ecology & Evolutionary Biology Weekly Seminar Series ',
        'description':'Dr. Simon Levin, Princeton: Public goods, from biofilms to societies, *Wednesday* 12:20-1:20p; Corson-Mudd Hall, A106',
        'location':'Corson/Mudd Hall, A106 ',
        'longitude':'-76.478701',
        'latitude':'42.447161',
        'date':'Wednesday, May 8, 2019 at 12:20pm to 1:20am',
        'tag':'Academic',
        'link':'http://ecologyandevolution.cornell.edu',
        'image':'6.jpg'
    }
USERBODY = {'name': 'Alicia Wang', 'netid': 'aw1234'}
ASSIGNMENTBODY = {'description': 'PA5', 'due_date': 1554076799}

all_events=[
    {
        'name':'Cat Video Fest',
        'description':'CatVideoFest is a compilation reel of the latest and best cat videos culled from countless hours of unique submissions and sourced animations, music videos, and, of course, classic internet powerhouses. Cornell Cinema is excited to bring back this joyous communal experience, and raise money for cats in need! 10% of the proceeds will go to the SPCA of Tompkins County. This super entertaining interactive event – which will include cat trivia & door prizes — is cosponsored with the Cornell Feline Health Center, Cornell Vet Feline Club and Cats Pajamas, a fun store for kids and kids at heart, located in the DeWitt Mall in downtown Ithaca. Leah Shafer ’94/’99/’08 (Media and Society, Hobart & William Smith Colleges) has written about the phenomenon of online cat videos. Recommended for all ages! More at catvideofest.com.  Advance tickets available at CornellCinemaTickets.com starting April 15.',
        'location':'Willard Straight theatre',
        'longitude':'-76.485420',
        'latitude':'42.446491',
        'date':'Friday, May 10, 2019 at 7:00pm to 8:10pm',
        'tag':'Social',
        'link':'https://cinema.cornell.edu/Spring2019/cat_video_fest.html',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/852313/big/f36cfebb2f1df9705a38e7028f41c2651d86cd4c.jpg'
    },
    {
        'name':'CU Jazz: Jazz+ Jam Session',
        'description':'Enjoy a meal and listen or join the band and play. Sponsored by Bethe House, CU Jazz, Jazz+ and SAFC.5:00-7:00 pm Jansens Dining RoomSpecial CU Jazz guests, local musicians, and faculty.',
        'location':' Hans Bethe House, Jansens Dinning Room',
        'longitude':'-76.488060',
        'latitude':'42.446790',
        'date':'May 4, 2019 at 5:00pm to 7:00pm',
        'tag':'Music',
        'link':'http://www.arts.cornell.edu/jazz',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/788003/big/1e4c9a982e76378689b68e7c3a4c701b0e96f5f2.jpg'
    },
    {
        'name':'Shadow',
        'description':'In a kingdom ruled by a young and unpredictable king, the military commander has a secret weapon: a “shadow,” a look-alike who can fool both his enemies and the King himself.  Now he must use this weapon in an intricate plan that will lead his people to victory in a war that the King does not want. Based on the fabled “Three Kingdoms” saga of Chinese legend… Shadow is a knotty tale of palace intrigue, old grudges and crafty doppelgangers. Director Zhang Yimou (Hero, House of Flying Daggers) once again pushes the boundaries of wuxia action to create a film like no other, masterfully painting a canvas of inky blacks and greys punctuated with bursts of color from the blood of the defeated. “Shadow [is] a thrilling return to form, which matches Zhang’s best work for the sheer voracious elegance of the images and possibly surpasses much of it for inventiveness.” (Variety) In Mandarin. Subtitled. More at wellgousa.com/films/shadow',
        'location':'Willard Straight theatre',
        'longitude':'-76.485420',
        'latitude':'42.446491',
        'date':'Thursday, May 9, 2019 at 7:30pm to 9:30pm',
        'tag':'Movies',
        'link':'https://www.facebook.com/events/1397738563700928/',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/852303/big/2ca6af7bab2ccaf4fbf9b337b14ee33abae04612.jpg'
    },
    {
        'name':'Europe Day: Celebrating CIES Fellowship Recipients',
        'description':'Please join Cornell Institute for European Studies (CIES) faculty, staff, and students in celebrating this year’s CIES fellowship and grant recipients in our annual Europe Day event, scheduled around the European Union’s observed celebration of Europe. Each fellowship recipient will be recognized publicly at the event; recipients’ advisors and recommenders are particularly encouraged to attend. The celebration begins at 4:30 p.m. with refreshments, and the recognition of fellowship recipients will take place at approximately 5:00 p.m.',
        'location':' A.D. White House',
        'longitude':'-76.482790',
        'latitude':'42.448210',
        'date':'Tuesday, May 7, 2019 at 4:30pm',
        'tag':'Social',
        'link':'https://www.facebook.com/events/2414844872083674/',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/863723/big/880bfd5a3ef861054de705e2cc7c0fb2a5f51bc2.jpg'
    },
    {
        'name':'Department of Physics Colloquium',
        'description':'Abstract:  Electromagnetic fields carry energy, momentum, and even angular momentum.  The momentum density is є0 (E x B), and it accounts, among other things for the pressure of light.  But even static fields can harbor momentum, and this would appear to contradict a general theorem:  if the center of energy of a close system is at rest, then its total momentum must be zero.  Evidently in such cases there lurks some other momentum, not electromagnetic in nature, which cancels the field momentum.  But finding this “hidden momentum” can be surprisingly subtle.  I’ll discuss a particularly nice example.',
        'location':'Rockefeller Hall, Schwartz Auditorium ',
        'longitude':'-76.481947',
        'latitude':'42.449110',
        'date':'Monday, May 6, 2019 at 4:00pm to 5:00pm',
        'tag':'Academic',
        'link':'https://physics.cornell.edu/upcoming-colloquia',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/835460/big/160349165d47d1935dc5f3287d0ad221c537debc.jpg'
    },
    {
        'name':'Ecology & Evolutionary Biology Weekly Seminar Series ',
        'description':'Dr. Simon Levin, Princeton: Public goods, from biofilms to societies, *Wednesday* 12:20-1:20p; Corson-Mudd Hall, A106',
        'location':'Corson/Mudd Hall, A106 ',
        'longitude':'-76.478701',
        'latitude':'42.447161',
        'date':'Wednesday, May 8, 2019 at 12:20pm to 1:20am',
        'tag':'Academic',
        'link':'http://ecologyandevolution.cornell.edu',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/16540/big/219d657f96ad42e86320bec70126f5540cdde486.jpg'
    },
    {
        'name':'Cornell Wind Symphony, Chorale, and Chamber Singers: CU Music',
        'description':'The Cornell Wind Symphony, Chorale, and Chamber Singers combine forces to explore the musical works of Percy Grainger and Igor Stravinsky, who were born only two weeks apart. Selections include Lincolnshire Posy and Symphony of Psalms, plus a premiere of a new work by Daniel Sabzghabaei',
        'location':' Bailey Hall, Auditorium ',
        'longitude':'-76.480013',
        'latitude':'42.449225',
        'date':' Sunday, May 5, 2019 at 3:00pm',
        'tag':'Music',
        'link':'http://music.cornell.edu',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/788050/big/1542d23cc4d2412df7500fe66618ba2c6fa06c61.jpg'
    },
    {
        'name':'CIT Training: Learn Excel Basics',
        'description':'In this 4-hour workshop, you will learn to create workbooks, edit and format data, modify worksheets, use functions, and print documents.To register for this class, visit:https://cornell.sabacloud.com/Saba/Web_spf/NA1PRD0089/c',
        'location':'120 Maple Ave, Training Room 150',
        'longitude':'-76.475750',
        'latitude':'42.441580',
        'date':'Monday, June 10, 2019 at 8:00am to 12:00pm',
        'tag':'Academic',
        'link':'N/A',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/383704/big/280b45456aa9d4e5eb4e4de5828d4d1dc0772e63.jpg'
    },
    {
        'name':'Cornell Games Club Weekly Meeting',
        'description':'We play board games, card games, miniatures games, and role-playing games (RPGs). Attendance is free and open to anyone. Rules are taught for most games.',
        'location':'Goldwin Smith Hall, 156-164 ',
        'longitude':'-76.483557',
        'latitude':'42.449265',
        'date':' Friday, May 10, 2019 at 7:00pm',
        'tag':'Sports',
        'link':'http://orgsync.rso.cornell.edu/org/gamesclub/',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/19179/big/e6c62d5db7126166d7447e3dd50f3996848fced7.jpg'
    },
    {
        'name':'LASP Seminar: "Socialist Domestic Infrastructures and the Politics of the Body: Bucharest and Havana" by Iulia Statica',
        'description':'Iulia Staticas presentation explores the role of domestic infrastructures in the constitution of gendered subjectivities through the concrete examples of two socialist cities: Bucharest and Havana. It investigates, through comparative study, the ways in which the socialist state aimed to reinvent domesticity and to constitute a new socialist subject—the Socialist Man and Woman— through the construction of an extensive housing infrastructure. The domestic revolution, initiated by Khrushchev, constitutes the narrative that both Bucharest and Havana share; an archaeology of its formation reveals it as a common paradigm instituting a politics of domesticity—generated by the transition to state socialism. Their desire to establish a new ideology through the convergence of productive and domestic life by way of industrialization resulted in an ontological transformation that connected ideology, domestic infrastructure, and the subjective body. The project argues that domestic infrastructures were constituted as the aesthetic and technological vehicle through which the body was politically inscribed and shaped. The total project of domesticity initiated in the 1950s can thus be understood as built on the legacy of the programs of the Russian avant-gardes, and the political formation of the body seen as an infrastructural and cognitive process that is articulated at the ‘hearth’ of the home.',
        'location':' Uris Hall, 153 109 Tower Road',
        'longitude':'-76.485420',
        'latitude':'42.446491',
        'date':'Monday, May 6, 2019 at 12:15pm to 1:10pm',
        'tag':'Seminar',
        'link':'N/A',
        'image':'https://d3e1o4bcbhmj8g.cloudfront.net/photos/804295/big/e289661ed9089207a459ee9c88cb85dcc0413ec1.jpg'
    }
]


class TestRoutes(unittest.TestCase):

    def test_get_initial_classes(self):
        res = requests.get(LOCAL_URL + '/api/classes/')
        assert res.json()['success']

    def test_create_class(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[0]))
        cls = res.json()['data']
        assert res.json()['success']
        assert cls['tag'] == 'Social'
    def test_create_class1(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[1]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class2(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[2]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class3(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[3]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class4(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[4]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class5(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[5]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class6(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[6]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class7(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[7]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class8(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[8]))
        cls = res.json()['data']
        assert res.json()['success']
    def test_create_class9(self):
        res = requests.post(LOCAL_URL + '/api/event/', data=json.dumps(all_events[9]))
        cls = res.json()['data']
        assert res.json()['success']

    def test_get_class(self):
        res = requests.post(LOCAL_URL + '/api/classes/', data=json.dumps(CLASSBODY))
        cls_id = res.json()['data']['id']
        res = requests.get(LOCAL_URL + '/api/class/' + str(cls_id) + '/')
        assert res.json()['success'] 

    def test_delete_class(self):
        res = requests.post(LOCAL_URL + '/api/classes/', data=json.dumps(CLASSBODY))
        cls_id = res.json()['data']['id']
        res = requests.delete(LOCAL_URL + '/api/class/' + str(cls_id) + '/')
        assert res.json()['success']
    
    def test_create_user(self):
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        cls = res.json()['data']
        assert res.json()['success']
        assert cls['name'] == 'Alicia Wang'
        assert cls['netid'] == 'aw1234'
    
    def test_get_user(self):
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        usr_id = res.json()['data']['id']
        res = requests.get(LOCAL_URL + '/api/user/' + str(usr_id) + '/')
        assert res.json()['success'] 
    
    def test_add_student_to_class(self):
        res = requests.post(LOCAL_URL + '/api/classes/', data=json.dumps(CLASSBODY))
        cls_id = res.json()['data']['id']
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        usr_id = res.json()['data']['id']
        body = {'type': 'student', 'user_id': usr_id}
        res = requests.post(LOCAL_URL + '/api/class/' + str(cls_id) + '/add/',
                            data=json.dumps(body))
        assert res.json()['success']

        res = requests.get(LOCAL_URL + '/api/class/' + str(cls_id) + '/')
        assert res.json()['success']
        students = res.json()['data']['students']
        assert len(students) == 1
        assert students[0]['name'] == 'Alicia Wang'
        
    def test_create_assignment_for_class(self):
        res = requests.post(LOCAL_URL + '/api/classes/', data=json.dumps(CLASSBODY))
        cls_id = res.json()['data']['id']
        res = requests.post(LOCAL_URL + '/api/class/' + str(cls_id) + '/assignment/',
                            data=json.dumps(ASSIGNMENTBODY))
        assert res.json()['data']['description'] == 'PA5'
        assert res.json()['data']['due_date'] == 1554076799 

    def test_get_invalid_class(self):
        res = requests.get(LOCAL_URL + '/api/class/1000/')
        assert not res.json()['success']

    def test_delete_invalid_class(self):
        res = requests.delete(LOCAL_URL + '/api/class/1000/')
        assert not res.json()['success']
    
    def test_get_invalid_user(self):
        res = requests.get(LOCAL_URL + '/api/user/1000/')
        assert not res.json()['success']

    def test_add_user_invalid_class(self):
        body = {'type': 'instructor', 'user_id': 0}
        res = requests.post(LOCAL_URL + '/api/class/1000/add/', data=json.dumps(body))
        assert not res.json()['success']

    def test_create_assignment_invalid_class(self):
        res = requests.post(LOCAL_URL + '/api/class/1000/assignment/', 
                            data=json.dumps(ASSIGNMENTBODY))
        assert not res.json()['success']

    def test_cls_id_increments(self):
        res = requests.post(LOCAL_URL + '/api/classes/', data=json.dumps(CLASSBODY))
        cls_id = res.json()['data']['id']

        res2 = requests.post(LOCAL_URL + '/api/classes/', data=json.dumps(CLASSBODY))
        cls_id2= res2.json()['data']['id']

        assert cls_id + 1 == cls_id2 

def run_tests():
    sleep(1.5)
    unittest.main()

if __name__ == '__main__':
    thread = Thread(target=run_tests)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
