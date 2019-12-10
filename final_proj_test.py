import unittest
import final_proj as final
from final_proj import *


class TestBar(unittest.TestCase):

    def testConstructor(self):
        bar1 = final.Bar('New Life')
        bar2 = final.Bar('new', addr='1000 DreamWorld Str')
        bar3 = final.Bar('old', rev="here is a short review", addr="100 tear dr", phone_num='2124007234',
                         url='https://www.newsite.org', price='1.2', hours=[], img='', neigh='MidTown')
        self.assertEqual(bar1.addr, "")
        self.assertEqual(bar2.addr, "1000 DreamWorld Str")
        self.assertEqual(bar3.hours, [])


class TestScrape(unittest.TestCase):
    def testGetBars(self):
        (barls, neighls) = final.get_bars()

        self.assertEqual(len(barls), 131)
        self.assertEqual(len(neighls), 24)
        self.assertEqual(barls[0].name, 'Holiday Cocktail Lounge')
        self.assertEqual(neighls[2], 'West Village')

    def testGetNeigh(self):
        neighls = final.get_bars()[1]
        self.neighbors = final.get_neigh(neighls)

        self.assertEqual(type(self.neighbors), dict)
        self.assertEqual(self.neighbors[neighls[3]], 4)


class TestDatabase(unittest.TestCase):

    def test_bar_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Bars'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Death & Co',), result_list)
        self.assertEqual(len(result_list), 131)

        conn.close()

    def test_neighbor_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT NeighName
            FROM Neighborhoods
            WHERE Bar_Num=12
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('East Village',), result_list)
        self.assertEqual(len(result_list), 2)

        sql = '''
            SELECT COUNT(*)
            FROM Neighborhoods
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertTrue(count == 24)

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT NeighName
            FROM Neighborhoods
                JOIN Bars
                ON Bars.Neighborhood=Neighborhoods.Id
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Midtown',), result_list)
        conn.close()


if __name__ == '__main__':
    unittest.main()
