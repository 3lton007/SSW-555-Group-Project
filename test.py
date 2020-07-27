import unittest
import datetime
import sys
from typing import Iterator, Tuple, IO, List, Dict, Set
from SSW555_Group_Project import GedcomFile, Individual, Family
from prettytable import PrettyTable

class main_testing(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        GedcomFile._individual_dt.clear()
        GedcomFile._family_dt.clear()
        GedcomFile._individuals_living_and_married.clear()
        GedcomFile._individuals_living_over_thirty_and_never_married.clear()
        self.gedcom = GedcomFile()
        self.today = datetime.datetime.today()

        # Create 12 individuals and assign IDs and names.
        # IDs are from @I0@ to @I11@
        # Names are from "Test Subject0" to "Test Subject11"
        # All even numbered IDs are Male. All odd are Female.
        for i in range (0, 12):
            person = Individual()
            person.id = "@I" + str(i) + "@"
            person.name = "Test " + "Subject"+ str(i)
            person.living = True
            if person.id in "@I0@ @I2@ @I4@ @I6@ @I8@ @I10@":
                person.sex = "M"
            else:
                person.sex = "F"
            GedcomFile._individual_dt[person.id] = person

        
        GedcomFile._individual_dt["@I0@"].birth = datetime.date(1900,12,12)
        GedcomFile._individual_dt["@I1@"].birth = datetime.date(1900,11,11)
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(1910,10,10)
        GedcomFile._individual_dt["@I3@"].birth = datetime.date(1910,9,9)
        GedcomFile._individual_dt["@I4@"].birth = datetime.date(1920,8,8)
        GedcomFile._individual_dt["@I5@"].birth = datetime.date(1920,7,7)
        GedcomFile._individual_dt["@I6@"].birth = datetime.date(1930,6,6)
        GedcomFile._individual_dt["@I7@"].birth = datetime.date(1930,6,6)
        GedcomFile._individual_dt["@I8@"].birth = datetime.date(1940,5,5)
        GedcomFile._individual_dt["@I9@"].birth = datetime.date(1940,5,5)
        GedcomFile._individual_dt["@I10@"].birth = datetime.date(1950,6,6)
        GedcomFile._individual_dt["@I11@"].birth = datetime.date(1950,12,31)
        for individual in GedcomFile._individual_dt.values():
            individual.setAge()

        # Create 6 families and assign IDs
        # IDs are from @F_test0 to @F_test5
        for i in range (0,6):
            family = Family()
            family.id = "@F_test" + str(i)
            GedcomFile._family_dt[family.id] = family

        # Pair up individuals into husbands and wives.
        GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        GedcomFile._family_dt["@F_test0"].husband_name = GedcomFile._individual_dt["@I0@"].name
        GedcomFile._family_dt["@F_test0"].wife_id = "@I1@"
        GedcomFile._family_dt["@F_test0"].wife_name = GedcomFile._individual_dt["@I1@"].name
        GedcomFile._family_dt["@F_test0"].marriage_date = datetime.date(1930,1,1)
        GedcomFile._individual_dt["@I0@"].fams = set(["@F_test0"])
        GedcomFile._individual_dt["@I1@"].fams = set(["@F_test0"])  

        GedcomFile._family_dt["@F_test1"].husband_id = "@I2@"
        GedcomFile._family_dt["@F_test1"].husband_name = GedcomFile._individual_dt["@I2@"].name
        GedcomFile._family_dt["@F_test1"].wife_id = "@I3@"
        GedcomFile._family_dt["@F_test1"].wife_name = GedcomFile._individual_dt["@I3@"].name
        GedcomFile._family_dt["@F_test1"].marriage_date = datetime.date(1940,2,2)
        GedcomFile._individual_dt["@I2@"].fams = set(["@F_test1"])
        GedcomFile._individual_dt["@I3@"].fams = set(["@F_test1"])  

        GedcomFile._family_dt["@F_test2"].husband_id = "@I4@"
        GedcomFile._family_dt["@F_test2"].husband_name = GedcomFile._individual_dt["@I4@"].name
        GedcomFile._family_dt["@F_test2"].wife_id = "@I5@"
        GedcomFile._family_dt["@F_test2"].wife_name = GedcomFile._individual_dt["@I5@"].name
        GedcomFile._family_dt["@F_test2"].marriage_date = datetime.date(1950,3,3)
        GedcomFile._individual_dt["@I4@"].fams = set(["@F_test2"])
        GedcomFile._individual_dt["@I5@"].fams = set(["@F_test2"])   

        GedcomFile._family_dt["@F_test3"].husband_id = "@I6@"
        GedcomFile._family_dt["@F_test3"].husband_name = GedcomFile._individual_dt["@I6@"].name
        GedcomFile._family_dt["@F_test3"].wife_id = "@I7@"
        GedcomFile._family_dt["@F_test3"].wife_name = GedcomFile._individual_dt["@I7@"].name
        GedcomFile._family_dt["@F_test3"].marriage_date = datetime.date(1960,4,4)
        GedcomFile._individual_dt["@I6@"].fams = set(["@F_test3"])
        GedcomFile._individual_dt["@I7@"].fams = set(["@F_test3"])   

        GedcomFile._family_dt["@F_test4"].husband_id = "@I8@"
        GedcomFile._family_dt["@F_test4"].husband_name = GedcomFile._individual_dt["@I8@"].name
        GedcomFile._family_dt["@F_test4"].wife_id = "@I9@"
        GedcomFile._family_dt["@F_test4"].wife_name = GedcomFile._individual_dt["@I9@"].name
        GedcomFile._family_dt["@F_test4"].marriage_date = datetime.date(1970,5,5)
        GedcomFile._individual_dt["@I8@"].fams = set(["@F_test4"])
        GedcomFile._individual_dt["@I9@"].fams = set(["@F_test4"])   

        GedcomFile._family_dt["@F_test5"].husband_id = "@I10@"
        GedcomFile._family_dt["@F_test5"].husband_name = GedcomFile._individual_dt["@I10@"].name
        GedcomFile._family_dt["@F_test5"].wife_id = "@I11@"
        GedcomFile._family_dt["@F_test5"].wife_name = GedcomFile._individual_dt["@I11@"].name
        GedcomFile._family_dt["@F_test5"].marriage_date = datetime.date(1980,6,6)
        GedcomFile._individual_dt["@I10@"].fams = set(["@F_test5"])
        GedcomFile._individual_dt["@I11@"].fams = set(["@F_test5"])   


    def test_US35_30days(self):
        GedcomFile._individual_dt["@I0@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=30))
        name = GedcomFile._individual_dt["@I0@"].name
        id = GedcomFile._individual_dt["@I0@"].id
        birth = GedcomFile._individual_dt["@I0@"].birth

        expected = f"ANOMALY: US35: Name: {name}, Individual: ID {id}, born 30 days ago! Birthday: {birth}\n" 
        
        actual = GedcomFile.US35_list_recent_births(self.gedcom)

        self.assertEqual(expected, actual)


    def test_US35_0days(self):
        GedcomFile._individual_dt["@I5@"].birth =  datetime.date(self.today.year, self.today.month, self.today.day)       
        name = GedcomFile._individual_dt["@I5@"].name
        id = GedcomFile._individual_dt["@I5@"].id
        birth = GedcomFile._individual_dt["@I5@"].birth

        expected = f"ANOMALY: US35: Name: {name}, Individual: ID {id}, born 0 days ago! Birthday: {birth}\n"

        actual = GedcomFile.US35_list_recent_births(self.gedcom)

        self.assertEqual(expected, actual)


    def test_US35_31days(self):
        GedcomFile._individual_dt["@I11@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=31))
        expected = ""
        actual = GedcomFile.US35_list_recent_births(self.gedcom)
        self.assertEqual(expected, actual)


    def test_US35_neg1days(self):
        GedcomFile._individual_dt["@I7@"].birth = datetime.datetime.date(self.today + datetime.timedelta(days=1))
        expected = ""
        actual = GedcomFile.US35_list_recent_births(self.gedcom)
        self.assertEqual(expected, actual)



    def test_US34_spouseExactly2xAge(self):
        husband_age = 18
        wife_age = husband_age * 2
        GedcomFile._individual_dt["@I0@"].age = husband_age
        GedcomFile._individual_dt["@I1@"].age = wife_age
        
        wife_age = 35
        husband_age = wife_age * 2
        GedcomFile._individual_dt["@I2@"].age = husband_age
        GedcomFile._individual_dt["@I3@"].age = wife_age

        actual = GedcomFile.US34_list_large_age_differences(self.gedcom)

        expected = ""
        self.assertEqual(expected, actual)



    def test_US34_spouseGreater2xAge(self):
        husband_age = 18
        wife_age = (husband_age * 2) + 1
        GedcomFile._individual_dt["@I0@"].age = husband_age
        GedcomFile._individual_dt["@I1@"].age = wife_age
        husband_name = GedcomFile._individual_dt["@I0@"].name
        wife_name = GedcomFile._individual_dt["@I1@"].name
        family_id = next(iter(GedcomFile._individual_dt["@I0@"].fams)) # We only expect 1 family
        
        expected_1 = "ANOMALY: US34: FAMILY: %s Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d\n" \
            %(family_id, wife_name, "@I1@", wife_age, husband_name,  "@I0@", husband_age )

        wife_age = 35
        husband_age = (wife_age * 2) + 1
        GedcomFile._individual_dt["@I2@"].age = husband_age
        GedcomFile._individual_dt["@I3@"].age = wife_age
        husband_name = GedcomFile._individual_dt["@I2@"].name
        wife_name = GedcomFile._individual_dt["@I3@"].name
        family_id = next(iter(GedcomFile._individual_dt["@I2@"].fams)) # We only expect 1 family

        expected_2 = "ANOMALY: US34: FAMILY: %s Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d\n" \
            %(family_id, husband_name, "@I2@", husband_age, wife_name,  "@I3@", wife_age ) 

        expected = expected_1 + expected_2

        actual = GedcomFile.US34_list_large_age_differences(self.gedcom)

        self.assertEqual(expected, actual)


    def test_US34_spouseNegAge(self):
        husband_age = -18
        wife_age = -8
        GedcomFile._individual_dt["@I0@"].age = husband_age
        GedcomFile._individual_dt["@I1@"].age = wife_age

        wife_age = -35
        husband_age = -17
        GedcomFile._individual_dt["@I2@"].age = husband_age
        GedcomFile._individual_dt["@I3@"].age = wife_age

        expected = ""
        actual = GedcomFile.US34_list_large_age_differences(self.gedcom)

        self.assertEqual(expected, actual)
        

    def test_US30_all_people_living_and_married(self) -> None:
        '''Tests that the method correctly identifies all individuals, by ID and name, that are alive and married.
        '''
        # The initial unittest setup declares all 12 individuals to be living and married. Therefore, we are going to
        # override a few as deceased, and a few as unmarried.
        GedcomFile._individual_dt["@I0@"].living = False
        GedcomFile._individual_dt["@I8@"].living = False
        GedcomFile._individual_dt["@I3@"].fams = set()
        GedcomFile._individual_dt["@I11@"].fams = set()

        GedcomFile.parse_individuals_based_on_living_and_marital_details(self.gedcom)
        
        result: Dict[str, str] = GedcomFile._individuals_living_and_married

        expected = dict()
        for individual in GedcomFile._individual_dt.values():
            if individual.id in "@I0@ @I8@ @I3@ @I11@":
                continue
            else:
                expected[individual.id] = individual.name

        self.assertEqual(result, expected)

    def test_US04_Marriage_before_divorce(self):
        # Family 0: Divorce before marriage by 1 day
        GedcomFile._family_dt["@F_test0"].marriage_date = datetime.date(1985,11,11)
        GedcomFile._family_dt["@F_test0"].divorce_date = datetime.date(1985,11,10)

        # Family 2: Normal (Divorce after Marriage by 1 day). No Error Expected
        GedcomFile._family_dt["@F_test1"].marriage_date = datetime.date(1985,11,10)
        GedcomFile._family_dt["@F_test1"].divorce_date = datetime.date(1985,12,10)     
   
        # Family 5: Normal (Divorce after Marriage by 60 years). No Error Expected
        GedcomFile._family_dt["@F_test2"].marriage_date = datetime.date(1940,11,10)
        GedcomFile._family_dt["@F_test2"].divorce_date = datetime.date(2000,11,10)   


        result = self.gedcom.US4_Marriage_before_divorce()
        expect = [
                  "ERROR:US04:FAMILY:<@F_test0> Divorce 1985-11-10 happens before marriage 1985-11-11 Husband: ID @I0@, Name Test Subject0  Wife: ID @I1@, Name Test Subject1" , 
                 ]
        self.assertEqual(result, expect)


    def test_US21_correct_gender_for_role(self):
        # Family 0: Wrong Husband Sex
        husband_id = GedcomFile._family_dt["@F_test0"].husband_id
        GedcomFile._individual_dt[husband_id].sex = "F"

        # Family 1: Wrong Wife Sex
        wife_id = GedcomFile._family_dt["@F_test1"].wife_id
        GedcomFile._individual_dt[wife_id].sex = "M"

        # Family 2: Invalid Wife Sex
        wife_id = GedcomFile._family_dt["@F_test2"].wife_id
        GedcomFile._individual_dt[wife_id].sex = "BAD VALUE"

        # Family 3: Invalid Husband Sex
        husband_id = GedcomFile._family_dt["@F_test3"].husband_id
        GedcomFile._individual_dt[husband_id].sex = ""

        # Family 4: Uninitialized Husband ID (No error expected)
        GedcomFile._family_dt["@F_test4"].husband_id = ""

        # Family 5: Uninitialized Wife ID (No Error expected)
        GedcomFile._family_dt["@F_test4"].wife_id = ""        

        result = self.gedcom.US21_correct_gender_for_role()
        expect = [
                  "ERROR: US21: FAMILY:<@F_test0> Incorrect sex for husband id: @I0@ name: Test Subject0 sex: F ",
                  "ERROR: US21: FAMILY:<@F_test1> Incorrect sex for wife id: @I3@ name: Test Subject3 sex: M ",
                  "ERROR: US21: FAMILY:<@F_test2> Incorrect sex for wife id: @I5@ name: Test Subject5 sex: BAD VALUE ",
                  "ERROR: US21: FAMILY:<@F_test3> Incorrect sex for husband id: @I6@ name: Test Subject6 sex:  ",
                 ]
        self.assertEqual(result, expect)


    def test_US31_all_people_living_over_thirty_and_never_married(self) -> None:
        '''Tests that the method correctly identifies all individuals, by ID and name, that are alive
            over 30 yrs old, and have never been married.
        '''
        # The initial unittest setup declares all 12 individuals to be living and married. Therefore, we are going to
        # override a few as not married and over 30.
        # Force @I8@ and @I3@ to both be over 30 and never married. 
        GedcomFile._individual_dt["@I8@"].age = 31
        GedcomFile._individual_dt["@I8@"].fams = set() # Not married

        GedcomFile._individual_dt["@I3@"].age = 50
        GedcomFile._individual_dt["@I3@"].fams = set() # Not married

        GedcomFile._individual_dt["@I11@"].age = 29  # Married in initial setup

        GedcomFile._individual_dt["@I0@"].age = 30 
        GedcomFile._individual_dt["@I0@"].fams = set() # Not married

        GedcomFile.parse_individuals_based_on_living_and_marital_details(self.gedcom)
        
        result: Dict[str, str] = GedcomFile._individuals_living_over_thirty_and_never_married

        expected = dict()
        expected["@I8@"] = GedcomFile._individual_dt["@I8@"].name
        expected["@I3@"] = GedcomFile._individual_dt["@I3@"].name       

        self.assertEqual(result, expected)



    def test_US06(self):

        # Define case where the error won't happen (Death 1 day after divorce)
        w_id = GedcomFile._family_dt["@F_test1"].wife_id
        GedcomFile._individual_dt[w_id].death_date = datetime.date(1985,11,11)
        GedcomFile._family_dt["@F_test1"].divorce_date = datetime.date(1985,11,10)

        # Define case where error won't happen (Death 1 year after divorce)
        h_id = GedcomFile._family_dt["@F_test2"].husband_id
        GedcomFile._individual_dt[h_id].death_date = datetime.date(2005,9,1)
        GedcomFile._family_dt["@F_test2"].divorce_date = datetime.date(2004,9,1)

        # Define a case where the error will happen (Death 1 day before divorce)
        h_id = GedcomFile._family_dt["@F_test0"].husband_id
        w_id = GedcomFile._family_dt["@F_test0"].wife_id
        h_name = GedcomFile._family_dt["@F_test0"].husband_name
        w_name = GedcomFile._family_dt["@F_test0"].wife_name

        GedcomFile._individual_dt[w_id].death_date = datetime.date(1985,11,9)
        GedcomFile._family_dt["@F_test0"].divorce_date = datetime.date(1985,11,10)
        
        result = GedcomFile.US06_divorce_before_death(self.gedcom)

        expect = [
                   f"ERROR: US06: family:@F_test0: Husband ID: {h_id} Husband Name: {h_name} Divorced 1985-11-10 after wife's death:  ID: {w_id} Name: {w_name} death date: 1985-11-09"
                 ]
        self.assertEqual(expect, result)
        
        
    def test_US03(self):
        GedcomFile._individual_dt["@I11@"].death_date = datetime.date(2000,4,13)
        GedcomFile._individual_dt["@I11@"].birth = datetime.date(2000,4,14)
        name = GedcomFile._individual_dt["@I11@"].name
        result = GedcomFile.US03_birth_death(self.gedcom)

        expect = [ 
                  f"ERROR: US03: Individual ID: @I11@ Name: {name} has death date 2000-04-13 before birth 2000-04-14"
                 ]

        self.assertEqual(expect, result)

    def test_US07(self):
        #Exactly 150 Years old and Alive (Error Expected)
        GedcomFile._individual_dt["@I11@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*150))
        GedcomFile._individual_dt["@I11@"].death_date = 'NA'
        GedcomFile._individual_dt["@I11@"].living = True
        GedcomFile._individual_dt["@I11@"].setAge()
        name_11 = GedcomFile._individual_dt["@I11@"].name

        #150 Years old + 1 day and Alive (Error Expected)
        GedcomFile._individual_dt["@I10@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*150 + 1))
        GedcomFile._individual_dt["@I10@"].death_date = 'NA'
        GedcomFile._individual_dt["@I10@"].living = True
        GedcomFile._individual_dt["@I10@"].setAge()
        name_10 = GedcomFile._individual_dt["@I10@"].name

        # 150 Years old minus 1 Day and Alive (No error expected)
        GedcomFile._individual_dt["@I9@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*150 - 1))
        GedcomFile._individual_dt["@I9@"].death_date = 'NA'
        GedcomFile._individual_dt["@I9@"].living = True
        GedcomFile._individual_dt["@I9@"].setAge()

        result = GedcomFile.US07_Death150(self.gedcom)
        expect = [
                  f"ERROR: US07: Individual ID: @I10@ Name: {name_10} is more more than 150 years old!",
                  f"ERROR: US07: Individual ID: @I11@ Name: {name_11} is more more than 150 years old!",

                 ]
        self.assertEqual(expect, result)

    def test_US12(self):

        # Mother is exactly 60 years older than child (error expected)
        GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        GedcomFile._family_dt["@F_test0"].children = set(["@I2@"])

        GedcomFile._individual_dt["@I0@"].birth = datetime.date(1940,4,19)
        GedcomFile._individual_dt["@I0@"].setAge()
        GedcomFile._individual_dt["@I1@"].birth = datetime.date(1940,4,19)
        GedcomFile._individual_dt["@I1@"].setAge()
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(2000,4,19)
        GedcomFile._individual_dt["@I2@"].setAge()

        result = GedcomFile.US12_Mother_Father_older(self.gedcom)
        self.assertEqual({'@F_test0'}, result)

        # Mother is (59) older than child (no error expected)
        GedcomFile._individual_dt["@I0@"].birth = datetime.date(1940,4,19)
        GedcomFile._individual_dt["@I0@"].setAge()
        GedcomFile._individual_dt["@I1@"].birth = datetime.date(1941,4,19)
        GedcomFile._individual_dt["@I1@"].setAge()
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(2000,4,19)
        GedcomFile._individual_dt["@I2@"].setAge()


        result = GedcomFile.US12_Mother_Father_older(self.gedcom)
        self.assertEqual(set(), result)


        # Father is exactly 80 years older than child (error expected)
        GedcomFile._individual_dt["@I0@"].birth = datetime.date(1920,4,19)
        GedcomFile._individual_dt["@I0@"].setAge()
        GedcomFile._individual_dt["@I1@"].birth = datetime.date(1941,4,19)
        GedcomFile._individual_dt["@I1@"].setAge()
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(2000,4,19)
        GedcomFile._individual_dt["@I2@"].setAge()

        result = GedcomFile.US12_Mother_Father_older(self.gedcom)
        self.assertEqual({'@F_test0'}, result)


        # Father is (79) older than child (no error expected)
        GedcomFile._individual_dt["@I0@"].birth = datetime.date(1921,4,19)
        GedcomFile._individual_dt["@I0@"].setAge()
        GedcomFile._individual_dt["@I1@"].birth = datetime.date(1941,4,19)
        GedcomFile._individual_dt["@I1@"].setAge()
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(2000,4,19)
        GedcomFile._individual_dt["@I2@"].setAge()


        result = GedcomFile.US12_Mother_Father_older(self.gedcom)
        self.assertEqual(set(), result)

    def test_US16(self):
        
        # Family1 same name
        GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        GedcomFile._family_dt["@F_test0"].children = set(["@I2@"])

        GedcomFile._individual_dt["@I0@"].name = 'aran /kel/ '
        GedcomFile._individual_dt["@I1@"].name = 'molly /kel/ '
        GedcomFile._individual_dt["@I2@"].name = 'jo /kel/ '

        # Family2 differennt name
        GedcomFile._family_dt["@F_test1"].husband_id = "@I4@"
        GedcomFile._family_dt["@F_test1"].wife_id =    "@I5@"
        GedcomFile._family_dt["@F_test1"].children = set(["@I6@"])

        GedcomFile._individual_dt["@I4@"].name = 'yash /smith/ '
        GedcomFile._individual_dt["@I5@"].name = 'ind /smith/ '
        GedcomFile._individual_dt["@I6@"].name = 'shree /pal/ '

        result = GedcomFile.US16_male(self.gedcom)
        self.assertEqual(["@F_test1"], result)

    def test_US19(self):

        #GrandParents
        GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        GedcomFile._family_dt["@F_test0"].children = set({"@I2@","@I5@"})
        GedcomFile._individual_dt["@I0@"].fams = set(["@F_test0"])
        GedcomFile._individual_dt["@I1@"].fams = set(["@F_test0"])
        

        #Boys Parents
        GedcomFile._family_dt["@F_test1"].husband_id = "@I2@"
        GedcomFile._family_dt["@F_test1"].wife_id =    "@I3@"
        GedcomFile._family_dt["@F_test1"].children = set({"@I10@"})
        GedcomFile._individual_dt["@I2@"].fams = set(["@F_test1"])
        GedcomFile._individual_dt["@I3@"].fams = set(["@F_test1"])
        GedcomFile._individual_dt["@I2@"].famc = set(["@F_test0"])

        #Girls Parents
        GedcomFile._family_dt["@F_test2"].husband_id = "@I4@"
        GedcomFile._family_dt["@F_test2"].wife_id =    "@I5@"
        GedcomFile._family_dt["@F_test2"].children = set({"@I11@"})
        GedcomFile._individual_dt["@I4@"].fams = set(["@F_test2"])
        GedcomFile._individual_dt["@I5@"].fams = set(["@F_test2"])
        GedcomFile._individual_dt["@I5@"].famc = set(["@F_test0"])

        #fam3
        GedcomFile._family_dt["@F_test5"].husband_id = "@I10@"
        GedcomFile._family_dt["@F_test5"].wife_id =    "@I11@"
        GedcomFile._individual_dt["@I10@"].fams = set(["@F_test5"])
        GedcomFile._individual_dt["@I11@"].fams = set(["@F_test5"])
        GedcomFile._individual_dt["@I10@"].famc = set(["@F_test1"])
        GedcomFile._individual_dt["@I11@"].famc = set(["@F_test2"])

        result = GedcomFile.US19_married_first_cousins(self.gedcom)
        self.assertEqual(["@F_test5"],result)


    





    def test_US36_recently_deceased(self):
        # Initialize Inputs 
        GedcomFile._individual_dt["@I0@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=29))
        GedcomFile._individual_dt["@I1@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=30))
        GedcomFile._individual_dt["@I2@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=31))
        GedcomFile._individual_dt["@I3@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=0))
        GedcomFile._individual_dt["@I4@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=365*40))
        GedcomFile._individual_dt["@I5@"].death_date =  datetime.datetime.date(self.today + datetime.timedelta(days=1))
        GedcomFile._individual_dt["@I6@"].death_date =  datetime.datetime.date(self.today + datetime.timedelta(days=365*40))
        GedcomFile._individual_dt["@I7@"].death_date =  ""
        GedcomFile._individual_dt["@I8@"].death_date =  "NA"
        GedcomFile._individual_dt["@I9@"].death_date =  "28 JAN 1940"

        #Initialize expected results. 
        # We expect only the death dates that fall within the past 30 days. Therefore, @I0@, @I1@, and @I3@
        expected_results = list()
        expected_results.append(["@I0@", GedcomFile._individual_dt["@I0@"].name, GedcomFile._individual_dt["@I0@"].death_date])
        expected_results.append(["@I1@", GedcomFile._individual_dt["@I1@"].name, GedcomFile._individual_dt["@I1@"].death_date])
        expected_results.append(["@I3@", GedcomFile._individual_dt["@I3@"].name, GedcomFile._individual_dt["@I3@"].death_date])

        #Invoke method under test 
        actual = self.gedcom.find_deceased_within30days()
        
        for entry in expected_results:
            self.assertEqual(True, entry in actual)

        expected_pt: PrettyTable = PrettyTable(field_names=['ID', 'Name', "Death Date"])
        
        for entry in expected_results:
            expected_pt.add_row(entry)
        expected_pt.sortby = "Death Date"
        
        actual_pt = self.gedcom.US36_list_recent_deaths()

        self.assertEqual(expected_pt.get_string(), actual_pt.get_string())


    def US37_recent_survivors_3Generations(self, divorced):
        # Initialize Inputs 
        # Define the following 3-generation Family:
        # @F_Test0: Husband:@I0@  Wife: @I1@  children: @I2@.  In this family, Husband is deceased recently.
        #   @F_Test1: Husband:@I2@  Wife: @I3@  children: @I4@
        #       @F_Test2: Husband:@I4@  Wife: @I5@  children: @I6@ @I8@ @I10@. In this family, @I10@ is deceased.
        #
        # Therefore Descendants of @I0@ are Children (@I2@), grand children (@I4@), and great-grand-children (@I6@, @I8@, @I10@) 
        #
        GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        GedcomFile._family_dt["@F_test0"].children = set({"@I2@"})

        GedcomFile._family_dt["@F_test1"].husband_id = "@I2@"
        GedcomFile._family_dt["@F_test1"].wife_id =    "@I3@"
        GedcomFile._family_dt["@F_test1"].children = set({"@I4@"})

        GedcomFile._family_dt["@F_test2"].husband_id = "@I4@"
        GedcomFile._family_dt["@F_test2"].wife_id =    "@I5@"
        GedcomFile._family_dt["@F_test2"].children = set({"@I6@", "@I8@", "@I10@"})

        GedcomFile._individual_dt["@I0@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=29))
        GedcomFile._individual_dt["@I0@"].living = False
        GedcomFile._individual_dt["@I10@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=31))
        GedcomFile._individual_dt["@I10@"].living = False

        if divorced:
            GedcomFile._family_dt["@F_test0"].divorce_date = GedcomFile._individual_dt["@I0@"].death_date - datetime.timedelta(days=500)

        #Initialize expected results. 
        # Define ALL Descendants.
        expected_descendants = ["@I2@", "@I4@", "@I6@", "@I8@", "@I10@"]

        #Invoke method under test 
        actual_descendants = list()
        self.gedcom.walk_down_family_tree("@F_test0", actual_descendants)

        for entry in expected_descendants:
            self.assertEqual(True, entry in actual_descendants)


        # OK, now let's test the pretty table of recent survivors. We expect the same individuals, except for @I10@ which is deceased.
        expected_pt = PrettyTable(field_names=['Recently Deceased ID', 'Recently Deceased Name', 'Surviver ID', 'Surviver Name', "Relationship to Deceased"])

        # Start by adding the spouse:
        if divorced:
            expected_pt.add_row([
                                    GedcomFile._individual_dt["@I0@"].id,
                                    GedcomFile._individual_dt["@I0@"].name,
                                    GedcomFile._individual_dt["@I1@"].id,
                                    GedcomFile._individual_dt["@I1@"].name,
                                    "Ex-Spouse"
                            ])
        else:
            expected_pt.add_row([
                                    GedcomFile._individual_dt["@I0@"].id,
                                    GedcomFile._individual_dt["@I0@"].name,
                                    GedcomFile._individual_dt["@I1@"].id,
                                    GedcomFile._individual_dt["@I1@"].name,
                                    "Spouse"
                            ])
        for entry in expected_descendants:
            if entry == "@I10@":
                continue
            expected_pt.add_row([
                                 GedcomFile._individual_dt["@I0@"].id,
                                 GedcomFile._individual_dt["@I0@"].name,
                                 GedcomFile._individual_dt[entry].id,
                                 GedcomFile._individual_dt[entry].name,
                                 "Descendant"
                                ])
        expected_pt.sortby = "Recently Deceased ID"


        actual_pt = self.gedcom.US37_list_recent_survivors()

        self.assertEqual(expected_pt.get_string(), actual_pt.get_string())



    def test_US37_recent_survivors_3Generations_married(self):
        self.US37_recent_survivors_3Generations(False)

    def test_US37_recent_survivors_3Generations_divorced(self):
        self.US37_recent_survivors_3Generations(True)



    def test_US37_recent_survivors_multiple_deaths(self):
        # Initialize Inputs 
        # Define the following 3-generation Family:
        # @F_Test0: Husband:@I0@  Wife: @I1@  children: @I2@.  In this family, Husband is deceased recently.
        #   @F_Test1: Husband:@I2@  Wife: @I3@  children: @I4@. In this family, Wife is deceased recently.
        #       @F_Test2: Husband:@I4@  Wife: @I5@  children: @I6@ @I8@ @I10@. In this family, @I10@ is deceased.
        #
        # Therefore Descendants of @I0@ are Children (@I2@), grand children (@I4@), and great-grand-children (@I6@, @I8@, @I10@) 
        #
        GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        GedcomFile._family_dt["@F_test0"].children = set(["@I2@"])

        GedcomFile._family_dt["@F_test1"].husband_id = "@I2@"
        GedcomFile._family_dt["@F_test1"].wife_id =    "@I3@"
        GedcomFile._family_dt["@F_test1"].children = set(["@I4@"])

        GedcomFile._family_dt["@F_test2"].husband_id = "@I4@"
        GedcomFile._family_dt["@F_test2"].wife_id =    "@I5@"
        GedcomFile._family_dt["@F_test2"].children = set(["@I6@", "@I8@", "@I10@"])

        GedcomFile._individual_dt["@I0@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=29))
        GedcomFile._individual_dt["@I0@"].living = False
        GedcomFile._individual_dt["@I3@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=1))
        GedcomFile._individual_dt["@I3@"].living = False
        GedcomFile._individual_dt["@I10@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=31))
        GedcomFile._individual_dt["@I10@"].living = False

        # Test the descendants method for the 1st family who had a recent death.
        expected_descendants_1 = ["@I2@", "@I4@", "@I6@", "@I8@", "@I10@"]


        #Invoke method under test 
        actual_descendants_1 = list()
        self.gedcom.walk_down_family_tree("@F_test0", actual_descendants_1)

        for entry in expected_descendants_1:
            self.assertEqual(True, entry in actual_descendants_1)


        # Test the descendants method for the 2nd family who had a recent death
        expected_descendants_2 = ["@I4@", "@I6@", "@I8@", "@I10@"]

        #Invoke method under test 
        actual_descendants_2 = list()
        self.gedcom.walk_down_family_tree("@F_test1", actual_descendants_2)

        for entry in expected_descendants_2:
            self.assertEqual(True, entry in actual_descendants_2)

        # OK, now let's test the pretty table of recent survivors. We expect the same individuals, except for @I10@ which is deceased.
        expected_pt = PrettyTable(field_names=['Recently Deceased ID', 'Recently Deceased Name', 'Surviver ID', 'Surviver Name', "Relationship to Deceased"])

        # Handle first family. Start by adding the spouse:
        expected_pt.add_row([
                                GedcomFile._individual_dt["@I0@"].id,
                                GedcomFile._individual_dt["@I0@"].name,
                                GedcomFile._individual_dt["@I1@"].id,
                                GedcomFile._individual_dt["@I1@"].name,
                                "Spouse"
                            ])
        for entry in expected_descendants_1:
            if entry == "@I10@":
                continue
            expected_pt.add_row([
                                 GedcomFile._individual_dt["@I0@"].id,
                                 GedcomFile._individual_dt["@I0@"].name,
                                 GedcomFile._individual_dt[entry].id,
                                 GedcomFile._individual_dt[entry].name,
                                 "Descendant"
                                ])

        
        # Handle second family. Start by adding the spouse
        expected_pt.add_row([
                                GedcomFile._individual_dt["@I3@"].id,
                                GedcomFile._individual_dt["@I3@"].name,
                                GedcomFile._individual_dt["@I2@"].id,
                                GedcomFile._individual_dt["@I2@"].name,
                                "Spouse"
                            ])
        for entry in expected_descendants_2:
            if entry == "@I10@":
                continue
            expected_pt.add_row([
                                 GedcomFile._individual_dt["@I3@"].id,
                                 GedcomFile._individual_dt["@I3@"].name,
                                 GedcomFile._individual_dt[entry].id,
                                 GedcomFile._individual_dt[entry].name,
                                 "Descendant"
                                ])

        expected_pt.sortby = "Recently Deceased ID"

        actual_pt = self.gedcom.US37_list_recent_survivors()

        self.assertEqual(expected_pt.get_string(), actual_pt.get_string())


    def test_US22_uni_ids_indi_fam(self):
        # For this test we are not depending on the dictionaries created as part of the test setup, since we're
        # partially testing the parser. So, clear the containers.
        self.gedcom._individual_dt.clear()
        self.gedcom._family_dt.clear()
        self.gedcom._individuals_living_and_married.clear()
        self.gedcom._individuals_living_over_thirty_and_never_married.clear()
        self.gedcom._validated_list.clear()

        # Create two different families with unique individuals, but with the same exact Family ID ('@EA1@')
                                     #Level,  Tag,    Argument
        
        # Family 1:
        self.gedcom._validated_list.append([0, 'INDI',  '@E0@'          ])
        self.gedcom._validated_list.append([1, 'NAME',  'Radi /Alofi/'  ])
        self.gedcom._validated_list.append([1, 'SEX',   'F'             ])
        self.gedcom._validated_list.append([1, 'BIRT',  ''              ])
        self.gedcom._validated_list.append([2, 'DATE',  '10 MAR 2000'   ])
        self.gedcom._validated_list.append([1, 'FAMS',  '@EA1@'         ])

        self.gedcom._validated_list.append([0, 'INDI',  '@E1@'          ])
        self.gedcom._validated_list.append([1, 'NAME',  'Roaa /Alofi/'  ])
        self.gedcom._validated_list.append([1, 'SEX',   'F'             ])
        self.gedcom._validated_list.append([1, 'BIRT',  ''              ])
        self.gedcom._validated_list.append([2, 'DATE',  '10 MAR 2000'   ])
        self.gedcom._validated_list.append([1, 'FAMS',  '@EA1@'         ])

        self.gedcom._validated_list.append([0, 'FAM',   '@EA1@'         ])
        self.gedcom._validated_list.append([1, 'HUSB',  '@E0@'          ])
        self.gedcom._validated_list.append([1, 'WIFE',  '@E1@'          ])
        self.gedcom._validated_list.append([1, 'MARR',  ''              ])
        self.gedcom._validated_list.append([2, 'DATE',  '1 APR 2020'    ])

        # Family 2: The Duplicate Family
        self.gedcom._validated_list.append([0, 'INDI',  '@E2@'          ])
        self.gedcom._validated_list.append([1, 'NAME',  'Radi /Alofi/'  ])
        self.gedcom._validated_list.append([1, 'SEX',   'F'             ])
        self.gedcom._validated_list.append([1, 'BIRT',  ''              ])
        self.gedcom._validated_list.append([2, 'DATE',  '10 MAR 2000'   ])
        self.gedcom._validated_list.append([1, 'FAMS',  '@EA1@'         ])

        self.gedcom._validated_list.append([0, 'INDI', '@E3@'           ])
        self.gedcom._validated_list.append([1, 'NAME', 'Roaa /Alofi/'   ])
        self.gedcom._validated_list.append([1, 'SEX',  'F'              ])
        self.gedcom._validated_list.append([1, 'BIRT', ''               ])
        self.gedcom._validated_list.append([2, 'DATE', '10 MAR 2000'    ])
        self.gedcom._validated_list.append([1, 'FAMS', '@EA1@'          ])

        self.gedcom._validated_list.append([0, 'FAM',  '@EA1@'          ])
        self.gedcom._validated_list.append([1, 'HUSB', '@E2@'           ])
        self.gedcom._validated_list.append([1, 'WIFE', '@E3@'           ])
        self.gedcom._validated_list.append([1, 'MARR', ''               ])
        self.gedcom._validated_list.append([2, 'DATE', '1 APR 2019'     ])

        # Add a duplicate individual with the exact same ID
        self.gedcom._validated_list.append([0, 'INDI',  '@E2@'          ])
        self.gedcom._validated_list.append([1, 'NAME',  'Jess /Soares/' ])
        self.gedcom._validated_list.append([1, 'SEX',   'F'             ])
        self.gedcom._validated_list.append([1, 'BIRT',  ''              ])
        self.gedcom._validated_list.append([2, 'DATE',  '1 JAN 2004'    ])


        # Kick off the parser to create the individuals and families, and to detect the duplicates.
        self.gedcom.parse_validated_gedcom()

        # Expect the Duplicate family
        expect = ["ERROR: US22: Family ID: @EA1@ with wife ID: @E3@ and husband ID: @E2@ "+\
                "is a duplicate of Family ID: @EA1@ with wife ID: @E1@ and husband id: @E0@"]
 
        # Expect the duplicate individual
        expect.append(f"ERROR: US22: Individual ID: @E2@ with name Jess /Soares/ is a duplicate of individual ID @E2@ "+\
                     f"with name Radi /Alofi/")

        # Call method under test
        result = GedcomFile.US22_uni_ids_indi_fam(self.gedcom)

        self.assertEqual(expect, result)
        



    def test_US23_uni_name_birth(self):
        # Rise an error if the both individuals have same name and birthdates 
        GedcomFile._individual_dt["@I5@"].name = "Safa /Alofi/"
        GedcomFile._individual_dt["@I5@"].birth =  datetime.date(1990,5,16)
        GedcomFile._individual_dt["@I6@"].name = "Safa /Alofi/"
        GedcomFile._individual_dt["@I6@"].birth =  datetime.date(1990,5,16)
        result = GedcomFile.US23_uni_name_birth(self.gedcom)
        expect = ["ERROR US23 Individuals ids @I5@ and name Safa /Alofi/ found duplicated name and birthdate", "ERROR US23 Individuals ids @I6@ and name Safa /Alofi/ found duplicated name and birthdate"] 
        self.assertEqual(expect, result)



    def test_US02_birth_before_marriage(self):
        # Family 0: birth of individual before their marriage by 1 day (Not possible, but not an error!)
        GedcomFile._family_dt["@F_test0"].marriage_date = datetime.date(1985,11,11)
        GedcomFile._individual_dt["@I0@"].birth = datetime.date(1985,11,10)

        # Family 2: birth of individual after their marriage by 1 day (Error Expected)
        GedcomFile._family_dt["@F_test1"].marriage_date = datetime.date(1985,11,11)
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(1985,11,12)
  
        result = GedcomFile.US2_birth_before_marriage(self.gedcom)
        expect = ["ERROR: US2: FAMILY: @F_test1"]
        self.assertEqual(expect, result)


    def test_US5_marriage_before_death(self):
        # Family 0: marriage occurs after death of husband by 1 day (Error Expected)
        GedcomFile._family_dt["@F_test0"].marriage_date = datetime.date(1985,11,11)
        id = GedcomFile._family_dt["@F_test0"].husband_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,10)
        GedcomFile._individual_dt[id].living = False
        id = GedcomFile._family_dt["@F_test0"].wife_id
        GedcomFile._individual_dt[id].death_date = "NA"
        GedcomFile._individual_dt[id].living = True

        # Family 1: marriage occurs after death of wife by 1 day (Error Expected)
        GedcomFile._family_dt["@F_test1"].marriage_date = datetime.date(1985,11,11)
        id = GedcomFile._family_dt["@F_test1"].wife_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,10)
        GedcomFile._individual_dt[id].living = False
        id = GedcomFile._family_dt["@F_test1"].husband_id
        GedcomFile._individual_dt[id].death_date = "NA"
        GedcomFile._individual_dt[id].living = True

        # Family 2: marriage occurs before death of husband by 1 day (no error expected)
        GedcomFile._family_dt["@F_test2"].marriage_date = datetime.date(1985,11,11)
        id = GedcomFile._family_dt["@F_test2"].husband_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,12)
        GedcomFile._individual_dt[id].living = False
        id = GedcomFile._family_dt["@F_test2"].wife_id
        GedcomFile._individual_dt[id].death_date = "NA"
        GedcomFile._individual_dt[id].living = True

        # Family 3: marriage occurs before death of wife by 1 day (no error expected)
        GedcomFile._family_dt["@F_test3"].marriage_date = datetime.date(1985,11,11)
        id = GedcomFile._family_dt["@F_test3"].wife_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,12)
        GedcomFile._individual_dt[id].living = False
        id = GedcomFile._family_dt["@F_test3"].husband_id
        GedcomFile._individual_dt[id].death_date = "NA"
        GedcomFile._individual_dt[id].living = True

        # Family 4: marriage occurs after death of husband and wife by 1 day (Error Expected twice!)
        GedcomFile._family_dt["@F_test4"].marriage_date = datetime.date(1985,11,11)
        id = GedcomFile._family_dt["@F_test4"].wife_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,10)
        GedcomFile._individual_dt[id].living = False
        id = GedcomFile._family_dt["@F_test4"].husband_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,10)
        GedcomFile._individual_dt[id].living = False

        # Family 5: marriage occurs before death of husband and wife by 1 day (No Error Expected)
        GedcomFile._family_dt["@F_test5"].marriage_date = datetime.date(1985,11,11)
        id = GedcomFile._family_dt["@F_test5"].wife_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,12)
        GedcomFile._individual_dt[id].living = False
        id = GedcomFile._family_dt["@F_test5"].husband_id
        GedcomFile._individual_dt[id].death_date = datetime.date(1985,11,12)
        GedcomFile._individual_dt[id].living = False

        result = GedcomFile.US5_marriage_before_death(self.gedcom)
        expect = [
                     "ERROR: US5: FAMILY:@F_test0", 
                     "ERROR: US5: FAMILY:@F_test1",
                     "ERROR: US5: FAMILY:@F_test4",
                     "ERROR: US5: FAMILY:@F_test4",
                 ]
        self.assertEqual(expect, result)

        
    def test_US28_order_siblings_by_age(self) -> None:
        '''tests that the method implemented for US28 correctly orders sibling for every family: from Oldest to Youngest'''

        # Define 1st family with 3 children of different ages.
        GedcomFile._family_dt["@F_test0"].children = set(["@I3@", "@I4@", "@I6@"])
        GedcomFile._individual_dt["@I3@"].age = 30
        GedcomFile._individual_dt["@I3@"].famc = set(["@F_test0"])
        GedcomFile._individual_dt["@I4@"].age = 18
        GedcomFile._individual_dt["@I4@"].famc = set(["@F_test0"])
        GedcomFile._individual_dt["@I6@"].age = 26
        GedcomFile._individual_dt["@I6@"].famc = set(["@F_test0"])

        # Define a second fammily with 3 children of different ages.
        GedcomFile._family_dt["@F_test1"].children = set(["@I2@", "@I5@", "@I7@"])
        GedcomFile._individual_dt["@I2@"].age = 35
        GedcomFile._individual_dt["@I2@"].famc = set(["@F_test1"])
        GedcomFile._individual_dt["@I5@"].age = 24
        GedcomFile._individual_dt["@I5@"].famc = set(["@F_test1"])
        GedcomFile._individual_dt["@I7@"].age = 22
        GedcomFile._individual_dt["@I7@"].famc = set(["@F_test1"])        
        
        result: List[List[str]] = GedcomFile.US28_list_all_siblings_from_oldest_to_youngest(self.gedcom)

        expected: List[List[str]] = [
                                    ['@F_test0', '@I3@', GedcomFile._individual_dt["@I3@"].name, 30],
                                    ['@F_test0', '@I6@', GedcomFile._individual_dt["@I6@"].name, 26],
                                    ['@F_test0', '@I4@', GedcomFile._individual_dt["@I4@"].name, 18],
                                    ['@F_test1', '@I2@', GedcomFile._individual_dt["@I2@"].name, 35],
                                    ['@F_test1', '@I5@', GedcomFile._individual_dt["@I5@"].name, 24],
                                    ['@F_test1', '@I7@', GedcomFile._individual_dt["@I7@"].name, 22],
                                    ]
                                   

        self.assertEqual(result, expected)

    def test_US27_setAge(self) -> None:
        '''tests that the method implemented to set an individual's age correctly calculates age'''

        person1: Individual = Individual()
        person1.preceding_tag_related_to_date: str = 'BIRT'
        person1.process_individual_record_date_tag('20 MAR 1991')

        person2: Individual = Individual()
        person2.preceding_tag_related_to_date: str = 'BIRT'
        person2.process_individual_record_date_tag('6 JUN 1925')  
        person2.preceding_tag_related_to_date: str = 'DEAT'
        person2.process_individual_record_date_tag('28 JUN 2020')

        person3: Individual = Individual()
        person3.preceding_tag_related_to_date: str = 'BIRT'
        person3.process_individual_record_date_tag('28 JUN 2020')

        person4: Individual = Individual()
        person4.preceding_tag_related_to_date: str = 'BIRT'
        person4.process_individual_record_date_tag('29 FEB 2000')

        result: List[str] = [person1.age, person2.age, person3.age, person4.age]
        expected: List[str] = [29, 95, 0, 20]

        self.assertEqual(result, expected)




    def test_US32_Multiple_Births(self) -> None:
        # Define 1st family with 5 children. 3 are multiple birth, 2 are not.
        GedcomFile._family_dt["@F_test0"].children = set(["@I3@", "@I4@", "@I6@", "@I8@", "@I10@"])

        # These 3 are born one day apart (part of same multiple birth)
        GedcomFile._individual_dt["@I3@"].birth = datetime.date(1980, 1, 1)
        GedcomFile._individual_dt["@I4@"].birth = datetime.date(1979, 12, 31)
        GedcomFile._individual_dt["@I6@"].birth = datetime.date(1980, 1, 1)

        # These 2 are not part of multiple birth
        GedcomFile._individual_dt["@I8@"].birth = datetime.date(1985, 1, 1)
        GedcomFile._individual_dt["@I10@"].birth = datetime.date(1986, 1, 1)

        # Make sure each child is actually part of the test family.
        for child in GedcomFile._family_dt["@F_test0"].children:
            GedcomFile._individual_dt[child].living = True
            GedcomFile._individual_dt[child].setAge()
            GedcomFile._individual_dt[child].famc = set(["@F_test0"])    


        # Define 2nd family with 3 children. 2 are multiple birth, 1 is not.
        GedcomFile._family_dt["@F_test1"].children = set(["@I2@", "@I5@", "@I7@"])

        # These 2 are born one day apart (part of same multiple birth)
        GedcomFile._individual_dt["@I2@"].birth = datetime.date(1980, 1, 1)
        GedcomFile._individual_dt["@I5@"].birth = datetime.date(1980, 1, 2)

        # This one is not
        GedcomFile._individual_dt["@I7@"].birth = datetime.date(1985, 1, 1)

        # Make sure each child is actually part of the test family.
        for child in GedcomFile._family_dt["@F_test1"].children:
            GedcomFile._individual_dt[child].living = True
            GedcomFile._individual_dt[child].setAge()
            GedcomFile._individual_dt[child].famc = set(["@F_test1"]) 


        expected_pt: PrettyTable = PrettyTable(field_names = ['Family ID', 'Child ID', 'Child Name', 'Child Birth Date'])
        expected_pt.add_row([set(["@F_test0"]), "@I3@", GedcomFile._individual_dt["@I3@"].name, GedcomFile._individual_dt["@I3@"].birth])
        expected_pt.add_row([set(["@F_test0"]), "@I4@", GedcomFile._individual_dt["@I4@"].name, GedcomFile._individual_dt["@I4@"].birth])
        expected_pt.add_row([set(["@F_test0"]), "@I6@", GedcomFile._individual_dt["@I6@"].name, GedcomFile._individual_dt["@I6@"].birth])
        expected_pt.add_row([set(["@F_test1"]), "@I2@", GedcomFile._individual_dt["@I2@"].name, GedcomFile._individual_dt["@I2@"].birth])
        expected_pt.add_row([set(["@F_test1"]), "@I5@", GedcomFile._individual_dt["@I5@"].name, GedcomFile._individual_dt["@I5@"].birth])


        actual = self.gedcom.US32_list_multiple_births()
        self.assertEqual(expected_pt.get_string(), actual.get_string())




    def test_US33_Orphans(self) -> None:
        # Define family with 3 children. Both parents are deceased
        GedcomFile._family_dt["@F_test0"].children = set(["@I2@", "@I5@", "@I7@"])
        GedcomFile._individual_dt["@I2@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*18))
        GedcomFile._individual_dt["@I5@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*17))
        GedcomFile._individual_dt["@I7@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*19))

        # Make sure each child is actually part of the test family.
        for child in GedcomFile._family_dt["@F_test0"].children:
            GedcomFile._individual_dt[child].setAge()
            GedcomFile._individual_dt[child].famc = set(["@F_test0"]) 

        father = GedcomFile._family_dt["@F_test0"].husband_id
        mother = GedcomFile._family_dt["@F_test0"].wife_id



        #####Test 1: Both parents deceased
        GedcomFile._individual_dt[father].living = False
        GedcomFile._individual_dt[mother].living = False
        expected_pt: PrettyTable = PrettyTable(field_names = ['Family ID (as child)', 'Individual ID', 'Name']) 
        expected_pt.add_row([set(["@F_test0"]), "@I5@", GedcomFile._individual_dt["@I5@"].name])

        actual = self.gedcom.US33_list_orphans()
        self.assertEqual(expected_pt.get_string(), actual.get_string())



         #####Test 2: Father is alive, mother is deceased
        GedcomFile._individual_dt[father].living = True
        GedcomFile._individual_dt[mother].living = False

        expected_pt: PrettyTable = PrettyTable(field_names = ['Family ID (as child)', 'Individual ID', 'Name']) 
        # We don't expect any entries in the table

        actual = self.gedcom.US33_list_orphans()
        self.assertEqual(expected_pt.get_string(), actual.get_string())



         #####Test 3: Father is deceased, mother is alive
        GedcomFile._individual_dt[father].living = False
        GedcomFile._individual_dt[mother].living = True

        expected_pt: PrettyTable = PrettyTable(field_names = ['Family ID (as child)', 'Individual ID', 'Name']) 
        # We don't expect any entries in the table
        
        actual = self.gedcom.US33_list_orphans()
        self.assertEqual(expected_pt.get_string(), actual.get_string())



         #####Test 4: both parents deceased, more than one sibling is younger than 18
        GedcomFile._individual_dt[father].living = False
        GedcomFile._individual_dt[mother].living = False
        GedcomFile._individual_dt["@I2@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*17))
        GedcomFile._individual_dt["@I5@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*16))
        GedcomFile._individual_dt["@I7@"].birth = datetime.datetime.date(self.today - datetime.timedelta(days=365*18))

        # Make sure each child is actually part of the test family.
        for child in GedcomFile._family_dt["@F_test0"].children:
            GedcomFile._individual_dt[child].setAge()
            GedcomFile._individual_dt[child].famc = set(["@F_test0"]) 

        expected_pt: PrettyTable = PrettyTable(field_names = ['Family ID (as child)', 'Individual ID', 'Name']) 
        expected_pt.add_row([set(["@F_test0"]), "@I5@", GedcomFile._individual_dt["@I5@"].name])
        expected_pt.add_row([set(["@F_test0"]), "@I2@", GedcomFile._individual_dt["@I2@"].name])
        expected_pt.sortby = 'Individual ID'
        actual = self.gedcom.US33_list_orphans()
        self.assertEqual(expected_pt.get_string(), actual.get_string())

    def test_US24_unique_families_by_spouses(self) -> None:
        '''tests that the method implemented for US24 highlight the case where more than one family has the same spouses and marriage date'''

        #Making @F_test1 and @F_test2 the same as @F_test0:
        GedcomFile._family_dt['@F_test1'].husband_name = 'Test Subject0'
        GedcomFile._family_dt['@F_test1'].wife_name = 'Test Subject1'
        GedcomFile._family_dt['@F_test1'].marriage_date = datetime.date(1930,1,1)

        GedcomFile._family_dt['@F_test2'].husband_name = 'Test Subject0'
        GedcomFile._family_dt['@F_test2'].wife_name = 'Test Subject1'
        GedcomFile._family_dt['@F_test2'].marriage_date = datetime.date(1930,1,1)

        #Making @F_test4 the same as @F_test3:
        GedcomFile._family_dt['@F_test4'].husband_name = 'Test Subject6'
        GedcomFile._family_dt['@F_test4'].wife_name = 'Test Subject7'
        GedcomFile._family_dt['@F_test4'].marriage_date = datetime.date(1960,4,4)
        
        result: List[str] = GedcomFile.US24_unique_families_by_spouses(self.gedcom)

        expected: List[str] = [
                f'ANOMALY: US24: Families @F_test0, @F_test1, @F_test2, have the same spouses and marriage date: Husband: Test Subject0, Wife: Test Subject1, Marriage Date: 1930-01-01',
                f'ANOMALY: US24: Families @F_test3, @F_test4, have the same spouses and marriage date: Husband: Test Subject6, Wife: Test Subject7, Marriage Date: 1960-04-04',
                
                ]

        self.assertEqual(result, expected)

    def test_US25_unique_first_names_in_families(self) -> None:
        '''tests that the method implemented for US25 highlights the case where more than one child has the same name and birth date in the same family'''

        #Setting individuals "@I1@" and "@I2@" to have same name and birth date as inividual "@I0@", and putting them all as children in family "@F_test0"
        GedcomFile._individual_dt['@I1@'].name = 'Test Subject0'
        GedcomFile._individual_dt['@I1@'].birth = datetime.date(1900,12,12)
        GedcomFile._individual_dt['@I2@'].name = 'Test Subject0'
        GedcomFile._individual_dt['@I2@'].birth = datetime.date(1900,12,12)
        GedcomFile._family_dt['@F_test0'].children = ({'@I0@', '@I1@', '@I2@'})

        #Setting individual "@I6@" to have same name and birth date as individual "@I5@", and putting them all as children in family "@F_test3"
        GedcomFile._individual_dt['@I6@'].name = 'Test Subject5'
        GedcomFile._individual_dt['@I6@'].birth = datetime.date(1920,7,7)
        GedcomFile._family_dt['@F_test3'].children = ({'@I5@', '@I6@'})

        result: List[str] = GedcomFile.US25_unique_first_names_in_families(self.gedcom)

        child_ids_for_fam0: Set[str] = ', '.join(GedcomFile._family_dt['@F_test0'].children)
        child_ids_for_fam3: Set[str] = ', '.join(GedcomFile._family_dt['@F_test3'].children)
        
        expected: List[str] = [
                f'ANOMALY: US25: Individuals {child_ids_for_fam0} from family @F_test0, have the same name and birth date: Name: Test Subject0, Birth Date: 1900-12-12',
                f'ANOMALY: US25: Individuals {child_ids_for_fam3} from family @F_test3, have the same name and birth date: Name: Test Subject5, Birth Date: 1920-07-07',

        ]

        self.assertEqual(result, expected)

    def test_US26_corresponding_entries_individuals(self) -> None:
        '''tests the case where family roles (spouse, child) specified in an individual record are not consistent with the corresponding entries in the 
            corresponding family record. If such a case is found, it is highlihgted as an error. 
        
        family roles in an individual record are specified as follows: spouse = "fams", child = "famc"
        '''
        #Clears tags to be used in test cases:
        for individuals in GedcomFile._individual_dt.values():
            individuals.fams: Set[str] = set()
            individuals.famc: Set[str] = set()

        for family in GedcomFile._family_dt.values():
            family.husband_id: str = ''
            family.wife_id: str = ''
            family.children: Set[str] = set()

        #Case where spouse and child roles are inconsistent with family record
        GedcomFile._individual_dt['@I0@'].fams = ({'@F_test2'})
        GedcomFile._individual_dt['@I0@'].famc = ({'@F_test3'})

        #Case where only spouse role is inconsistent with family record
        GedcomFile._individual_dt['@I1@'].fams = ({'@F_test4'})

        #Case where only child role is inconsistent with family record
        GedcomFile._individual_dt['@I2@'].famc = ({'@F_test5'})

        #Family records that are inconsistent with the above individual records:
        GedcomFile._family_dt['@F_test2'].husband_id = '@I4@'
        GedcomFile._family_dt['@F_test3'].children = ({'@I5@', '@I6@'})
        GedcomFile._family_dt['@F_test4'].wife_id = '@I9@'
        GedcomFile._family_dt['@F_test5'].children = ({'@I8@'})

        fam3_children: str = ', '.join(GedcomFile._family_dt['@F_test3'].children)

        result: List[str] = GedcomFile.US26_corresponding_entries_individuals(self.gedcom)

        expected: List[str] = [

            f'ERROR: US26: Individual @I0@-Test Subject0 and Family @F_test2 show spouse inconsistency. @I0@-Test Subject0 is identified as husband in @F_test2, but @F_test2 identifies husband as @I4@-Test Subject4',
            f'ERROR: US26: Individual @I0@-Test Subject0 and Family @F_test3 show children inconsistency. @I0@-Test Subject0 is identified as child in @F_test3, but @F_test3 identifies children as {fam3_children}',
            f'ERROR: US26: Individual @I1@-Test Subject1 and Family @F_test4 show spouse inconsistency. @I1@-Test Subject1 is identified as wife in @F_test4, but @F_test4 identifies wife as @I9@-Test Subject9',
            f'ERROR: US26: Individual @I2@-Test Subject2 and Family @F_test5 show children inconsistency. @I2@-Test Subject2 is identified as child in @F_test5, but @F_test5 identifies children as @I8@',

        ]

        self.assertEqual(result, expected)
        
    def test_US26_corresponding_entries_families(self) -> None:
        '''tests the case where individual roles (spouse, child) specified in a family record are not consistent with the corresponding entries in the 
            corresponding individual record. If such a case is found, it is highlihgted as an error
        '''

        #Clears tags to be used in test cases:
        for individuals in GedcomFile._individual_dt.values():
            individuals.fams: Set[str] = set()
            individuals.famc: Set[str] = set()

        for family in GedcomFile._family_dt.values():
            family.husband_id: str = ''
            family.wife_id: str = ''
            family.children: Set[str] = set()

        #Case where husband, wife, and child roles are inconsistent with individual record:
        GedcomFile._family_dt['@F_test0'].husband_id = '@I0@'
        GedcomFile._family_dt['@F_test0'].wife_id = '@I1@'
        GedcomFile._family_dt['@F_test0'].children = ({'@I2@', '@I3@', '@I4@'})

        #Case where wife role is inconsistent with individual record:
        GedcomFile._family_dt['@F_test1'].wife_id = '@I5@'

        #Case where husband role is inconsistent with individual record:
        GedcomFile._family_dt['@F_test2'].husband_id = '@I6@'

        #Case where a child role is inconsistent with individual record:
        GedcomFile._family_dt['@F_test3'].children = ({'@I7@'})

        #Individual records that are inconsistent with the above family records:
        GedcomFile._individual_dt['@I0@'].fams = ({'@F_test5'})
        GedcomFile._individual_dt['@I1@'].fams = ({'@F_test5'})
        GedcomFile._individual_dt['@I2@'].famc = ({'@F_test5'})
        GedcomFile._individual_dt['@I3@'].famc = ({'@F_test5'})
        GedcomFile._individual_dt['@I4@'].famc = ({'@F_test5'})
        GedcomFile._individual_dt['@I5@'].fams = ({'@F_test4'})
        GedcomFile._individual_dt['@I6@'].fams = ({'@F_test3'})
        GedcomFile._individual_dt['@I7@'].famc = ({'@F_test1'})

        fam0_children: List[str] = list(GedcomFile._family_dt['@F_test0'].children)
        fam0_child1: str = f'{fam0_children[0]}-{GedcomFile._individual_dt[fam0_children[0]].name}'
        fam0_child2: str = f'{fam0_children[1]}-{GedcomFile._individual_dt[fam0_children[1]].name}'
        fam0_child3: str = f'{fam0_children[2]}-{GedcomFile._individual_dt[fam0_children[2]].name}'

        result: List[str] = GedcomFile.US26_corresponding_entries_families(self.gedcom)

        expected: List[str] = [

             f'ERROR: US26: Family @F_test0 and Individual @I0@-Test Subject0 show spouse inconsistency. @F_test0 identifies @I0@-Test Subject0 as husband, but @I0@-Test Subject0 is husband in @F_test5',
             f'ERROR: US26: Family @F_test0 and Individual @I1@-Test Subject1 show spouse inconsistency. @F_test0 identifies @I1@-Test Subject1 as wife, but @I1@-Test Subject1 is wife in @F_test5',
             f'ERROR: US26: Family @F_test0 and Individual {fam0_child1} show child inconsistency. @F_test0 identifies {fam0_child1} as child, but {fam0_child1} is child in @F_test5',
             f'ERROR: US26: Family @F_test0 and Individual {fam0_child2} show child inconsistency. @F_test0 identifies {fam0_child2} as child, but {fam0_child2} is child in @F_test5',
             f'ERROR: US26: Family @F_test0 and Individual {fam0_child3} show child inconsistency. @F_test0 identifies {fam0_child3} as child, but {fam0_child3} is child in @F_test5',
             f'ERROR: US26: Family @F_test1 and Individual @I5@-Test Subject5 show spouse inconsistency. @F_test1 identifies @I5@-Test Subject5 as wife, but @I5@-Test Subject5 is wife in @F_test4',
             f'ERROR: US26: Family @F_test2 and Individual @I6@-Test Subject6 show spouse inconsistency. @F_test2 identifies @I6@-Test Subject6 as husband, but @I6@-Test Subject6 is husband in @F_test3',
             f'ERROR: US26: Family @F_test3 and Individual @I7@-Test Subject7 show child inconsistency. @F_test3 identifies @I7@-Test Subject7 as child, but @I7@-Test Subject7 is child in @F_test1',    

        
        ]

        self.assertEqual(result, expected)


    def test_US29_list_deceased_individuals(self) -> None:
        '''tests that the method implented for US29 stores the ID and Name for all individuals that are deceased'''

        GedcomFile._individual_dt['@I0@'].living = False
        GedcomFile._individual_dt['@I0@'].death_date = datetime.date(1990,10,12)

        GedcomFile._individual_dt['@I1@'].living = False
        GedcomFile._individual_dt['@I1@'].death_date = datetime.date(1985,11,11)

        GedcomFile._individual_dt['@I2@'].living = False
        GedcomFile._individual_dt['@I2@'].death_date = datetime.date(1995,11,11)


        result: Dict[str, str] = GedcomFile.US29_list_deceased_individuals(self.gedcom)

        expected: Dict[str, str] = {

                    '@I0@' : {'name':'Test Subject0', 'death date': datetime.date(1990,10,12)},
                    '@I1@' : {'name':'Test Subject1', 'death date': datetime.date(1985,11,11)},
                    '@I2@' : {'name':'Test Subject2', 'death date': datetime.date(1995,11,11)},
        }


        self.assertEqual(result, expected)



    def test_US38_upcoming_birthdays(self):

        # Let's remove the birthday from all individuals, so that the test can focus only
        # on those that we drive as inputs. This also drives an input case for 
        # individuals without a birthday listed.
        for person in self.gedcom._individual_dt.values():
            person.birth = ""

        expected_persons_list = list()

        # 30 Days Ahead - Expected in the output
        person = GedcomFile._individual_dt["@I0@"]
        person.birth = datetime.datetime.date(self.today + datetime.timedelta(days=30))
        expected_persons_list.append([person.id, person.name, person.birth, 30])

        # 30 Days Ahead, but deceased - Not expected in the output
        person = GedcomFile._individual_dt["@I1@"]
        person.birth = datetime.datetime.date(self.today + datetime.timedelta(days=30))
        person.living = False

        # 30 Days already past - not Expected in the output
        person = GedcomFile._individual_dt["@I2@"]
        person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=30))

        # Birthday Tomorrow! - Expected in the output
        person = GedcomFile._individual_dt["@I3@"]
        person.birth = datetime.datetime.date(self.today + datetime.timedelta(days=1))
        expected_persons_list.append([person.id, person.name, person.birth, 1])

        # Birthday Yesterday -Not Expected in the output
        person = GedcomFile._individual_dt["@I4@"]
        person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=1))

        # Birthday Today! - Expected in the output
        person = GedcomFile._individual_dt["@I5@"]
        person.birth =  datetime.date(self.today.year, self.today.month, self.today.day) 
        expected_persons_list.append([person.id, person.name, person.birth, 0])

        # 31 Days ahead - Not expected in the output
        person = GedcomFile._individual_dt["@I11@"]
        person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=31))


        # Invoke method under test, determine result.
        actual = self.gedcom.list_upcoming_birthdays()
        self.assertEqual(expected_persons_list, actual)

        # Test whether the pretty table prints out correctly.
        test_pt_upcoming_bdays: PrettyTable = PrettyTable(field_names=['ID', 'Name', "Birth Date", "Days Until"])

        for id, name, birthdate, days_till in expected_persons_list:
            test_pt_upcoming_bdays.add_row([id, name, birthdate, days_till])

        test_pt_upcoming_bdays.sortby = "Days Until"
        test_pt_upcoming_bdays.reversesort = False

        actual_pt = self.gedcom.US38_print_upcoming_birthdays()
        self.assertEqual(test_pt_upcoming_bdays.get_string(), actual_pt.get_string())






    def test_US39_upcoming_anniversaries(self):

        # Default families and individuals
        for family in self.gedcom._family_dt.values():
            family.marriage_date = "NA"
            family.divorce_date = "NA"
            self.gedcom._individual_dt[family.husband_id].living = True
            self.gedcom._individual_dt[family.husband_id].death_date = "NA"
            self.gedcom._individual_dt[family.wife_id].living = True
            self.gedcom._individual_dt[family.wife_id].death_date = "NA"

        expected_family_list = list()

        # 30 Days Ahead - Expected in the output
        family = GedcomFile._family_dt["@F_test0"]
        family.marriage_date = datetime.datetime.date(self.today + datetime.timedelta(days=30))
        expected_family_list.append([family.id, 30])

        # 30 Days Ahead, but divorced - Not expected in the output
        family = GedcomFile._family_dt["@F_test1"]
        family.marriage_date = datetime.datetime.date(self.today + datetime.timedelta(days=30))
        family.divorce_date =  datetime.datetime.date(self.today + datetime.timedelta(days=365))

        # 1 Day already past - not Expected in the output
        family = GedcomFile._family_dt["@F_test2"]
        family.marriage_date = datetime.datetime.date(self.today - datetime.timedelta(days=1))

        # Anniversary Tomorrow! - Expected in the output
        family = GedcomFile._family_dt["@F_test3"]
        family.marriage_date = datetime.datetime.date(self.today + datetime.timedelta(days=1))
        expected_family_list.append([family.id, 1])

        # Anniversary Today, but spouse is deceased. Not Expected in the output
        family = GedcomFile._family_dt["@F_test4"]
        family.marriage_date =  datetime.date(self.today.year, self.today.month, self.today.day)
        self.gedcom._individual_dt[family.wife_id].living = False

        # 31 Days ahead - Not expected in the output
        family = GedcomFile._family_dt["@F_test5"]
        family.marriage_date = datetime.datetime.date(self.today + datetime.timedelta(days=31))

        # Invoke method under test, determine result.
        actual = self.gedcom.list_upcoming_anniversaries()
        self.assertEqual(expected_family_list, actual)

        # Test whether the pretty table prints out correctly.
        test_pt_upcoming_adays: PrettyTable = PrettyTable(field_names=['Family ID', 'Husband Name', 'Husband ID', "Wife Name", "Wife ID", "Marriage Date", "Days Until"])

        for id, days_till in expected_family_list:
            f = self.gedcom._family_dt[id]
            test_pt_upcoming_adays.add_row([id, f.husband_name, f.husband_id, f.wife_name, f.wife_id, f.marriage_date, days_till])

        test_pt_upcoming_adays.sortby = "Days Until"
        test_pt_upcoming_adays.reversesort = False

        actual_pt = self.gedcom.US39_print_upcoming_anniversaries()
        self.assertEqual(test_pt_upcoming_adays.get_string(), actual_pt.get_string())






if __name__ == '__main__':
    unittest.main()
