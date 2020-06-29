import unittest
import unittest.mock
import SSW555_Group_Project
import io
import datetime
import sys
import logging
from typing import IO, Dict
from SSW555_Group_Project import Individual, GedcomFile
from prettytable import PrettyTable

# Set True if you want to see expected/actual values.
TC_VERBOSE = False

class Test_US35(unittest.TestCase):

    def setUp(self):
        SSW555_Group_Project.GedcomFile._individual_dt.clear()
        self.gedcom = SSW555_Group_Project.GedcomFile()
        self.person = SSW555_Group_Project.Individual()
        self.person.id = "@I_test1@"
        self.person.living = True
        self.person.name = "Test Subject"
        self.person.famc = "@F_test1@"
        self.person.fams = "@F_test2@"
        SSW555_Group_Project.GedcomFile._individual_dt[self.person.id]=self.person
        self.today = datetime.datetime.today()
        self.log = logging.getLogger("Test")

    def print_testcasedetails(self,expected,actual):
        if TC_VERBOSE==True:
            self.log.debug("Test Case: %s",self.id())
            self.log.debug("Expected Value: %s" %expected)
            self.log.debug("  Actual Value: %s" %actual)
            self.log.debug("Test Passed? %s" %(expected==actual))         


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_30days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=30))
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)

        expected = "ANOMALY: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s\n" \
                %(self.person.name, self.person.id, 30, self.person.birth)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())
   
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_0days(self,mocked_stdout):
        self.person.birth = datetime.date(self.today.year, self.today.month, self.today.day)       
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)
        expected = "ANOMALY: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s\n" \
                %(self.person.name, self.person.id, 0, self.person.birth)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_31days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=31))
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_neg1days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today + datetime.timedelta(days=1))
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())






class Test_US34(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        SSW555_Group_Project.GedcomFile._individual_dt.clear()
        SSW555_Group_Project.GedcomFile._family_dt.clear()
        self.gedcom = SSW555_Group_Project.GedcomFile()

        # Create 2 pairs husband/wife. This creates the individuals and families.
        for i in range(0,4):

            if i%2 == 0:
                self.family = SSW555_Group_Project.Family()
                self.family.id = "@F_Stest" + str(i//2)
                SSW555_Group_Project.GedcomFile._family_dt[self.family.id] = self.family

            self.person = SSW555_Group_Project.Individual()
            self.person.id = "@I" + str(i) + "@"
            self.person.living = True
            self.person.name = "Test " + "Subject"+ str(i)
            self.person.famc = "@F_Ctest" + str(i)
            self.person.fams = "@F_Stest" + str(i//2)

            if i%2 == 0:
                self.person.sex = "M"
                self.family.husband_id = self.person.id
                self.family.husband_name = self.person.name
            else:
                self.person.sex = "F"
                self.family.wife_id = self.person.id
                self.family.wife_name = self.person.name

            SSW555_Group_Project.GedcomFile._individual_dt[self.person.id] = self.person     


    def test_US34_spouseExactly2xAge(self):
        husband_age = 18
        wife_age = husband_age * 2
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].age = wife_age
        
        wife_age = 35
        husband_age = wife_age * 2
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].age = wife_age

        actual = SSW555_Group_Project.GedcomFile.US34_list_large_age_differences(self.gedcom)

        expected = ""
        self.assertEqual(expected, actual)
        



    def test_US34_spouseGreater2xAge(self):
        husband_age = 18
        wife_age = (husband_age * 2) + 1
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].age = wife_age
        husband_name = SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name
        wife_name = SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].name
        family_id = SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].fams
        
        expected_1 = "ANOMALY: US34: FAMILY: %s Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d\n" \
            %(family_id, wife_name, "@I1@", wife_age, husband_name,  "@I0@", husband_age )

        wife_age = 35
        husband_age = (wife_age * 2) + 1
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].age = wife_age
        husband_name = SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].name
        wife_name = SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].name
        family_id = SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].fams

        expected_2 = "ANOMALY: US34: FAMILY: %s Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d\n" \
            %(family_id, husband_name, "@I2@", husband_age, wife_name,  "@I3@", wife_age ) 

        expected = expected_1 + expected_2

        actual = SSW555_Group_Project.GedcomFile.US34_list_large_age_differences(self.gedcom)

        self.assertEqual(expected, actual)


    def test_US34_spouseNegAge(self):
        husband_age = -18
        wife_age = -8
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].age = wife_age

        wife_age = -35
        husband_age = -17
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].age = wife_age

        expected = ""

        actual = SSW555_Group_Project.GedcomFile.US34_list_large_age_differences(self.gedcom)

        self.assertEqual(expected, actual)
        



class GedcomFileTest(unittest.TestCase):
    '''Tests that the method implemented for US30 & US31:
        -Identifies all people that are living and married
        -Identifies all people that are living, over 30 yrs old, & have never been married
    '''

    test_file_name: str = 'p1.ged'

    def test_all_people_living_and_married(self) -> None:
        '''Tests that the method correctly identifies all individuals, by ID and name, that are alive and married.
        '''

        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        gedcom.parse_individuals_based_on_living_and_marital_details()
        
        result: Dict[str, str] = gedcom._individuals_living_and_married

        expected: Dict[str, str] = {
                                    '@I10@' : 'James /Matthews/',
                                    '@I11@' : 'Vera /Matthews/',
                                    '@I14@' : 'Jim /Halpert/',
                                    '@I16@' : 'Ross /Geller/',
                                    '@I17@' : 'Rachel /Geller/',
                                    '@I18@' : 'Steve /Smith/',
                                    '@I19@' : 'April /Smith/',
                                    '@I20@' : 'Sammy /Paterson/',
                                    '@I21@' : 'Ran /Paterson/',
                                    '@I2@' : 'Sankar /Sam/',
                                    '@I3@' : 'Sunitha /Krish/',
                                    '@I5@' : 'Baby /Chung/',
                                    '@I6@' : 'Leela /Pritish/',
                                   }

        self.assertEqual(result, expected)

    def test_all_people_living_over_thirty_and_never_married(self) -> None:
        '''Tests that the method correctly identifies all individuals, by ID and name, that are alive
            over 30 yrs old, and have never been married.
        '''

        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        gedcom.parse_individuals_based_on_living_and_marital_details()
        
        result: Dict[str, str] = gedcom._individuals_living_over_thirty_and_never_married
        
        expected: Dict[str, str] = {
                                    '@A3@' : 'Peter /Parker/',
                                    '@I8@' : 'Manuel /Rivera/',
                                   }

        self.assertEqual(result, expected)

    def test_US06(self):
    
        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        result = gedcom.US06_divorce_before_death()

        expect = [
                   f"ERROR: US06: family:@F6@: Husband ID: @I14@ Husband Name: Jim /Halpert/ Divorced 2018-04-14 after wife's death:  ID: @I15@ Name: Pam /Halpert/ death date: 2018-04-13"
                 ]
        self.assertEqual(expect, result)

    def test_US03(self):
    
        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        result = gedcom.US03_birth_death()

        expect = [ 
                  f"ERROR: US03: Individual ID: @I13@ Name: Joe /Swanson/ has death date 2000-04-13 before birth 2000-04-14"
                 ]

        self.assertEqual(expect, result)





class TestUS04_US21(unittest.TestCase):
    def setUp(self):
        SSW555_Group_Project.GedcomFile._individual_dt.clear()
        SSW555_Group_Project.GedcomFile._family_dt.clear()
        self.gedcom = SSW555_Group_Project.GedcomFile()

        # Create 6 pairs husband/wife. This creates the individuals and families.
        for i in range(0,(6*2)):

            if i%2 == 0:
                self.family = SSW555_Group_Project.Family()
                self.family.id = "@F_Stest" + str(i//2)
                SSW555_Group_Project.GedcomFile._family_dt[self.family.id] = self.family

            self.person = SSW555_Group_Project.Individual()
            self.person.id = "@I" + str(i) + "@"
            self.person.living = True
            self.person.name = "Test " + "Subject"+ str(i)
            self.person.fams = "@F_Stest" + str(i//2)

            if i%2 == 0:
                self.person.sex = "M"
                self.family.husband_id = self.person.id
                self.family.husband_name = self.person.name
            else:
                self.person.sex = "F"
                self.family.wife_id = self.person.id
                self.family.wife_name = self.person.name

            SSW555_Group_Project.GedcomFile._individual_dt[self.person.id] = self.person

        self.log = logging.getLogger("Test")
     
    def test_US04_Marriage_before_divorce(self):
        # Family 0: Divorce before marriage by 1 day
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest0"].marriage_date = datetime.date(1985,11,11)
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest0"].divorce_date = datetime.date(1985,11,10)

        # Family 2: Normal (Divorce after Marriage by 1 day). No Error Expected
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest1"].marriage_date = datetime.date(1985,11,10)
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest1"].divorce_date = datetime.date(1985,12,10)     
   
        # Family 5: Normal (Divorce after Marriage by 60 years). No Error Expected
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest2"].marriage_date = datetime.date(1940,11,10)
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest2"].divorce_date = datetime.date(2000,11,10)   


        result = self.gedcom.US4_Marriage_before_divorce()
        expect = [
                  "ERROR:US04:FAMILY:<@F_Stest0> Divorce 1985-11-10 happens before marriage 1985-11-11 Husband: ID @I0@, Name Test Subject0  Wife: ID @I1@, Name Test Subject1" , 
                 ]
        self.assertEqual(result, expect)



    def test_US21_correct_gender_for_role(self):
        # Family 0: Wrong Husband Sex
        husband_id = SSW555_Group_Project.GedcomFile._family_dt["@F_Stest0"].husband_id
        SSW555_Group_Project.GedcomFile._individual_dt[husband_id].sex = "F"

        # Family 1: Wrong Wife Sex
        wife_id = SSW555_Group_Project.GedcomFile._family_dt["@F_Stest1"].wife_id
        SSW555_Group_Project.GedcomFile._individual_dt[wife_id].sex = "M"

        # Family 2: Invalid Wife Sex
        wife_id = SSW555_Group_Project.GedcomFile._family_dt["@F_Stest2"].wife_id
        SSW555_Group_Project.GedcomFile._individual_dt[wife_id].sex = "BAD VALUE"

        # Family 3: Invalid Husband Sex
        husband_id = SSW555_Group_Project.GedcomFile._family_dt["@F_Stest3"].husband_id
        SSW555_Group_Project.GedcomFile._individual_dt[husband_id].sex = ""

        # Family 4: Uninitialized Husband ID (No error expected)
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest4"].husband_id = ""

        # Family 5: Uninitialized Wife ID (No Error expected)
        SSW555_Group_Project.GedcomFile._family_dt["@F_Stest4"].wife_id = ""        

        result = self.gedcom.US21_correct_gender_for_role()
        expect = [
                  "ERROR: US21: FAMILY:<@F_Stest0> Incorrect sex for husband id: @I0@ name: Test Subject0 sex: F ",
                  "ERROR: US21: FAMILY:<@F_Stest1> Incorrect sex for wife id: @I3@ name: Test Subject3 sex: M ",
                  "ERROR: US21: FAMILY:<@F_Stest2> Incorrect sex for wife id: @I5@ name: Test Subject5 sex: BAD VALUE ",
                  "ERROR: US21: FAMILY:<@F_Stest3> Incorrect sex for husband id: @I6@ name: Test Subject6 sex:  ",
                 ]
        self.assertEqual(result, expect)







class TestUS36_US37(unittest.TestCase):
    def setUp(self):
        SSW555_Group_Project.GedcomFile._individual_dt.clear()
        SSW555_Group_Project.GedcomFile._family_dt.clear()
        self.gedcom = SSW555_Group_Project.GedcomFile()

        # Create 6 pairs husband/wife. This creates the individuals and families.
        for i in range(0,(6*2)):

            if i%2 == 0:
                family = SSW555_Group_Project.Family()
                family.id = "@F_test" + str(i//2)
                SSW555_Group_Project.GedcomFile._family_dt[family.id] = family

            person = SSW555_Group_Project.Individual()
            person.id = "@I" + str(i) + "@"
            person.name = "Test " + "Subject"+ str(i)
            person.fams = set({"@F_test" + str(i//2)})

            if i%2 == 0:
                person.sex = "M"
                family.husband_id = person.id
                family.husband_name = person.name
            else:
                person.sex = "F"
                family.wife_id = person.id
                family.wife_name = person.name

            SSW555_Group_Project.GedcomFile._individual_dt[person.id] = person

        self.log = logging.getLogger("Test")
        self.today = datetime.datetime.today()

    def test_US36_recently_deceased(self):
        # Initialize Inputs 
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=29))
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=30))
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=31))
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=0))
        SSW555_Group_Project.GedcomFile._individual_dt["@I4@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=365*40))
        SSW555_Group_Project.GedcomFile._individual_dt["@I5@"].death_date =  datetime.datetime.date(self.today + datetime.timedelta(days=1))
        SSW555_Group_Project.GedcomFile._individual_dt["@I6@"].death_date =  datetime.datetime.date(self.today + datetime.timedelta(days=365*40))
        SSW555_Group_Project.GedcomFile._individual_dt["@I7@"].death_date =  ""
        SSW555_Group_Project.GedcomFile._individual_dt["@I8@"].death_date =  "NA"
        SSW555_Group_Project.GedcomFile._individual_dt["@I9@"].death_date =  "28 JAN 1940"

        #Initialize expected results. 
        # We expect only the death dates that fall within the past 30 days. Therefore, @I0@, @I1@, and @I3@
        expected_results = list()
        expected_results.append(["@I0@", SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name, SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].death_date])
        expected_results.append(["@I1@", SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].name, SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].death_date])
        expected_results.append(["@I3@", SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].name, SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].death_date])

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
        SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].children = set({"@I2@"})

        SSW555_Group_Project.GedcomFile._family_dt["@F_test1"].husband_id = "@I2@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test1"].wife_id =    "@I3@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test1"].children = set({"@I4@"})

        SSW555_Group_Project.GedcomFile._family_dt["@F_test2"].husband_id = "@I4@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test2"].wife_id =    "@I5@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test2"].children = set({"@I6@", "@I8@", "@I10@"})

        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=29))
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].living = False
        SSW555_Group_Project.GedcomFile._individual_dt["@I10@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=31))
        SSW555_Group_Project.GedcomFile._individual_dt["@I10@"].living = False

        if divorced:
            SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].divorce_date = SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].death_date - datetime.timedelta(days=500)

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
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].id,
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name,
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].id,
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].name,
                                    "Ex-Spouse"
                            ])
        else:
            expected_pt.add_row([
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].id,
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name,
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].id,
                                    SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].name,
                                    "Spouse"
                            ])
        for entry in expected_descendants:
            if entry == "@I10@":
                continue
            expected_pt.add_row([
                                 SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].id,
                                 SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name,
                                 SSW555_Group_Project.GedcomFile._individual_dt[entry].id,
                                 SSW555_Group_Project.GedcomFile._individual_dt[entry].name,
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
        SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].husband_id = "@I0@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].wife_id =    "@I1@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test0"].children = set({"@I2@"})

        SSW555_Group_Project.GedcomFile._family_dt["@F_test1"].husband_id = "@I2@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test1"].wife_id =    "@I3@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test1"].children = set({"@I4@"})

        SSW555_Group_Project.GedcomFile._family_dt["@F_test2"].husband_id = "@I4@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test2"].wife_id =    "@I5@"
        SSW555_Group_Project.GedcomFile._family_dt["@F_test2"].children = set({"@I6@", "@I8@", "@I10@"})

        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=29))
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].living = False
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=1))
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].living = False
        SSW555_Group_Project.GedcomFile._individual_dt["@I10@"].death_date =  datetime.datetime.date(self.today - datetime.timedelta(days=31))
        SSW555_Group_Project.GedcomFile._individual_dt["@I10@"].living = False

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
                                SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].id,
                                SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name,
                                SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].id,
                                SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].name,
                                "Spouse"
                            ])
        for entry in expected_descendants_1:
            if entry == "@I10@":
                continue
            expected_pt.add_row([
                                 SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].id,
                                 SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name,
                                 SSW555_Group_Project.GedcomFile._individual_dt[entry].id,
                                 SSW555_Group_Project.GedcomFile._individual_dt[entry].name,
                                 "Descendant"
                                ])

        
        # Handle second family. Start by adding the spouse
        expected_pt.add_row([
                                SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].id,
                                SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].name,
                                SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].id,
                                SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].name,
                                "Spouse"
                            ])
        for entry in expected_descendants_2:
            if entry == "@I10@":
                continue
            expected_pt.add_row([
                                 SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].id,
                                 SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].name,
                                 SSW555_Group_Project.GedcomFile._individual_dt[entry].id,
                                 SSW555_Group_Project.GedcomFile._individual_dt[entry].name,
                                 "Descendant"
                                ])

        expected_pt.sortby = "Recently Deceased ID"

        actual_pt = self.gedcom.US37_list_recent_survivors()

        self.assertEqual(expected_pt.get_string(), actual_pt.get_string())





if __name__ == '__main__':
    if TC_VERBOSE == True:
        logging.basicConfig( stream=sys.stderr )
        logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
