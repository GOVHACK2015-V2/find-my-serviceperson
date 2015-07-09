import sys, requests, json, pprint, unittest

# TODO move this into its own module
class Person(object):
    """Basic info on a service person

    name, rank, rel_units"""

    def __init__(self, name, rank=None, conflict=None, units=None, units_ids=None):
        """Constructor"""
        # TODO implement the rest of a Person
        self.name       = str(name)
        self.rank       = str(rank) if (rank != None) else rank
        # This isn't what should be stored ...
        self.conflict   = json.dumps(conflict)
        self.units_names= units
        self.units_ids  = units_ids

    def __str__(self):
        """Printing"""
        return self.name

"""These make queries to the AWM REST API (pardon the shouting)
"""
def query_awm_for_people(query):
    """Do query on awm API, returns list of Persons in results"""
    record_type     = ' AND record_type:people'

    url             = 'https://www.awm.gov.au/direct/data.php?key=ww1hack2015&q=%s%s'% (query, record_type)
    response_json   = requests.get(url)
    response_dict   = response_json.json()

    # TODO check response code before doing this
    people          = get_people_from_results(response_dict['results'])

    return people

def get_people_from_results(results):
    """returns list of Person objects in a list of query results"""
    people = []

    for result in results:
        name        = result['preferred_name']
        rank        = get_rank_from_result(result)
        conflict    = get_conflict_from_result(result)
        units       = get_units_names_from_result(result)
        units_ids   = get_units_ids_from_result(result)
        people.append(Person(name, rank, conflict, units, units_ids))

    return people

def search_for_person(name, rank=None, year=None):
    """Search for a person? returns list of people(dict)"""
    # TODO implement rank and year search
    query   = name
    results = query_awm_for_people(query)

    return results

def search_for_people_in_unit(unit_code):
    """returns list of people in units"""
    query   = 'related_units_id:%s' % unit_code
    results = query_awm_for_people(query)

    return results

""" These get things from results of query

    Could probably do some dependency injection here (look into it soon)
"""
def get_rank_from_result(result):
    """returns the rank of the person, or None"""
    rank = None

    try:
        rank = result['base_rank']
    except KeyError:
        """"""
        # print 'missing key'

    return rank

def get_conflict_from_result(result):
    """"""
    conflict = None

    try:
        conflict = result['conflict']
    except KeyError:
        """"""
        # print 'missing key'

    return conflict

def get_units_names_from_result(result):
    """"""
    units = []

    try:
        units = result['related_units']
    except KeyError:
        """"""
        # print 'missing key'

    return units

def get_units_ids_from_result(result):
    """"""
    units = []

    try:
        units = result['related_units_id']
    except KeyError:
        """"""
        # print 'missing key'

    return units

def get_ranks_in_unit(unit):
    """returns list of all ranks represented in that unit"""
    role_set    = set()

    for person in unit:
        role_set.add(person.rank)

    return list(role_set)

def get_people_from_unit_by_rank(unit, rank):
    """returns list of people with 'rank' in a 'unit' """
    people = []

    for person in unit:
        if person.rank == rank:
            people.append(person)

    return people

def prepare_json_stack():
    """do comment"""
    hardcoded_name  = 'William Edward James Smith'
    hardcoded_unit  = 'U20795'

    rank_list       = []

    unit            = search_for_people_in_unit(unit_code)

    for rank in get_ranks_in_unit(unit):
        people_in_rank = []
        people_in_unit =  get_people_from_unit_by_rank(unit, rank)
        for person in people_in_unit:
            people_in_rank.append(dict(name=person.name))

        rank_list.append(dict(name=rank, children=people_in_rank))

    list_of_units = []
    list_of_units.append(dict(name=hardcoded_unit, children=rank_list))

    root = dict(name=hardcoded_name, children=list_of_units)

    return root

def prepare_json_stack_2(person_name):
    """do comment"""
    people = query_awm_for_people(person_name)
    service_person  = None
    list_of_units   = []

    for person in people:
        if (person.name == person_name) and (person.units_ids != []):
            service_person = person

    for unit_code in person.units_ids:
        rank_list   = []
        unit        = search_for_people_in_unit(unit_code)

        for rank in get_ranks_in_unit(unit):
            people_in_rank = []
            people_in_unit = get_people_from_unit_by_rank(unit, rank)

            for person in people_in_unit:
                people_in_rank.append(dict(name=person.name))

            rank_list.append(dict(name=rank, children=people_in_rank))

        list_of_units.append(dict(name=unit_code, children=rank_list))

    root = dict(name=service_person.name, children=list_of_units)

    return json.dumps(root)

class ExtractionTest(unittest.TestCase):
    """Unit tests for Extraction methods"""

    def test(self):
        print 'wot'

# TODO real testing
# if __name__ == '__main__':
#   unittest.main()


# Fake testing in place of unit ones ...
# ######################################
name        = '*'
unit_code   = 'U20795'
rank        = 'Major'

people      = search_for_person(name)
# unit      = search_for_people_in_unit(unit_code)

# print query_awm_for_people(name)

# print people
# for person in people:
#   print person.units[0]

# print unit
# for person in unit:
#   print person.name

# print get_ranks_in_unit(unit)
# print get_people_from_unit_by_rank(unit, rank)

# print prepare_json_stack()
# pprint.pprint(prepare_json_stack())