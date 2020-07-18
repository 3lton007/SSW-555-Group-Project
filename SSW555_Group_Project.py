from typing import Iterator, Tuple, IO, List, Dict, Set
from collections import defaultdict
import datetime
import os
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
                self._individual_dt[individual_id] = individual
                
            elif tag == "FAM":
                # Subsequent records will define a family
                family_record = True
                individual_record = False
                
                # Since this is the start - Create the Family!
                family: Family = Family()
                family_id: str = argument
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
    
    def US19_cousins(self):
        ''' First cousins cannot marry each other'''

        r = []

        for k, v in self._family_dt.items():
            hubby = v.husband_id
            wife = v.wife_id

            hubby_d = 'a'
            hubby_m = 'b'
            wife_d = 'c'
            wife_m = 'd'
            hubby_mgm = 'e'
            hubby_mgp = 'f'
            wife_mgp = 'g'
            wife_mgm = 'h'
            hubby_pgm = 'i'
            hubby_pgp = 'j'
            wife_pgp = 'k'
            wife_pgm = 'l'

            for k, v in self._family_dt.items():
                for x in v.children:
                    if x == hubby:
                        hubby_d = v.husband_id
                        hubby_m = v.wife_id

                        for k, v in self._family_dt.items():
                            for y in v.children:
                                if y == hubby_d:
                                    hubby_pgp = v.husband_id
                                    hubby_pgm = v.wife_id
                                    break

                        for k, v in self._family_dt.items():
                            for z in v.children:
                                if z == hubby_m:
                                    hubby_mgp = v.husband_id
                                    hubby_mgm = v.wife_id
                                    break

            for k, v in self._family_dt.items():
                for a in v.children:
                    if a == wife:
                        wife_d = v.husband_id
                        wife_m = v.wife_id

                        for k, v in self._family_dt.items():
                            for b in v.children:
                                if b == wife_d:
                                    wife_pgp = v.husband_id
                                    wife_pgm = v.wife_id
                                    break

                        for k, v in self._family_dt.items():
                            for c in v.children:
                                if z == wife_m:
                                    wife_mgp = v.husband_id
                                    wife_mgm = v.wife_id
                                    break 

        if (hubby_pgm == wife_pgm or hubby_mgm == wife_pgm or hubby_mgm == wife_mgm or hubby_pgm == wife_mgm):
            print(f"ERROR: US19: Family id:{k} Husband name:{v.husband_name}, husband id:{v.husband_id} and wife name:{v.wife_name},wife id:{v.wife_id} are first cousins")
            r.append(k)
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

            child_lst = list()
            for child in list(fam.children):
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


def main() -> None:
    '''Runs main program'''

    file_name: str = input('Enter GEDCOM file name: ')
    
    gedcom: GedcomFile = GedcomFile()
    gedcom.read_file(file_name)
    gedcom.validate_tags_for_output()
    
    gedcom.update_validated_list()
    gedcom.parse_validated_gedcom()
    gedcom.family_set_spouse_names()
    
    gedcom.print_individuals_pretty()
    gedcom.print_family_pretty()

    # Print out User Story output from hereon
    gedcom.US34_list_large_age_differences()
    gedcom.US35_list_recent_births()
    gedcom.US4_Marriage_before_divorce()
    gedcom.US21_correct_gender_for_role()
    gedcom.US2_birth_before_marriage()
    gedcom.US5_marriage_before_death()

    #US30 & #US31
    gedcom.parse_individuals_based_on_living_and_marital_details()
    gedcom.list_individuals_living_and_married()
    gedcom.list_individuals_living_over_thirty_never_married()
    
    gedcom.US03_birth_death()
    gedcom.US06_divorce_before_death()
    gedcom.US07_Death150()
    gedcom.US12_Mother_Father_older()
    gedcom.US16_male()
    gedcom.US19_cousins()
    gedcom.US28_list_all_siblings_from_oldest_to_youngest()
    gedcom.US36_list_recent_deaths()
    gedcom.US37_list_recent_survivors()

    
    # Sprint 03
    gedcom.US32_list_multiple_births()
    gedcom.US33_list_orphans()
    


if __name__ == '__main__':
    main()
