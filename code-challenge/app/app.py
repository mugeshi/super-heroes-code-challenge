#!/usr/bin/env python3
import os
from flask import Flask, make_response
from flask_migrate import Migrate
from flask import Blueprint, jsonify, request
from models import Hero, Power, HeroPower, db
from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "Welcome to a world where ordinary people become extraordinary heroes, where courage defies fear, and where hope conquers despair."

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_data)

# GET /heroes/:id
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404

    # Retrieve the powers associated with the hero using the 'hero_powers' relationship
    powers = [{'id': hero_power.power.id, 'name': hero_power.power.name, 'description': hero_power.power.description}
              for hero_power in hero.hero_powers]

    return jsonify({
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    })

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        power.description = data['description']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    else:
        return jsonify({'errors': ['validation errors']}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if 'strength' in data and 'power_id' in data and 'hero_id' in data:
        power = Power.query.get(data['power_id'])
        hero = Hero.query.get(data['hero_id'])

        if not power or not hero:
            return jsonify({'errors': ['validation errors']}), 400

        hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=data['strength'])
        db.session.add(hero_power)
        db.session.commit()

        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'errors': ['validation errors']}), 400

app.debug = True

if __name__ == '__main__':
    app.run(port=5555)





