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
  a = extraction.prepare_json_stack() 
  extraction.pretty_print(a)
  return render_template('map.html', data=json.dumps(a))
  

def josh():
    a = extraction.prepare_json_stack() 
    print a
    
    return extraction.pretty_print(a)
#    return "cats"

def results():
	if request.method == 'POST':
		name=request.form['servicename']
		year=request.form['serviceyear']
		rank=request.form['servicerank']
		return render_template('results.html', name=name, year=year, rank=rank)
