import unittest
import json
import requests
from app import app
from threading import Thread
from time import sleep

local_url='http://localhost:4000'
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
        'image':'1.jpg'
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
        'image':'2.jpg'
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
        'image':'3.jpg'
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
        'image':'4.jpg'
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
        'image':'5.jpg'
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
        'image':'6.jpg'
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
        'image':'7.jpg'
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
        'image':'8.jpg'
    },
    {
        'name':'Cornell Games Club Weekly Meeting',
        'description':'We play board games, card games, miniatures games, and role-playing games (RPGs). Attendance is free and open to anyone. Rules are taught for most games.',
        'location':'Goldwin Smith Hall, 156-164 ',
        'longitude':'-76.483557',
        'latitude':'42.449265',
        'date':' Friday, May 10, 2019 at 7:00pm',
        'tag':'Social',
        'link':'http://orgsync.rso.cornell.edu/org/gamesclub/',
        'image':'9.jpg'
    },
    {
        'name':'LASP Seminar: "Socialist Domestic Infrastructures and the Politics of the Body: Bucharest and Havana" by Iulia Statica',
        'description':'Iulia Staticas presentation explores the role of domestic infrastructures in the constitution of gendered subjectivities through the concrete examples of two socialist cities: Bucharest and Havana. It investigates, through comparative study, the ways in which the socialist state aimed to reinvent domesticity and to constitute a new socialist subject—the Socialist Man and Woman— through the construction of an extensive housing infrastructure. The domestic revolution, initiated by Khrushchev, constitutes the narrative that both Bucharest and Havana share; an archaeology of its formation reveals it as a common paradigm instituting a politics of domesticity—generated by the transition to state socialism. Their desire to establish a new ideology through the convergence of productive and domestic life by way of industrialization resulted in an ontological transformation that connected ideology, domestic infrastructure, and the subjective body. The project argues that domestic infrastructures were constituted as the aesthetic and technological vehicle through which the body was politically inscribed and shaped. The total project of domesticity initiated in the 1950s can thus be understood as built on the legacy of the programs of the Russian avant-gardes, and the political formation of the body seen as an infrastructural and cognitive process that is articulated at the ‘hearth’ of the home.',
        'location':' Uris Hall, 153 109 Tower Road',
        'longitude':'-76.485420',
        'latitude':'42.446491',
        'date':'Monday, May 6, 2019 at 12:15pm to 1:10pm',
        'tag':'Academic',
        'link':'N/A',
        'image':'10.jpg'
    }
]

class Add_events(unittest.TestCase):

    def get_all(self):

        res=requests.get(local_url+'/api/events/')
        assert res.json()['success']
    def add_eve(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[0]))
        cls=res.json()['data']
        assert cls['name'] =='Cat Video Fest'
        assert res.json()['success']
    def add_eve1(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[1]))
        assert res.json()['success']
    def add_eve2(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[2]))
        assert res.json()['success']
    def add_eve3(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[3]))
        assert res.json()['success']
    def add_eve4(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[4]))
        assert res.json()['success']
    def add_eve5(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[5]))
        assert res.json()['success']
    def add_eve6(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[6]))
        assert res.json()['success']
    def add_eve7(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[7]))
        assert res.json()['success']
    def add_eve8(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[8]))
        assert res.json()['success']
    def add_eve9(self):
        res=requests.post(local_url+'/api/event/',data=json.dumps(all_events[9]))
        assert res.json()['success']

def run_tests():
    sleep(1.5)
    unittest.main()
if __name__ == '__main__':
    thread=Thread(target=run_tests)
    thread.start() 				   
    app.run(host='0.0.0.0',port='4000',debug=False)

