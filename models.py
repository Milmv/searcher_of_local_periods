from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    end = db.Column(db.DateTime, comment='Конец периодa')

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
