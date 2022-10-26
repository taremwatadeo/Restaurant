from add_data import session
from database_setup import MenuItem, Restaurant

# session.query(MenuItem).all()

firstResult = session.query(Restaurant).all()

for res in firstResult:
    print(res.name)

items = session.query(MenuItem).all()
for item in items:
    print(item.name)
