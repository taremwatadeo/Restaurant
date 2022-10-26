from unicodedata import name
from add_data import session
from database_setup import MenuItem

v_Burgers = session.query(MenuItem).filter_by(name='Veggie Burger')

# for vBurger in v_Burgers:
#   print(vBurger.id)
#  print(vBurger.price)
# print(vBurger.restaurant.name)
# print('\n')

# urbanVBurger = session.query(MenuItem).filter_by(
#    id=8).one()  # prints on that item without looping through
#urbanVBurger.price = '$3.24'
# session.add(urbanVBurger)
# session.commit()

for vBurger in v_Burgers:
    if vBurger.price != '$3.24':
        vBurger.price = '$3.24'
        session.add(vBurger)
        session.commit()

    print(vBurger.id)
    print(vBurger.price)
    print(vBurger.restaurant.name)
    print('\n')
