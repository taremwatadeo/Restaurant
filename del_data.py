from add_data import session
from database_setup import MenuItem

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()

print(spinach.restaurant.name)

session.delete(spinach)
session.commit()
