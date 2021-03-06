from typing import Iterator, Tuple, IO, List, Dict, Set, DefaultDict
from collections import defaultdict
import datetime
import os
import sys
from prettytable import PrettyTable

class Family:
    '''class Family'''
    _pretty_table_headers: List[str] = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']

    def __init__(self):
        '''Initializes the details for an instance of a family'''

        self.id: str = ''
        self.marriage_date: str = 'NA'                         
        self.divorce_date: str = 'NA'                                 
        self.husband_id: str = ''
        self.husband_name: str = 'TBD'
        self.wife_id: str = ''
        self.wife_name: str = 'TBD'
        self.children: Set[str] = set()
        self.preceding_tag_related_to_date: str = ''

    def details(self, tag: str, argument: str) -> None:
        '''Assigns family detail based on a given tag'''
        
        if tag == 'FAM':
            self.id = argument
        
        if tag == 'HUSB':
            self.husband_id = argument

        if tag == 'WIFE':
            self.wife_id = argument
        
        if tag == 'CHIL':
            self.children.add(argument)
        
        if tag == 'MARR' or tag == 'DIV':
            self.preceding_tag_related_to_date = tag

        if tag == 'DATE':
            self.process_family_record_date_tag(argument)

    def process_family_record_date_tag(self, date_in_gedcom_format: str) -> None:
        '''Converts a date from the format set in a GEDCOM file (day, month, year) to
            the final desired format (year, month, day). Assigns the date to either marriage date or divorce date, based on its 
            preceding tag, which is either "MARR" or "DIV"
        '''

        day, month, year = date_in_gedcom_format.split(" ")
        day: int = int(day)
        year: int = int(year)
        month: int = datetime.datetime.strptime(month, '%b').month
        date_in_final_format: str = datetime.date(year, month, day)

        if self.preceding_tag_related_to_date == 'MARR':
            self.marriage_date = date_in_final_format

        elif self.preceding_tag_related_to_date == 'DIV':
            self.divorce_date = date_in_final_format
                
    def return_pretty_table_row(self) -> List[str]:
        '''Returns a list that is to be used as a row in the families pretty table'''

        return [self.id, self.marriage_date, self.divorce_date, self.husband_id, self.husband_name, self.wife_id, self.wife_name, (self.children or "None")]


class Individual:
    '''class Individual'''

    _headers_for_prettytable: List[str] = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    def __init__(self):
        '''Initializes the details for an instance of an individual'''

        self.id: str = ''
        self.name: str = ''
        self.sex: str = ''
        self.birth: str = ''
        self.age: int = ''
        self.living: str = True
        self.death_date: str = 'NA'
        self.famc: Set[str] = set()
        self.fams: Set[str] = set()
        self.preceding_tag_related_to_date: str = ''

    def details(self, tag: str, argument: str) -> None:
        '''Assigns family detail based on a given tag'''

        if tag == 'INDI':
            self.id = argument

        elif tag == 'NAME':
            self.name = argument

        elif tag == 'SEX':
            self.sex = argument

        elif tag == 'BIRT' or tag == 'DEAT':
            self.preceding_tag_related_to_date = tag
        
        elif tag == 'FAMC':
            self.famc.add(argument)
        
        elif tag == 'FAMS':
            self.fams.add(argument)

        elif tag == 'DATE':
            self.process_individual_record_date_tag(argument)

    def process_individual_record_date_tag(self, date_in_gedcom_format: str) -> None:
        '''Converts a date from the format set in a GEDCOM file (day, month, year) to
            the final desired format (year, month, day). Assigns the date to either marriage date or divorce date, based on its 
            preceding tag, which is either "BIRT" or "DEAT"
        '''

        day, month, year = date_in_gedcom_format.split(" ")
        day: int = int(day)
        year: int = int(year)
        month: int = datetime.datetime.strptime(month, '%b').month
        date_in_final_format: str = datetime.date(year, month, day)

        if self.preceding_tag_related_to_date == 'BIRT':
            self.birth = date_in_final_format

        elif self.preceding_tag_related_to_date == 'DEAT':
            self.death_date = date_in_final_format
            self.living = False
        #print(self.name)
        self.setAge()

    def setAge(self) -> None: 
        '''Calculates the age of an individual'''

        if self.living:
            today = datetime.date.today()
        else:
            today = self.death_date
        self.age = (today - self.birth).days//365  #TBD: Not perfect. leap years, etc.

    def return_pretty_table_row(self) -> List[str]:
        '''Returns a list that is to be used as a row for the individuals pretty table'''

        return [self.id, self.name, self.sex, self.birth, self.age, self.living, self.death_date, (self.famc or "None"), (self.fams or "NA")]

    def return_living_and_marital_details(self) -> Tuple[bool, int, str]:
        '''Implemented for US30 & US31. 
            Returns a tuple containing: individual's name as the first element, age as second element, a boolean as third element, and an int as the fourth element.
            -The boolean is True if individual is living, False if not.
            -The int reflects the # of families this individual has been a spouse of. If 0, the individual is/has not married. If greter than 0, the individual is married.
        '''

        return self.name, self.age, self.living, len(self.fams) 


class GedcomFile:
    '''class GedcomFile'''

    _valid_tags: Dict[str, str] = {  'INDI' : '0', 'NAME' : '1', 'SEX' : '1', 'BIRT' : '1', 'DEAT' : '1', 'FAMC' : '1',
                                'FAMS' : '1', 'FAM' : '0', 'MARR' : '1', 'HUSB' : '1', 'WIFE' : '1', 'CHIL' : '1', 
                                'DIV' : '1', 'DATE' : '2', 'HEAD' : '0', 'TRLR' : '0', 'NOTE' : '0', } #key = tag : value = level
    
    _individual_dt: Dict[str, Individual] = dict()
    _family_dt: Dict[str, Family] = dict()
    _individuals_living_and_married: Dict[str, str] = dict()
    _individuals_living_over_thirty_and_never_married: Dict[str, str] = dict()
    _list_of_duplicate_individual_ids: List[Individual] = list()
    _list_of_duplicate_family_ids: List[Family] = list()

    def __init__(self) -> None:
        '''Sets containers to store the input and output lines'''

        self._input: List[str] = list()
        self._output: List[str] = list()
        self._validated_list: List[str] = list()        

    def read_file(self, file_name: str) -> None:
        '''Reads a GEDCOM file and populates the self._input list container with the lines from the GEDCOM file'''

        file: IO = open(file_name)

        with file:
            for line in file:
                self._input.append(line.strip())
    
    def validate_tags_for_output(self) -> None:
        '''Takes each line in the self._input list container, splits it, and determines whether tags are valid'''
        #print(self._input)
        for line in self._input:
            #skip blank lines
            if len(line) == 0:
                continue
            line: List[str] = line.split()
            level: str = line[0]
            tag: str = line[1]
            arguments: str = f'{" ".join(line[2:])}'

            if 'INDI' in line or 'FAM' in line:
                self.validate_tags_for_exceptions(line, level, tag)
            else:
                if tag in GedcomFile._valid_tags and level == GedcomFile._valid_tags[tag]:
                    self._output.append(f'<-- {level}|{tag}|Y|{arguments}')
                else:
                    self._output.append(f'<-- {level}|{tag}|N|{arguments}')
      
    def validate_tags_for_exceptions(self, line: List[str], level: str, default_tag: str) -> None:
        '''Validates the tags for any line that meets the formatting exception identified in Project02 description.
            Format exceptions identified are: '0 <id> INDI' and '0 <id> FAM'
        '''

        if line[-1] == 'INDI' or line[-1] == 'FAM':
            tag: str = line[-1]
            arguments: str = f'{line[1]}'

            if tag in GedcomFile._valid_tags and level == GedcomFile._valid_tags[tag]:
                self._output.append(f'<-- {level}|{tag}|Y|{arguments}')
            else:
                self._output.append(f'<-- {level}|{tag}|N|{arguments}')

        else:
            arguments: str = f'{line[-1]}'
            self._output.append(f'<-- {level}|{default_tag}|N|{arguments}')
        
    def update_validated_list(self) -> None:
        '''Create a list of validated gedcom entries'''
        for entry in self._output:
            level, tag, validity, arg = entry.split("|")
            level = int(level[-1])
            if validity == 'Y':
                self._validated_list.append([level, tag, arg])

    def parse_valid_entry(self) -> Tuple[str]:
        '''Generator to extract level, tag and argument from validated list'''

        for valid_line in self._validated_list: 
            level: int = int(valid_line[0])
            tag: str = valid_line[1]
            argument: str = valid_line[2]
            yield level, tag, argument

    def parse_validated_gedcom(self) -> None:
        '''Parses the gedcom entries for individuals and families'''
        
        # Default our flags to neither an individual or family
        individual_record = False
        family_record = False
        
        for _, tag, argument in self.parse_valid_entry():
            if tag == "INDI":
                # Subsequent records will define an individual
                individual_record = True
                family_record = False
                
                # Since this is the start - Create the Individual!
                individual: Individual = Individual()
                individual_id: str = argument

                if individual_id in self._individual_dt:
                    self._list_of_duplicate_individual_ids.append(individual)
                else:
                    self._individual_dt[individual_id] = individual
                
            elif tag == "FAM":
                # Subsequent records will define a family
                family_record = True
                individual_record = False
                
                # Since this is the start - Create the Family!
                family: Family = Family()
                family_id: str = argument

                if family_id in self._family_dt:
                    self._list_of_duplicate_family_ids.append(family)
                else:
                    self._family_dt[family_id] = family
                
            elif tag == "TRLR" or tag == "HEAD" or tag == "NOTE":
                 # this is neither a family or an individual.
                 family_record = False
                 individual_record = False
            
            # Record the details regarding this tag to the appropriate record type.
            if individual_record:
                individual.details(tag,argument)
            elif family_record:
                family.details(tag,argument)

    def print_individuals_pretty(self) -> PrettyTable:
        '''Prints a prettytable containing details for individuals'''

        individuals_pretty_table: PrettyTable = PrettyTable(field_names= Individual._headers_for_prettytable)
        
        for individual in self._individual_dt.values():
            individuals_pretty_table.add_row(individual.return_pretty_table_row())
        
        individuals_pretty_table.sortby = 'ID'
        print("People")
        print(individuals_pretty_table)
        print("\n")

    def print_family_pretty(self) -> PrettyTable:
        '''Prints a prettytable containing details for individuals'''

        family_pretty_table: PrettyTable = PrettyTable(field_names= Family._pretty_table_headers)

        for family in self._family_dt.values():
            family_pretty_table.add_row(family.return_pretty_table_row())
        
        print("Families")
        print(family_pretty_table)
        print("\n")

    def family_set_spouse_names(self):
        for entry in self._family_dt:
            
            husband_id = self._family_dt[entry].husband_id
            try:
                husband_name = self._individual_dt[husband_id].name
            except KeyError:
                husband_name = "Unknown"      
            self._family_dt[entry].husband_name = husband_name   

            wife_id = self._family_dt[entry].wife_id
            try:
                wife_name = self._individual_dt[wife_id].name                    
            except KeyError:
                wife_name = "Unknown"  
            self._family_dt[entry].wife_name = wife_name        
            
    def US03_birth_death(self):
        ''' Birth before death '''
        x = []
        for k, v in self._individual_dt.items():
            if v.death_date != 'NA' and v.birth != 'NA':
                if(v.death_date < v.birth):
                    output = f"ERROR: US03: Individual ID: {k} Name: {v.name} has death date {v.death_date} before birth {v.birth}"
                    print(output)
                    x.append(output)
        return x

    def US06_divorce_before_death(self):
        '''Divorce can take place only before death of both individuals '''
        x = []
        for k, v in self._family_dt.items():
            if v.divorce_date != 'NA':
                hd = self._individual_dt[v.husband_id].death_date
                wd = self._individual_dt[v.wife_id].death_date
                if hd != 'NA' and v.divorce_date > hd:
                    output = f"ERROR: US06: family:{k}: Wife ID: {v.wife_id} Wife Name: {v.wife_name} Divorced {v.divorce_date} after husband's death:  ID: {v.husband_id} Name: {v.husband_name} death date: {hd}"
                    print(output)
                    x.append(output)
                if wd != 'NA' and v.divorce_date > wd:
                   output = f"ERROR: US06: family:{k}: Husband ID: {v.husband_id} Husband Name: {v.husband_name} Divorced {v.divorce_date} after wife's death:  ID: {v.wife_id} Name: {v.wife_name} death date: {wd}"
                   print(output)
                   x.append(output)
        return x            
               
    def US07_Death150(self):
        ''' Death for all dead people and currently living must be less than 150'''
        x = []

        for k, v in self._individual_dt.items():
            if v.age != 'NA' and v.age >= 150:
                output = f"ERROR: US07: Individual ID: {k} Name: {v.name} is more more than 150 years old!"

                if v.death_date != 'NA':
                    output += f"Death date is {v.death_date}"

                print(output)
                x.append(output)
        return x

    def US12_Mother_Father_older(self):
        ''' Mother's age - Sons age should be < 60, Father's age - Son's age should be < 80 '''
        x = set()

        for k in self._family_dt.values():
            if k.wife_id != 'NA':
                w = self._individual_dt[k.wife_id]
                if w.age == 'NA':
                    print(f"US12: Individual ID:{w.id} Mother's Name:{w.name} Age is NA")
                    continue
            if k.husband_id != 'NA':
                h = self._individual_dt[k.husband_id]
                if h.age == 'NA':
                    print(f"US12: Individual ID:{h.id} Father's Name:{h.name} Age is NA")
                    continue
            if k.children:
                for c in [self._individual_dt[ch] for ch in k.children]:
                    if c.age == 'NA':
                        print(f"US12: The child name:{c.name} with ID {c.id} has Age NA")
                    if w.age - c.age >= 60:
                        output = f"ANOMALY: US12: Family ID:{k.id} Mother's ID:{w.id} and Name:{w.name} and Age:{w.age} is 60 years or older than Child's ID: {c.id} Name: {c.name} Age: {c.age}"
                        print(output)
                        x.add(k.id)
                    if h.age - c.age >= 80:
                        output = f"ANOMALY: US12: Family ID:{k.id} Father's ID:{h.id} and Name:{h.name} and Age:{h.age} is 80 years or older than Child's ID: {c.id} Name: {c.name} Age: {c.age}"
                        print(output)
                        x.add(k.id)

        return x

    def US16_male(self):
        '''' Male members of the family must have the same last name'''
        r = []
        for x in self._family_dt.values():
            h_id = self._individual_dt[x.husband_id].id
            fullname = self._individual_dt[x.husband_id].name
            if ('/' not in fullname):
                continue

            last_name = (self._individual_dt[x.husband_id].name).split('/')[1]
            child_lname = []

            if x.husband_id != 'NA' and x.children:
                for child_id in x.children:
                    c = self._individual_dt[child_id]
                    if c.sex == 'M':
                        if ('/' not in c.name):
                            continue

                        child_lname.append(c.name.split('/')[1])

                for name in child_lname:
                    if name != last_name:
                        output = f"ERROR: US16: Family ID:{x.id} Last name do not match, Father's Name:{fullname} ID:{h_id} and Child's Name: {c.name} Child ID: {c.id}"
                        print(output)
                        r.append(x.id)
        return r

    def families(self, family_set):
        '''yields a family object for a given set of family ids'''
        for family in family_set:
            yield self._family_dt[family]

    def find_grandparents(self, indi_id):
        '''Finds all grandparents for a given individual'''
        r = list()
        indi = self._individual_dt[indi_id]

        # Run through all the families where this individual is a child. Normally expected only 1 family.
        for parent_fam in self.families(indi.famc):

            # Find the grandparents on the father's side.
            for grandparent_fam in self.families(self._individual_dt[parent_fam.husband_id].famc):
                r.append(grandparent_fam.husband_id)
                r.append(grandparent_fam.wife_id)

            # Find the grandparents on the mother's side
            for grandparent_fam in self.families(self._individual_dt[parent_fam.wife_id].famc):
                r.append(grandparent_fam.husband_id)
                r.append(grandparent_fam.wife_id)
                
        return r

    def US19_married_first_cousins(self): 
        r = list()
        for fam in self._family_dt.values():
            grandparents =  self.find_grandparents(fam.husband_id)
            grandparents += self.find_grandparents(fam.wife_id)
            
            # OK, now we have a list of grandparents from both spouses.
            # IF any grandparents are repeated in this list, then the spouses share a 
            # grandparent - and therefore are first cousins.
            if len(grandparents) == len(set(grandparents)):
                continue
            else:
                print(f"ANOMALY: US19: Family id: {fam.id} Husband name: {fam.husband_name}, husband id: {fam.husband_id} and wife name: {fam.wife_name}, wife id: {fam.wife_id} are first cousins")
                r.append(fam.id)
        return(r)

    def US01_dates_b4_current(self):
        '''Dates (birth, marriage, divorce, death) should not be after the current date'''
        current_date = datetime.date.today()
        r = list()
        for  fam in self._family_dt.values():
            if fam.marriage_date != 'NA':
                if fam.marriage_date > current_date:
                    output =f"Error US01 Family'ID:{fam.id} has marriage dates on {fam.marriage_date} after current date"
                    print(output)
                    r.append(output)

            if fam.divorce_date != 'NA':
                if fam.divorce_date > current_date:
                    output = f"Error US01 Family'ID:{fam.id} has divorce date on {fam.divorce_date} after current date"
                    print(output)
                    r.append(output)

        for  indi in self._individual_dt.values():
            if indi.birth != '':
                if indi.birth > current_date:
                    output = f"Error US01 Individual'ID:{indi.id} has birth date on {indi.birth} after current date"
                    print(output)
                    r.append(output)

            if indi.death_date != 'NA':        
                if indi.death_date > current_date:
                    output = f"Error US01 Individual'ID:{indi.id} has death date on {indi.death_date} after current date"
                    print(output)
                    r.append(output)
        return r
   
    def US17_no_marraige_2_children(self):
        '''Parents should not marry any of their children'''
        fam_list = list(self._family_dt.values())
        r = list()
        for fam in fam_list:
           if fam.husband_id != 'NA' and fam.wife_id !='NA':
                for famchild in fam_list:
                    if fam.husband_id in famchild.children and fam.wife_id == famchild.wife_id:
                         output = f"Error US17 Family ID {fam.id} Mother: wife's ID {fam.wife_id} wife's name {fam.wife_name} is married to her child's ID {famchild.husband_id} child's name {famchild.husband_name}"
                         print(output)
                         r.append(output)
                    elif fam.wife_id in famchild.children and fam.husband_id == famchild.husband_id:
                        output = f"Error US17 Family ID {fam.id} Father: Father's ID {fam.husband_id} husban's name {fam.husband_name} is married to his child's ID {famchild.wife_id} child's name {famchild.wife_name}"
                        print(output)
                        r.append(output)
        return r 

    def US14_multiple_births(self):
        '''No more than five siblings should be born at the same time '''
        r = []
        for k, v in self._family_dt.items():
            multiple_birth = self.Determine_multiple_birth(v.children)
            
            if len(multiple_birth) > 5:
                r.append(k)
        if r:
            print(f"ANOMALY: US14: Families {', '.join(r)} has more than 5 children born on the same time ")

        return r

    def US15_siblings15(self):
        '''There should be fewer than 15 siblings in a family '''
        r = []
        for k,v in self._family_dt.items():
            if (len(v.children) >= 15):
                r.append(k)
        
        if r:
            print(f"ANOMALY: US15: Families {', '.join(r)} have more than 15 children born")

        return r
                        
    def US2_birth_before_marriage(self):
        ''''Birth should occur before marriage of an individual'''
        r = list()
        for id in self._family_dt.keys():
            if self._family_dt[id].marriage_date != 'NA':
                marDate = self._family_dt[id].marriage_date
                indi_bdates = {}
                husID = self._family_dt[id].husband_id
                wifeID = self._family_dt[id].wife_id
                indi_bdates[husID] = self._individual_dt[husID].birth
                indi_bdates[wifeID] = self._individual_dt[wifeID].birth
                for ids, vals in indi_bdates.items():
                    if vals !='NA':
                        birthDate = vals
                        if marDate < birthDate:
                            output = f"ERROR: US2: FAMILY: {id} Individual: {ids} Name: {self._individual_dt[ids].name} birth: {birthDate} should be before marriage date {marDate}"
                            output2 = f"ERROR: US2: FAMILY: {id}"
                            print(output)
                            r.append(output2)
        return r

    def US5_marriage_before_death(self):
        '''Marriage should occur before death of either spouse'''
        r = list()
        for id in self._family_dt.keys():
            if self._family_dt[id].marriage_date != 'NA':
                marDate = self._family_dt[id].marriage_date
                indi_ddates = {} #inidvidual death dates dic 
                husID = self._family_dt[id].husband_id
                wifeID = self._family_dt[id].wife_id
                indi_ddates[husID] = self._individual_dt[husID].death_date
                indi_ddates[wifeID] = self._individual_dt[wifeID].death_date
                for ids, vals in indi_ddates.items():
                     if vals !='NA': # to find death date for each indivdual 
                         deathDate = vals
                         if deathDate < marDate: #Compare if  death date for inidvidual happens before marriage date 
                             output = f"ERROR: US5: Family: {id} Individual: {ids} Name: {self._individual_dt[ids].name} dies on {deathDate} before marriage date on {marDate}"
                             output2 = f"ERROR: US5: FAMILY:{id}"              
                             print(output)
                             r.append(output2)
        return r
    
    def US22_uni_ids_indi_fam(self):
        '''All individual IDs should be unique and all family IDs should be unique '''

        output = list()
        for dup_family in self._list_of_duplicate_family_ids:
            output.append(f"ERROR: US22: Family ID: {dup_family.id} with wife ID: {dup_family.wife_id} and husband ID: {dup_family.husband_id} "+\
                     f"is a duplicate of Family ID: {dup_family.id} with wife ID: {self._family_dt[dup_family.id].wife_id} and husband id: {self._family_dt[dup_family.id].husband_id}")

        for dup_ind in self._list_of_duplicate_individual_ids:
            output.append(f"ERROR: US22: Individual ID: {dup_ind.id} with name {dup_ind.name} is a duplicate of individual ID {dup_ind.id} "+\
                     f"with name {self._individual_dt[dup_ind.id].name}")

        for entry in output:
            print(entry)
        return output

    
    def US23_uni_name_birth(self):
        ''' No more than one individual with the same name and birth date should appear in a GEDCOM file'''
        r = list()

        for inid, vals in self._individual_dt.items():
            dup_names = list()
            dup_birthdates = list()

            for ids in self._individual_dt.keys():
                if self._individual_dt[ids].name == vals.name:
                    dup_names.append(ids)
            if len (dup_names) > 1:
                for idis in dup_names:
                    if self._individual_dt[idis].birth == vals.birth:
                        dup_birthdates.append(idis)
                if len(dup_birthdates) > 1:
                    output = f"ERROR US23 Individuals ids {inid} and name {vals.name} found duplicated name and birthdate"
                    print(output)
                    r.append(output)
        return r
    

    def US4_Marriage_before_divorce(self): 
        '''Marriage should occur before divorce of spouses, and divorce can only occur after marriage'''
        r = list()
        for id in self._family_dt:
            marDate = self._family_dt[id].marriage_date
            divDate = self._family_dt[id].divorce_date
            if divDate != 'NA' and marDate != 'NA':
                if marDate > divDate:
                    h_name = self._family_dt[id].husband_name
                    h_id = self._family_dt[id].husband_id
                    w_name = self._family_dt[id].wife_name
                    w_id = self._family_dt[id].wife_id
                    output = f"ERROR:US04:FAMILY:<{id}> Divorce {divDate} happens before marriage {marDate} Husband: ID {h_id}, Name {h_name}  Wife: ID {w_id}, Name {w_name}"  
                    print(output)
                    r.append(output)
        return r

    def US21_correct_gender_for_role(self):
        '''Husband in family should be male and wife in family should be female'''
        r = list()
        for fm in self._family_dt.values():
            try:
                husband_sex = self._individual_dt[fm.husband_id].sex
            except KeyError:
                # Uninitialized husband ID. Skip it.
                pass
            else:
                if husband_sex != "M":
                    output = f"ERROR: US21: FAMILY:<{fm.id}> Incorrect sex for husband id: {fm.husband_id} name: {fm.husband_name} sex: {husband_sex} "
                    print(output)
                    r.append(output)

            try:
               wife_sex = self._individual_dt[fm.wife_id].sex
            except KeyError:
                # Uninitialized Wife ID. Skip it.
                pass
            else:
                if wife_sex != "F":
                    output = f"ERROR: US21: FAMILY:<{fm.id}> Incorrect sex for wife id: {fm.wife_id} name: {fm.wife_name} sex: {wife_sex} "
                    print(output)
                    r.append(output) 
        return r

    def US34_list_large_age_differences(self):
        '''US 34: List all couples who were married when the older spouse was more than twice as old as the younger spouse '''
        output = ""
        for family in self._family_dt.values():
            
            try:
                husband = self._individual_dt[family.husband_id]
                wife = self._individual_dt[family.wife_id]
            except KeyError:
                #Individual doesn't exist, so skip this family.
                continue

            if type(husband.age) == str or type(wife.age) == str:
                # A birthdate was not provided for one of the spouses. Skip this family.
                continue
            elif husband.age < 0 or wife.age < 0:
                # Invalid age, so skip this family.
                continue

            if husband.age > (wife.age * 2):
                husband_is_older = True
            elif wife.age > (husband.age * 2):
                husband_is_older = False
            else:
                # No need to report this married couple.
                continue

            # OK, if we're still here, then we have an Anomaly to report. 
            output += f"ANOMALY: US34: FAMILY: {family.id} "

            if husband_is_older:
                output += f"Name: {family.husband_name}, id: {family.husband_id}, age: {husband.age} is more than 2x in age as spouse: {family.wife_name}, id: {family.wife_id}, age: {wife.age}\n"        
            else:
                output += f"Name: {family.wife_name}, id: {family.wife_id}, age: {wife.age} is more than 2x in age as spouse: {family.husband_name}, id: {family.husband_id}, age: {husband.age}\n"
        
        print(output, end="")
        return output
            

    def US35_list_recent_births(self):
        '''US35: List all people in a GEDCOM file who were born in the last 30 days'''
        output = ""
        for person in self._individual_dt.values():
            birth_date = person.birth
            if type(birth_date) != datetime.date:
                # Invalid entry
                continue
            today = datetime.date.today()
            age_days = (today - birth_date).days  # difference results in datetime.timedelta

            if age_days < 0:
                # Invalid birthdays (set in the future!). Skip this individual.
                continue
            
            if age_days <= 30:
                output += f"ANOMALY: US35: Name: {person.name}, Individual: ID {person.id}, born {age_days} days ago! Birthday: {birth_date}\n"
        print(output, end="")
        return output

    def parse_individuals_based_on_living_and_marital_details(self) -> None:
        '''US30 & US31: Identifies whether an individual is: Living and married, or Living, over 30 years old and has never been married. After identifying, stores the 
            individuals ID and Name in either the _individuals_living_and_married dictionary or the _individuals_living_over_thirty_and_never_married dictionary'''
        
        for individual_id, individual in self._individual_dt.items():
            name, age, alive, number_of_times_married = individual.return_living_and_marital_details()
            
            if alive == True and number_of_times_married > 0:
                GedcomFile._individuals_living_and_married[individual_id] = name
            
            elif alive == True and age > 30 and number_of_times_married == 0:
                GedcomFile._individuals_living_over_thirty_and_never_married[individual_id] = name

    def list_individuals_living_and_married(self) -> None:
        '''US30: Prints a prettytable that lists all individuals that are alive and married'''

        pretty_table_for_living_and_married_people: PrettyTable = PrettyTable(field_names=['ID', 'Name'])

        if len(GedcomFile._individuals_living_and_married) == 0:
            pretty_table_for_living_and_married_people.add_row(['None', 'None'])
        
        else:
            for individual_id, name in GedcomFile._individuals_living_and_married.items():
                pretty_table_for_living_and_married_people.add_row([individual_id, name])
        
        print(f'\nUS30: All Individuals Living and Married:\n{pretty_table_for_living_and_married_people}\n')

    def list_individuals_living_over_thirty_never_married(self) -> None:
        '''US31: Prints a prettytable that lists all individuals that are alive, over 30 yrs old, and have never been married'''

        pretty_table_for_living_over_thirty_never_married: PrettyTable = PrettyTable(field_names=['ID', 'Name'])

        if len(GedcomFile._individuals_living_over_thirty_and_never_married) == 0:
            pretty_table_for_living_over_thirty_never_married.add_row(['None', 'None'])
        
        else:
            for individual_id, name in GedcomFile._individuals_living_over_thirty_and_never_married.items():
                pretty_table_for_living_over_thirty_never_married.add_row([individual_id, name])
        
        print(f'US31: All Individuals Living, Over 30, and Never Married:\n{pretty_table_for_living_over_thirty_never_married}\n')
    
    


    def US28_list_all_siblings_from_oldest_to_youngest(self) -> List[List[str]]:
        '''Lists all siblings in a family from oldest to youngest'''

        pretty_table_for_all_siblings: PrettyTable = PrettyTable(field_names = ['Family ID', 'Child ID', 'Child Name', 'Child Age'])
        all_siblings: List[List[str]] = list()

        for siblings in self.US28_order_siblings_by_age():
            all_siblings.append(siblings)
            pretty_table_for_all_siblings.add_row(siblings)
 
        print(f'\nUS28: All Siblings Ordered by Age From Oldest to Youngest:\n{pretty_table_for_all_siblings}\n')
        return all_siblings

    def US28_order_siblings_by_age(self) -> Iterator[List[List[str]]]:
        '''US28: Orders the siblings in each family by age from oldest to youngest''' 

        family_siblings: List[str] = list()

        for family_id, family in self._family_dt.items():
            fam_id: str = family_id
            children: Set[str] = family.children

            if len(children) > 1:
                for child_id in children:
                    name: str = self._individual_dt[child_id].name
                    age: str = self._individual_dt[child_id].age
                    family_siblings.append([fam_id, child_id, name, age])

                for siblings_sorted_by_age in sorted(family_siblings, reverse = True, key = lambda n: n[-1]):
                    yield siblings_sorted_by_age

                family_siblings = list()

    def find_deceased_within30days(self):
        result = list()
        for person in self._individual_dt.values():
            death_date = person.death_date
            if type(death_date) != datetime.date:
                # Invalid entry. Death date never logged, so skip this individual.
                continue
            today = datetime.date.today()
            days_since_death = (today - death_date).days  # difference results in datetime.timedelta

            if days_since_death < 0:
                # Invalid death date (set in the future!). Skip this individual.
                continue
            elif days_since_death <= 30:
                result.append([person.id, person.name, person.death_date])
        return result

    def US36_list_recent_deaths(self) -> None:
        '''List all people who died in the last 30 days'''
        recently_deceased_lst = self.find_deceased_within30days()

        pt_recently_deceased: PrettyTable = PrettyTable(field_names=['ID', 'Name', "Death Date"])

        for id, name, deathdate in recently_deceased_lst:
            pt_recently_deceased.add_row([id, name, deathdate])

        pt_recently_deceased.sortby = "Death Date"
        pt_recently_deceased.reversesort = False

        if len(recently_deceased_lst) > 0:
            print(f'\nUS36: Recently deceased:\n{pt_recently_deceased}\n')
        return pt_recently_deceased



    def walk_down_family_tree(self, family, descendant_lst) -> None:
        '''Recursive method for finding all descendants'''
        for child_id in self._family_dt[family].children:
            descendant_lst.append(child_id)
            for fam in self._individual_dt[child_id].fams:
                self.walk_down_family_tree(fam, descendant_lst)


    def US37_list_recent_survivors(self) -> None:
        '''List all living spouses/descendants of people who died in last 30 days'''
        recently_deceased_lst = self.find_deceased_within30days()

        pt_survivors: PrettyTable = PrettyTable(field_names=['Recently Deceased ID', 'Recently Deceased Name', 'Surviver ID', 'Surviver Name', "Relationship to Deceased"])

        for d_id, name, _ in recently_deceased_lst:
            for spousefamid in self._individual_dt[d_id].fams:
                if d_id == self._family_dt[spousefamid].wife_id:
                    spouseid = self._family_dt[spousefamid].husband_id
                else:
                    spouseid = self._family_dt[spousefamid].wife_id
                
                if self._individual_dt[spouseid].living:
                    if self._family_dt[spousefamid].divorce_date != 'NA':
                        Prefix = "Ex-"
                    else:
                        Prefix = ""
                    pt_survivors.add_row([d_id, name, spouseid, self._individual_dt[spouseid].name, Prefix+"Spouse"])
                
                d_lst = list()
                self.walk_down_family_tree(spousefamid, d_lst)
                for descendant in d_lst:
                    if self._individual_dt[descendant].living:
                        pt_survivors.add_row([d_id, name, descendant, self._individual_dt[descendant].name, "Descendant"])

        pt_survivors.sortby = "Recently Deceased ID"

        if len(recently_deceased_lst) > 0:
            print(f"US37: Survivors of recently deceased:\n{pt_survivors}")
        return pt_survivors

                  
    def Determine_multiple_birth(self, famc):
        multiple_birth_set = set()
        child_lst = list()
        for child in list(famc):
            child_lst.append(self._individual_dt[child])

            # Compare each sibling against eachother, ensuring that siblings aren't compared with themselves.
            for i in range (len(child_lst)):
                for j in range (i+1, len(child_lst)):
                    # if birthdate not provided, then skip
                    if type(child_lst[i].birth) == str or type(child_lst[j].birth) == str:
                        continue

                    # Subtract birthdates. If the difference is one day or less, then both are part of same multiple birth
                    diff_days = abs((child_lst[i].birth - child_lst[j].birth).days)
                    if diff_days <= 1:
                        multiple_birth_set.add(child_lst[i])
                        multiple_birth_set.add(child_lst[j])

        return multiple_birth_set



    def US32_list_multiple_births(self)->None:
        ''' 
        List all multiple births
        A multiple birth is 2 or more offspring born in the same birth event. Normally they are born within seconds 
        of eachother. In case of complications it could be hours. Because they are not born precisely at the same time,
        it is possible for twins to be born on different days, years, centuries, etc.
        e.g. twin 1 born at 11:59:30 on DEC 31st 1999 and twin 2 born 30 seconds later on JAN 1st 2000.
        We will make an assumption that a multiple birth occurred if sibblings are born within 1 day of eachother.
        '''
        multiple_births_pt: PrettyTable = PrettyTable(field_names = ['Family ID', 'Child ID', 'Child Name', 'Child Birth Date'])
        multiple_birth_set = set()

        # Go through each and every family
        for fam in self._family_dt.values():
            temp = self.Determine_multiple_birth(fam.children)
            multiple_birth_set.update(temp)

        for child in multiple_birth_set:
            multiple_births_pt.add_row([str(child.famc), child.id, child.name, child.birth])

        if len(multiple_birth_set) > 0:
            multiple_births_pt.sortby = 'Family ID'
            print(f"\nUS32: Multiple Births:\n{multiple_births_pt}")
        return multiple_births_pt




    def US33_list_orphans(self)->None:
        '''
        List all orphaned children (both parents dead and child < 18 years old).
        If an individual has no parents listed, they won't be listed as an orphan. 
        Individuals will be listed regardless of whether they are living or dead.
        '''

        orphan_pt: PrettyTable = PrettyTable(field_names = ['Family ID (as child)', 'Individual ID', 'Name']) 
        num_pt_entries = 0
        for person in self._individual_dt.values():

            # Only orphan if parents are dead. If no parents are listed, skip this individual.
            if len(person.famc) == 0:
                continue

            # If we can't determine an age, skip that person. Otherwise, check for age requirement
            if type(person.age) != str and person.age < 18:

                # Loop through all famc families. We only expect one, but it may be possible for a child
                # to be present in multiple families if they are adopted. Here we are defining an orphan
                # as a child < 18 years old who has no living parents, biological or not.
                orphan = True

                for family in person.famc:
                    mother_id = self._family_dt[family].wife_id
                    father_id = self._family_dt[family].husband_id
                    if self._individual_dt[mother_id].living or self._individual_dt[father_id].living:
                        orphan = False
                
                if orphan:
                    orphan_pt.add_row([person.famc or "None", person.id, person.name])
                    num_pt_entries += 1

        if num_pt_entries > 0:
            orphan_pt.sortby = 'Individual ID'
            print(f"\nUS33: List Orphans:\n{orphan_pt}")
        return orphan_pt


    def US24_unique_families_by_spouses(self) -> List[str]:
        '''Identifies multiple families that have the same spouses and marriage date'''

        list_of_families: List[Family] = self.US24_set_list_of_families()
        output: List[str] = list()

        while True:
            if len(list_of_families) == 0: break
            family_ids_with_matching_spouses_and_marriage_date = list()
            
            family_being_compared: Family = list_of_families.pop(0)
            detail_for_family_being_compared = [family_being_compared.husband_name, family_being_compared.wife_name, family_being_compared.marriage_date]
            family_ids_with_matching_spouses_and_marriage_date.append(family_being_compared.id)

            for fam in list_of_families:
                if [fam.husband_name, fam.wife_name, fam.marriage_date] == detail_for_family_being_compared:
                    family_ids_with_matching_spouses_and_marriage_date.append(fam.id)

            if len(family_ids_with_matching_spouses_and_marriage_date) > 1:
                anomaly_message: str = self.US24_set_output_message(family_ids_with_matching_spouses_and_marriage_date, detail_for_family_being_compared)
                print(anomaly_message)
                output.append(anomaly_message)

            for family in list_of_families:
                if family.id in family_ids_with_matching_spouses_and_marriage_date:
                    list_of_families.remove(family)

        return output

    def US24_set_list_of_families(self) -> List[Family]:
        '''Traverses through the _family_dt to extract only the families that have husband name, wife name, and marriage date all poulated, and puts them in a list'''
        
        list_of_families: List[Family] = list()

        for family in self._family_dt.values():
            if family.husband_id == 'TBD' or family.wife_id == 'TBD' or family.marriage_date == 'NA':
                continue
            else:
                list_of_families.append(family)

        return list_of_families

    def US24_set_output_message(self, list_of_family_ids: List[str], family_detail: List[str]) -> str:
        '''Sets up the output message for US24'''

        family_ids: str = ', '.join(list_of_family_ids)
        husband: str = family_detail[0]
        wife: str = family_detail[1]
        marriage_date: str = family_detail[2]

        return f'ANOMALY: US24: Families {family_ids}, have the same spouses and marriage date: Husband: {husband}, Wife: {wife}, Marriage Date: {marriage_date}'

    def US25_unique_first_names_in_families(self) -> None:
        '''Traverses through the _family_dt and checks each family's children to see if multiple children have the same name and birth date'''
        
        output: List[str] = list()

        for family_id, children in self.US25_set_list_of_children_in_a_family():
            family_id: str = family_id
            list_of_children_in_family: List[Individual] = children
        
            while True:
                if len(list_of_children_in_family) == 0: break
                child_ids_with_matching_name_and_birth_date: List[str] = list()

                child_being_compared: Individual = list_of_children_in_family.pop(0)
                detail_for_child_being_compared: List[str] = [child_being_compared.name, child_being_compared.birth]
                child_ids_with_matching_name_and_birth_date.append(child_being_compared.id)

                for child in list_of_children_in_family:
                        if [child.name, child.birth] == detail_for_child_being_compared:
                            child_ids_with_matching_name_and_birth_date.append(child.id)
                
                if len(child_ids_with_matching_name_and_birth_date) > 1:
                    anomaly_message: str = self.US25_set_output_message(child_ids_with_matching_name_and_birth_date, detail_for_child_being_compared, family_id)
                    print(anomaly_message)
                    output.append(anomaly_message)
                            
                for child in list_of_children_in_family:
                    if child.id in child_ids_with_matching_name_and_birth_date:
                        list_of_children_in_family.remove(child)

        return output

    def US25_set_list_of_children_in_a_family(self) -> Iterator[List[Individual]]:
        '''Traverses through the _family_dt to extract only the families that have multiple children'''

        children_in_family: List[Individual] = list()

        for family in self._family_dt.values():
            if len(family.children) <= 1:
                continue
            else:
                for child_id in family.children:
                    children_in_family.append(self._individual_dt[child_id])
                
                yield family.id, children_in_family
                children_in_family = list()

    def US25_set_output_message(self, list_of_child_ids: List[str], child_detail: List[str], family_id: str):
        '''Sets up the output message for US24'''

        child_ids: str = ', '.join(list_of_child_ids)
        family_id: str = family_id
        name: str = child_detail[0]
        birth_date: str = child_detail[1]

        return f'ANOMALY: US25: Individuals {child_ids} from family {family_id}, have the same name and birth date: Name: {name}, Birth Date: {birth_date}'

    def date_diff_days_ignore_year(self, date1, date2):
        ''' Returns the difference in days. Ignores year in comparison'''
        new_date_1 = datetime.date(date1.year, date1.month, date1.day)
        new_date_2 = datetime.date(date1.year, date2.month, date2.day)
        day_delta = (new_date_2 - new_date_1).days # difference results in datetime.timedelta 
        return day_delta

    def list_upcoming_birthdays(self):
        '''Finds all living people in a GEDCOM file whose birthdays occur in the next 30 days '''
        result = list()
        for person in self._individual_dt.values():
            if type(person.birth) != datetime.date:
                # Invalid entry. Birth date never logged, so skip this individual.
                continue
            if not person.living:
                # Deceased, skip this person
                continue

            day_delta = self.date_diff_days_ignore_year(datetime.date.today(), person.birth)

            if day_delta < 0:
                # Well, birthday has already passed this year... 
                continue
            elif day_delta <= 30:
                result.append([person.id, person.name, person.birth, day_delta])
        return result


    def US38_print_upcoming_birthdays(self) -> None:
        '''Lists all living people in a GEDCOM file whose birthdays occur in the next 30 days '''
        upcoming_bday_lst = self.list_upcoming_birthdays()

        pt_upcoming_bdays: PrettyTable = PrettyTable(field_names=['ID', 'Name', "Birth Date", "Days Until"])

        for id, name, birthdate, delta in upcoming_bday_lst:
            pt_upcoming_bdays.add_row([id, name, birthdate, delta])

        pt_upcoming_bdays.sortby = "Days Until"
        pt_upcoming_bdays.reversesort = False

        if len(upcoming_bday_lst) > 0:
            print(f'\nUS38: Upcoming Birthdays:\n{pt_upcoming_bdays}\n')
        return pt_upcoming_bdays


    def list_upcoming_anniversaries(self):
        '''
        Finds all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days.
        Divorced couples are not included.
        '''
        result = list()
        for family in self._family_dt.values():
            if type(family.marriage_date) != datetime.date:
                # Invalid entry. marriage date never logged, so skip this individual.
                continue
            if not self._individual_dt[family.husband_id].living or not self._individual_dt[family.wife_id].living:
                # One of the spouses are deceased, skip this family
                continue

            if family.divorce_date != 'NA':
                # Divorced couple, so skip this family
                continue

            day_delta = self.date_diff_days_ignore_year (datetime.date.today(), family.marriage_date)

            if day_delta < 0:
                # Well, anniversary has already passed this year... 
                continue
            elif day_delta <= 30:
                result.append([family.id, day_delta])
        return result


    def US39_print_upcoming_anniversaries(self) -> None:
        '''List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days '''
        upcoming_aday_lst = self.list_upcoming_anniversaries()

        pt_upcoming_adays: PrettyTable = PrettyTable(field_names=['Family ID', 'Husband Name', 'Husband ID', "Wife Name", "Wife ID", "Marriage Date", "Days Until"])

        for id, delta in upcoming_aday_lst:
            f = self._family_dt[id]
            pt_upcoming_adays.add_row([id, f.husband_name, f.husband_id, f.wife_name, f.wife_id, f.marriage_date, delta])

        pt_upcoming_adays.sortby = "Days Until"
        pt_upcoming_adays.reversesort = False

        if len(upcoming_aday_lst) > 0:
            print(f'\nUS39: Upcoming Anniversaries:\n{pt_upcoming_adays}\n')
        return pt_upcoming_adays





    def US26_corresponding_entries_individuals(self) -> str:
        '''Goes through each individual record and calls cross_reference_family() to cross reference the families that are identified in the family related tags of the
            individual record: "fams" and "famc". If there is inconsistency between the individual and the family, then an error message is collected and printed. 
        '''

        output: List[str] = list()

        for individual in self._individual_dt.values():
            error_messages: List[str] = self.US26_cross_reference_family(individual)
            
            if len(error_messages) > 0:
                for message in error_messages:
                    print(message)
                    output.append(message)

        return output

    def US26_cross_reference_family(self, individual: Individual) -> None:
        '''Cross references the families that are identified in the "fams" and "famc" tags of an individual record to make sure there is consistency with both
           the individual and family record'''

        error_messages: List[str] = list()

        for family_id in individual.fams:
            family_being_referenced: Family = self._family_dt[family_id]

            if individual.sex == 'M':
                if individual.id != family_being_referenced.husband_id:
                    error_messages.append(self.US26_error_message_for_individual(individual, family_being_referenced, 'husband error'))

            elif individual.sex == 'F':
                if individual.id != family_being_referenced.wife_id:
                    error_messages.append(self.US26_error_message_for_individual(individual, family_being_referenced, 'wife error'))

        for family_id in individual.famc:
            family_being_referenced: Family = self._family_dt[family_id]
 
            if individual.id not in family_being_referenced.children:
                error_messages.append(self.US26_error_message_for_individual(individual, family_being_referenced, 'child error'))

        return error_messages

    def US26_error_message_for_individual(self, individual: Individual, family_being_referenced: Family, type_of_error: str):
        '''Returns the appropriate spouse or child error message when inconsistencies are found in an Individual record'''

        if type_of_error == 'husband error':
            return f'ERROR: US26: Individual {individual.id}-{individual.name} and Family {family_being_referenced.id} show spouse inconsistency. {individual.id}-{individual.name} is identified as husband in {family_being_referenced.id}, but {family_being_referenced.id} identifies husband as {family_being_referenced.husband_id}-{family_being_referenced.husband_name}'

        elif type_of_error == 'wife error':
            return f'ERROR: US26: Individual {individual.id}-{individual.name} and Family {family_being_referenced.id} show spouse inconsistency. {individual.id}-{individual.name} is identified as wife in {family_being_referenced.id}, but {family_being_referenced.id} identifies wife as {family_being_referenced.wife_id}-{family_being_referenced.wife_name}'

        elif type_of_error == 'child error':
            if len(family_being_referenced.children) == 0:
                return f'ERROR: US26: Individual {individual.id}-{individual.name} and Family {family_being_referenced.id} show children inconsistency. {individual.id}-{individual.name} is identified as child in {family_being_referenced.id}, but {family_being_referenced.id} has no children.' 
            else:
                return f'ERROR: US26: Individual {individual.id}-{individual.name} and Family {family_being_referenced.id} show children inconsistency. {individual.id}-{individual.name} is identified as child in {family_being_referenced.id}, but {family_being_referenced.id} identifies children as {", ".join(family_being_referenced.children)}'

    def US26_corresponding_entries_families(self):
        '''Goes through each family record and calls cross_reference_individual() to cross reference the individuals that are identified as the husband, wife, or child
             in the family. If there is inconsistency between the family and any individual, then an error message is collected and printed. 
        '''

        output: List[str] = list()
        
        for family in self._family_dt.values():
            error_messages: List[str] = self.US26_cross_reference_individual(family)

            if len(error_messages) > 0:
                for message in error_messages:
                    print(message)
                    output.append(message)

        return output

    def US26_cross_reference_individual(self, family: Family) -> List[str]:
        '''Cross references the individuals that are identified in a family as husband, wife, or child to make sure there is consistency with both
           the family and individual record'''

        error_messages: List[str] = list()

        if family.husband_id != '':
            husband_being_referenced: Individual = self._individual_dt[family.husband_id]

            if family.id not in husband_being_referenced.fams:
                error_messages.append(self.US26_error_messages_for_family(family, husband_being_referenced, 'husband error'))
        
        if family.wife_id != '':
            wife_being_referenced: Individual = self._individual_dt[family.wife_id]

            if family.id not in wife_being_referenced.fams:
                error_messages.append(self.US26_error_messages_for_family(family, wife_being_referenced, 'wife error'))

        for child_id in family.children:
            child_being_referenced: Individual = self._individual_dt[child_id]

            if family.id not in child_being_referenced.famc:
                error_messages.append(self.US26_error_messages_for_family(family, child_being_referenced, 'child error'))

        return error_messages

    def US26_error_messages_for_family(self, family: Family, individual_being_referenced: Individual, type_of_error: str):
        '''Returns the appropriate spouse or child error message when inconsistencies are found in a family record'''

        if type_of_error == 'husband error':
            if len(individual_being_referenced.fams) == 0:
                return f'ERROR: US26: Family {family.id} and Individual {individual_being_referenced.id}-{individual_being_referenced.name} show spouse inconsistency. {family.id} identifies {individual_being_referenced.id}-{individual_being_referenced.name} as husband, but {individual_being_referenced.id}-{individual_being_referenced.name} is not married'
            else:
                return f'ERROR: US26: Family {family.id} and Individual {individual_being_referenced.id}-{individual_being_referenced.name} show spouse inconsistency. {family.id} identifies {individual_being_referenced.id}-{individual_being_referenced.name} as husband, but {individual_being_referenced.id}-{individual_being_referenced.name} is husband in {", ".join(individual_being_referenced.fams)}'

        if type_of_error == 'wife error':
            if len(individual_being_referenced.fams) == 0:
                return f'ERROR: US26: Family {family.id} and Individual {individual_being_referenced.id}-{individual_being_referenced.name} show spouse inconsistency. {family.id} identifies {individual_being_referenced.id}-{individual_being_referenced.name} as wife, but {individual_being_referenced.id}-{individual_being_referenced.name} is not married' 
            else:    
                return f'ERROR: US26: Family {family.id} and Individual {individual_being_referenced.id}-{individual_being_referenced.name} show spouse inconsistency. {family.id} identifies {individual_being_referenced.id}-{individual_being_referenced.name} as wife, but {individual_being_referenced.id}-{individual_being_referenced.name} is wife in {", ".join(individual_being_referenced.fams)}'

        if type_of_error == 'child error':
            return f'ERROR: US26: Family {family.id} and Individual {individual_being_referenced.id}-{individual_being_referenced.name} show child inconsistency. {family.id} identifies {individual_being_referenced.id}-{individual_being_referenced.name} as child, but {individual_being_referenced.id}-{individual_being_referenced.name} is child in {", ".join(individual_being_referenced.famc)}'

    def US29_list_deceased_individuals(self) -> Dict[str, str]:
        '''Prints a prettytable that contains all deceased individuals'''

        deceased_individuals: Dict[str, str] = defaultdict(dict) #key = individuals ID : value = {name:individuals name, death date:individual death date}

        pretty_table_for_deceased_individuals: PrettyTable = PrettyTable(field_names = ['ID', 'Name', 'Date of Death'])

        for individual_id, individual in self._individual_dt.items():
            if individual.living == False:
                deceased_individuals[individual_id]
                deceased_individuals[individual_id]['name'] = individual.name
                deceased_individuals[individual_id]['death date'] = individual.death_date
                pretty_table_for_deceased_individuals.add_row([individual_id, individual.name, individual.death_date])
        
        print(f'\nUS29: All Deceased Individuals\n{pretty_table_for_deceased_individuals}')

        return deceased_individuals


def main() -> None:
    '''Runs main program'''

    # If the caller included the gedcom file as a parameter, accept it!
    # otherwise, prompt the user for it.
    if len(sys.argv) < 2:
        file_name: str = input('Enter GEDCOM file name: ')
    else:
        file_name = sys.argv[1]
    
    gedcom: GedcomFile = GedcomFile()
    gedcom.read_file(file_name)
    gedcom.validate_tags_for_output()
    
    gedcom.update_validated_list()
    gedcom.parse_validated_gedcom()
    gedcom.family_set_spouse_names()
    
    gedcom.print_individuals_pretty()
    gedcom.print_family_pretty()


    #Sprint 1
    gedcom.US34_list_large_age_differences()
    gedcom.US35_list_recent_births()
    gedcom.US4_Marriage_before_divorce()
    gedcom.US21_correct_gender_for_role()
    gedcom.parse_individuals_based_on_living_and_marital_details() #US30
    gedcom.list_individuals_living_and_married() #US30
    gedcom.list_individuals_living_over_thirty_never_married() #US31
    gedcom.US03_birth_death()
    gedcom.US06_divorce_before_death()

    #Sprint 2
    gedcom.US2_birth_before_marriage()
    gedcom.US5_marriage_before_death()
    gedcom.US07_Death150()
    gedcom.US12_Mother_Father_older()
    gedcom.US28_list_all_siblings_from_oldest_to_youngest()
    gedcom.US36_list_recent_deaths()
    gedcom.US37_list_recent_survivors()
    # Note: US27 included in Individuals Table

    
    # Sprint 03
    gedcom.US32_list_multiple_births()
    gedcom.US33_list_orphans()
    gedcom.US19_married_first_cousins()
    gedcom.US22_uni_ids_indi_fam()
    gedcom.US23_uni_name_birth()
    gedcom.US24_unique_families_by_spouses()
    gedcom.US25_unique_first_names_in_families()
    gedcom.US16_male()

    # Sprint 04
    gedcom.US01_dates_b4_current()
    gedcom.US17_no_marraige_2_children()
    gedcom.US38_print_upcoming_birthdays()
    gedcom.US39_print_upcoming_anniversaries()
    gedcom.US14_multiple_births()
    gedcom.US15_siblings15()
    gedcom.US26_corresponding_entries_individuals()
    gedcom.US26_corresponding_entries_families()
    gedcom.US29_list_deceased_individuals()

if __name__ == '__main__':
    main()
