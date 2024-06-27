from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask import Flask
from flask import make_response

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)
app = Flask(__name__)

class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    @app.route('/pets/<int:id>')
    def pet_by_id(id):
        pet = Pet.query.filter(Pet.id == id).first()

        if pet:
            body = pet.to_dict()
            status = 200
        else:
            body = {'message': f'Pet {id} not found.'}
            status = 404

        return make_response(body, status)

    @app.route('/species/<string:species>')
    def pet_by_species(species):
        pets = []
        for pet in Pet.query.filter_by(species=species).all():
            pets.append(pet.to_dict())
        body = {'count': len(pets),
                'pets': pets
                }
        return make_response(body, 200)

    def __repr__(self):
        return f'<Pet {self.id}, {self.name}, {self.species}>'
