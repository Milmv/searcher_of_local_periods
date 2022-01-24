from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from services import change_date_to_datetime, change_datetime_to_unix, array_from_unix_range, \
    attribute_array_from_dictionary, datetime_array_from_unix_array, delete_duplicates, get_union_range, \
    array_of_uncontained

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Entity(db.Model):
    tablename = 'Entity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, comment='ID сущности')
    name = db.Column(db.String(256), comment='Название сущности')
    type = db.Column(db.Integer, comment='Тип')

    def __repr__(self):
        return '<Entity %r>' % self.name


class Period(db.Model):
    tablename = 'Period'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, comment='ID периодa')
    start = db.Column(db.DateTime, comment='Начало периодa')
    stop = db.Column(db.DateTime, comment='Конец периодa')

    def __repr__(self):
        return '<Period %r>' % self.id


class Period_entity(db.Model):
    tablename = 'Period_entity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, comment='ID поля')
    entity_id = db.Column(db.Integer, db.ForeignKey(Entity.id), comment='ID сущности')
    period_id = db.Column(db.Integer, db.ForeignKey(Period.id), comment='ID периодa')

    def __repr__(self):
        return '<Period_entity (%r, %r, %r)>' % (
            self.id, self.entity_id, self.period_id
        )


@app.route('/', methods=['GET', 'POST'])
@app.route('/create-request', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        start = change_date_to_datetime(request.form['start'])
        stop = change_date_to_datetime(request.form['stop'])
        name = request.form['name']
        type_entity = request.form['type']

        start_unix = change_datetime_to_unix(start)
        stop_unix = change_datetime_to_unix(stop)

        period = Period(start=start, stop=stop)
        entity = Entity(name=name, type=type_entity)

        periods = Period.query.filter_by(start=start, stop=stop).all()

        entities = Entity.query.filter_by(name=name, type=type_entity).all()

        array = array_from_unix_range(start_unix, stop_unix)
        if len(entities):
            period_entiies_for_request = db.session.query(Period_entity).filter(
                Period_entity.entity_id == entities[0].id).all()

            identity_array_from_periods = attribute_array_from_dictionary(period_entiies_for_request, 'period_id')

            required_periods = db.session.query(Period).filter(Period.id.in_(identity_array_from_periods)).all()

            time_array = get_union_range(required_periods)

            array_for_replicator = array_of_uncontained(array, time_array)
            datetime_array_for_replicator = datetime_array_from_unix_array(array_for_replicator)
        else:
            datetime_array_for_replicator = datetime_array_from_unix_array(array)

        if len(periods):
            period_id = periods[0].id

        if len(entities):
            entity_id = entities[0].id

        try:
            if not len(periods):
                db.session.add(period)
                db.session.commit()
                period_id = period.id

            if not len(entities):
                db.session.add(entity)
                db.session.commit()
                entity_id = entity.id

            period_entities = Period_entity.query.filter_by(period_id=period_id, entity_id=entity_id).all()

            if not len(period_entities):
                period_entity = Period_entity(period_id=period_id, entity_id=entity_id)
                db.session.add(period_entity)
                db.session.commit()

            return redirect(f"/response_period/{datetime_array_for_replicator}")
        except:
            return 'except'

    else:
        return render_template("index.html")


@app.route('/period_entity')
def period_entity__template():
    period_entities = Period_entity.query.all()
    return render_template("period_entity.html", period_entities=period_entities)


@app.route('/period')
def period_template():
    periods = Period.query.all()
    return render_template("period.html", periods=periods)


@app.route('/entity')
def entity_template():
    entities = Entity.query.all()
    return render_template("entity.html", entities=entities)


@app.route('/response_period/<arr>')
def response_period(arr):
    newArr = arr.replace('[', '').replace(']', '').split(',')
    return render_template("response.html", arr=newArr)


if __name__ == '__main__':
    app.run(debug=True)
