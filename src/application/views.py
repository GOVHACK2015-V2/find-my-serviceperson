import json, extraction

from flask import render_template, request

def home():
    some_other = {}
    some_other['name'] = 'Bob'

    some_person = {}
    some_person['name'] = 'Alice'

    some_list = (some_other, some_person)

    return render_template('old_things.html', name=json.dumps(some_person))

def index():
    return render_template('index.html')

def network():
    name    = request.form['person_name']
    people  = extraction.prepare_json_stack(name)

    return render_template('map.html', data=json.dumps(people))

def josh():
    things = []

    for x in request.args:
        things.append(x)

    return render_template('old_things.html')

def results():
    if request.method == 'POST':
        name=request.form['servicename']
        year=request.form['serviceyear']
        rank=request.form['servicerank']
        return render_template('results.html', name=name, year=year, rank=rank)

    # Results page visited without submitting a form
    # Return some sort of error?
    return 'cats'

def new_results():
    people = extraction.search_for_person('Herbert')

    return render_template('new_results.html', people=people)
