from flask import Flask, render_template, request
from SQL.queries import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/dive')
def dive():
    table_names = query_get_table_names(Server1)

    max_id = max(query_get_last_id_value(Server1, table)
                 for table in table_names)  # global max id of record in any of the 4 tables

    data = {}
    for table in table_names:
        data[table] = query_get_data_by_id(Server1, table, max_id)

    return render_template('dive.html', data=data, max_id=max_id)


@app.route('/all_dives')
def all_dives():
    table_names = query_get_table_names(Server1)

    data = {}
    for table in table_names:
        data[table] = query_get_data_from_table(Server1, table)

    return render_template('all_dives.html', data=data)


@app.route('/combat')
def data_option1():
    data = query_get_data_from_table(Server1, 'combat')
    columns = data[0]  # Column names
    rows = data[1:]  # Data rows
    return render_template('data/combat.html', columns=columns, data=rows)


@app.route('/currency_gained')
def data_option2():
    data = query_get_data_from_table(Server1, 'currency_gained')
    columns = data[0]
    rows = data[1:]
    return render_template('data/currency_gained.html', columns=columns, rows=rows)


@app.route('/objectives_completed')
def data_option3():
    data = query_get_data_from_table(Server1, 'objectives_completed')
    columns = data[0]
    rows = data[1:]
    return render_template('data/objectives_completed.html', columns=columns, rows=rows)


@app.route('/samples_gained')
def data_option4():
    data = query_get_data_from_table(Server1, 'samples_gained')
    columns = data[0]
    rows = data[1:]
    return render_template('data/samples_gained.html', columns=columns, rows=rows)


@app.route('/input_combat')
def data_option5():
    return render_template('inputs/input_combat.html')


@app.route('/input_currency_gained')
def data_option6():
    return render_template('inputs/input_currency_gained.html')


@app.route('/input_objectives_completed')
def data_option7():
    return render_template('inputs/input_objectives_completed.html')


@app.route('/input_samples_gained')
def data_option8():
    return render_template('inputs/input_samples_gained.html')


@app.route('/submit_data_combat', methods=['POST'])
def submit_data_combat():
    # Extract form data
    id_ = query_get_last_id_value(Server1, 'combat')
    if id_ is None:
        id_ = 1
    else:
        id_ = int(id_) + 1

    kills = request.form['kills']
    accuracy = request.form['accuracy']
    shots_fired = request.form['shots_fired']
    deaths = request.form['deaths']
    stims_used = request.form['stims_used']
    accidentals = request.form['accidentals']
    samples_extracted = request.form['samples_extracted']
    stratagems_used = request.form['stratagems_used']
    melee_kills = request.form['melee_kills']
    times_reinforcing = request.form['times_reinforcing']
    friendly_fire_damage = request.form['friendly_fire_damage']
    distance_travelled = request.form['distance_travelled']

    # Insert data into the database
    # THIS LITTLE "_" ON TIMES REINFORCING WILL BE THE DEATH OF ME
    query_put_row(Server1, 'combat',
                  id=id_,
                  kills=int(kills),
                  accuracy=float(accuracy),
                  shots_fired=int(shots_fired),
                  deaths=int(deaths),
                  stims_used=int(stims_used),
                  accidentals=int(accidentals),
                  samples_extracted=int(samples_extracted),
                  stratagems_used=int(stratagems_used),
                  melee_kills=int(melee_kills),
                  times_reinforcing_=int(times_reinforcing),
                  friendly_fire_damage=int(friendly_fire_damage),
                  distance_travelled=int(distance_travelled))

    return 'Combat data submitted successfully'


@app.route('/submit_data_currency_gained', methods=['POST'])
def submit_data_currency_gained():
    id_ = query_get_last_id_value(Server1, 'currency_gained')
    if id_ is None:
        id_ = 1
    else:
        id_ = int(id_) + 1
    requisition = request.form['requisition']
    medals = request.form['medals']
    xp = request.form['xp']

    # Insert data into the database
    query_put_row(Server1, 'currency_gained',
                  id=id_,
                  requisition=int(requisition),
                  medals=int(medals),
                  xp=int(xp))

    return 'Currency gained data submitted successfully'


# This one doesn't work for some reason
@app.route('/submit_data_objectives_completed', methods=['POST'])
def submit_data_objectives_completed():
    id_ = query_get_last_id_value(Server1, 'objectives_completed')
    if id_ is None:
        id_ = 1
    else:
        id_ = int(id_) + 1
    main_objectives = request.form['main_objectives']
    optional_objectives = request.form['optional_objectives']
    helldivers_extracted = request.form['helldivers_extracted']
    outposts_destroyed_light = request.form['outposts_destroyed_light']
    outposts_destroyed_medium = request.form['outposts_destroyed_medium']
    outposts_destroyed_heavy = request.form['outposts_destroyed_heavy']
    mission_time_remaining = request.form['mission_time_remaining']

    # Insert data into the database
    query_put_row(Server1, 'objectives_completed',
                  id=id_,
                  main_objectives=int(main_objectives),
                  optional_objectives=int(optional_objectives),
                  helldivers_extracted=int(helldivers_extracted),
                  outposts_destroyed_light=int(outposts_destroyed_light),
                  outposts_destroyed_medium=int(outposts_destroyed_medium),
                  outposts_destroyed_heavy=int(outposts_destroyed_heavy),
                  mission_time_remaining=mission_time_remaining)

    return 'Objectives completed data submitted successfully'


@app.route('/submit_data_samples_gained', methods=['POST'])
def submit_data_samples_gained():
    # Extract form data
    id_ = query_get_last_id_value(Server1, 'samples_gained')
    if id_ is None:
        id_ = 1
    else:
        id_ = int(id_) + 1
    green_samples = request.form['green_samples']
    orange_samples = request.form['orange_samples']
    violet_samples = request.form['violet_samples']

    # Insert data into the database
    query_put_row(Server1, 'samples_gained',
                  id=id_,
                  green_samples=int(green_samples),
                  orange_samples=int(orange_samples),
                  violet_samples=int(violet_samples))

    return 'Samples gained data submitted successfully'


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
