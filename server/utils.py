# the below function may look confusing
# that's okay
# it requires knowlege of sqlalchemy
# the only way to get this knowlege is by reading the documentation and debugging
# just know it returns a normal dict
def model_to_dict(instance):
    return {column.name: str(getattr(instance, column.name)) for column in instance.__table__.columns}
