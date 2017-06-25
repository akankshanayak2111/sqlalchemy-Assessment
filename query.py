"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?
# Answer: The data type is an object. This is just the query and not the actual value of the query.
# The actual value can be obtained by using .one(), .first(), or .all() .



# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?
# Answer: An association table is a table that connects two tables in a database, but does
# not have any useful information. It usually holds foreign keys which are primary keys for the tables it connects.
# It is indicated using the secondary argument while defining a relationship() between the two tables that it connects.
# An association table manages a many to many relationship.



# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = db.session.query(Brand).filter(Brand.brand_id == 'ram').one()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = db.session.query(Model).filter(Model.name == 'Corvette', Model.brand_id == 'che').all()

# Get all models that are older than 1960.
q3 = db.session.query(Model).filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = db.session.query(Model).filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = db.session.query(Brand).filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = db.session.query(Brand).filter( (Brand.discontinued != None) | (Brand.founded < 1950) ).all()

# Get all models whose brand_id is not ``for``.
q8 = db.session.query(Model).filter(Model.brand_id != 'for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    model_info = db.session.query(Model.name, Brand.name, Brand.headquarters).join(Brand).filter(Model.year == year).all()
    for model_name, brand_name, brand_headquarters in model_info:
        print "model_name: {}, brand_name: {}, headquarters: {}".format(model_name, brand_name, brand_headquarters)


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
        including their year, using only ONE database query."""

    brand_model = db.session.query(Brand.name, Model).join(Model).all()
    brand_dict = {}
    for brand, model in brand_model:
        if brand not in brand_dict:
            brand_dict[brand] = [(model.name, model.year)]
        else:
            brand_dict[brand] += [(model.name, model.year)]

    for brand, models in brand_dict.items():
        print "brand: {} ".format(brand)
        for model in models:
            print "model_name: {}, model_year:{}".format(model[0], model[1])
        print " \n"



def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    brands = db.session.query(Brand).filter(Brand.name.like('%'+ mystr +'%')).all()
    return brands


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    models = db.session.query(Model).filter(Model.year >= start_year, Model.year < end_year).all()
    return models
