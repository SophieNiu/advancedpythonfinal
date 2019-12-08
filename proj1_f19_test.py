import unittest
import proj1_f19 as proj1

class TestMedia(unittest.TestCase):

    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        
        self.assertEqual(m2.__str__(), '1999 by Prince (No Year)')
        self.assertEqual(len(m1),0)

class TestSong(unittest.TestCase):

    def testConstructor(self):
        s1 = proj1.Song()
        s2 = proj1.Song('Hey Jude', 'The Beatles','1968', genre = 'Rock')
        
        self.assertEqual(s1.genre, "No Genre")
        self.assertEqual(s1.track_len, 0)
        self.assertEqual(s1.album,'No Album')
        self.assertEqual(s1.author,'No Author')

        self.assertEqual(s2.title, 'Hey Jude')
        self.assertEqual(s2.genre,'Rock')
        self.assertEqual(s2.album,'No Album')
        self.assertEqual(len(s2),0)
        self.assertEqual(s2.track_len,0)
        self.assertEqual(s2.__str__(),'Hey Jude by The Beatles (1968) [Rock]')

        # self.assertIsNone(s2.rating)

class TestMovie(unittest.TestCase):

    def testConstructor(self):
        mo1 = proj1.Movie()
        mo2 = proj1.Movie('Jaws', 'Steven Spielberg', '1975', rating= 'PG')

        self.assertEqual(mo1.author, 'No Author')
        self.assertEqual(mo1.rating, 'No Rating')
        self.assertEqual(mo2.title, 'Jaws')
        self.assertEqual(mo2.rating,'PG')
        self.assertEqual(mo2.__str__(),'Jaws by Steven Spielberg (1975)[PG]')
        self.assertEqual(len(mo2),0)
        self.assertEqual(mo2.movie_len, 0)


class TestJson(unittest.TestCase):

    def testMovieParsing(self):
        obj_list = proj1.parseJson('sample_json.json')
        movie1 = obj_list[0] 

        self.assertEqual(movie1.author,'Steven Spielberg')
        self.assertEqual(movie1.title, 'Jaws')
        self.assertEqual(len(movie1), 124) 
        self.assertEqual(movie1.__str__(), 'Jaws by Steven Spielberg (1975)[PG]')
        self.assertEqual(movie1.rating, 'PG')
        self.assertEqual(movie1.movie_len,7451455)

    def testSongParsing(self):
        obj_list = proj1.parseJson('sample_json.json')
        song1 = obj_list[1]

        self.assertEqual(song1.author,'The Beatles')
        self.assertEqual(song1.title, 'Hey Jude')
        self.assertEqual(song1.track_len, 431333) 
        self.assertEqual(song1.__str__(), 'Hey Jude by The Beatles (1968) [Rock]')
        self.assertEqual(song1.genre, 'Rock')
        self.assertEqual(len(song1), 431)

    def testMediaParsing(self):
        obj_list = proj1.parseJson('sample_json.json')
        media1 = obj_list[2]

        self.assertEqual(media1.author,'Helen Fielding')
        self.assertEqual(media1.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(media1.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")

        
class TestiTunes(unittest.TestCase):
    def testCommonWords(self):
        #test common word: baby
        baby_call= proj1.calliTunes('baby')['results']
        baby_list = proj1.parseiTunes(baby_call)
        # To make the call results more visible, uncomment the below print statements for the defined value for assertEqual
        # print('Search baby total return number of results: ', len(baby_call))
        # print('media list size: ',len(baby_list['media_list']))
        # print('song list size: ',len(baby_list['song_list']))
        # print('movie list size: ',len(baby_list['movie_list']))

        self.assertEqual(len(baby_list['media_list']),1)
        self.assertEqual(len(baby_list['song_list']),48)
        self.assertEqual(len(baby_list['movie_list']),1)
        self.assertIsInstance(baby_list['media_list'][0], proj1.Media)
        self.assertIsInstance(baby_list['song_list'][1], proj1.Song)
        self.assertIsInstance(baby_list['movie_list'][0], proj1.Movie)

        #test common word: love
        love_call = proj1.calliTunes('love')['results']
        love_list = proj1.parseiTunes(love_call) 
        
        # To make the call results more visible, uncomment the below print statements for the defined value for assertEqual
        # print("Search 'love' total return number of results: ", len(baby_call))
        # print('media list size: ',len(love_list['media_list']))
        # print('song list size: ',len(love_list['song_list']))
        # print('movie list size: ',len(love_list['movie_list']))

        self.assertEqual(len(love_list['media_list']),3)
        self.assertEqual(len(love_list['song_list']),41)
        self.assertEqual(len(love_list['movie_list']),6)
        self.assertIsInstance(love_list['media_list'][0], proj1.Media)
        self.assertIsInstance(love_list['song_list'][1], proj1.Song)
        self.assertIsInstance(love_list['movie_list'][0], proj1.Movie)

    def testRareWords(self):
        ## Test rare word: moana ##
        moana_call = proj1.calliTunes('moana')['results']
        moana_list = proj1.parseiTunes(moana_call)
        
        # To make the call results more visible, uncomment the below print statements for the defined value for assertEqual
        # print("Search 'moana' total return number of results: ", len(moana_call))
        # print('media list size: ',len(moana_list['media_list']))
        # print('song list size: ',len(moana_list['song_list']))
        # print('movie list size: ',len(moana_list['movie_list']))

        self.assertEqual(len(moana_list['media_list']),1)
        self.assertEqual(len(moana_list['song_list']),48)
        self.assertEqual(len(moana_list['movie_list']),1)
        self.assertIsInstance(moana_list['media_list'][0], proj1.Media)
        # print(moana_list['song_list'][0].author) trying to see why the item is returned with the search
        self.assertIsInstance(moana_list['song_list'][1], proj1.Song)
        self.assertIsInstance(moana_list['movie_list'][0], proj1.Movie)

        ## Test rare word: helter skelter ##
        helter_call = proj1.calliTunes('helter skelter')['results']
        helter_list = proj1.parseiTunes(helter_call)

        # To make the call results more visible, uncomment the below print statements for the defined value for assertEqual
        # print("Search 'helter skelter' total return number of results: ", len(helter_call))
        # print('media list size: ',len(helter_list['media_list']))
        # print('song list size: ',len(helter_list['song_list']))
        # print('movie list size: ',len(helter_list['movie_list']))

        self.assertEqual(len(helter_list['media_list']),3)
        self.assertEqual(len(helter_list['song_list']),46)
        self.assertEqual(len(helter_list['movie_list']),1)
        self.assertIsInstance(helter_list['media_list'][0], proj1.Media)
        self.assertIsInstance(helter_list['song_list'][1], proj1.Song)
        self.assertIsInstance(helter_list['movie_list'][0], proj1.Movie)


    def testNonsense(self):
        nonsense_call = proj1.calliTunes('&@#!$')['results']
        nonsense_list = proj1.parseiTunes(nonsense_call)

        # To make the call results more visible, uncomment the below print statements for the defined value for assertEqual
        # print("Search '&@#!$' total return number of results: ", len(nonsense_call))
        # print('media list size: ',len(nonsense_list['media_list']))
        # print('song list size: ',len(nonsense_list['song_list']))
        # print('movie list size: ',len(nonsense_list['movie_list']))

        self.assertEqual(len(nonsense_list['media_list']),27)
        self.assertEqual(len(nonsense_list['song_list']),1)
        self.assertEqual(len(nonsense_list['movie_list']),22)
        self.assertIsInstance(nonsense_list['media_list'][0], proj1.Media)
        self.assertIsInstance(nonsense_list['song_list'][0], proj1.Song)
        self.assertIsInstance(nonsense_list['movie_list'][0], proj1.Movie)

        # still don't know why these results return from the api
        # print(nonsense_list['song_list'][0].__str__())
    
    def testEmpty(self):
        empty_call =proj1.calliTunes('')['results']
        empty_list = proj1.parseiTunes(empty_call)

        # To make the call results more visible, uncomment the below print statements for the defined value for assertEqual
        # print("Blank search total return number of results: ", len(empty_call))
        # print('media list size: ',len(empty_list['media_list']))
        # print('song list size: ',len(empty_list['song_list']))
        # print('movie list size: ',len(empty_list['movie_list']))

        self.assertEqual(len(empty_list['media_list']),0)
        self.assertEqual(len(empty_list['song_list']),0)
        self.assertEqual(len(empty_list['movie_list']),0)
        
        
unittest.main()
