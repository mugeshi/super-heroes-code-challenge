from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    super_name = db.Column(db.String(255))
    hero_powers = db.relationship('HeroPower', back_populates='hero')


class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    hero_powers = db.relationship('HeroPower', back_populates='power')
   
    
    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return value


class HeroPower(db.Model):
    __tablename__ = 'hero_power'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.String(255))
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError('Strength must be "Strong", "Weak", or "Average"')
        return value
