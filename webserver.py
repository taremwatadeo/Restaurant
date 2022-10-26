from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import MenuItem, Restaurant
from add_data import session


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):

                restaurants_info = session.query(Restaurant).all()
                output = " "

                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output += "<html><body>"
                output += "<h1><a href ='/restaurants/new'>Make a new restaurant</a></h1>"
                for restaurant in restaurants_info:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br></br>"
                output += "</body></html>"
                # to turn string output into bytes(binary) the .encode removes the typeerror
                self.wfile.write(output.encode())
                # print(res)
                return

            if self.path.endswith('/edit'):
                restaurantIdPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIdPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = " "
                    output += "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIdPath
                    output += "<input name ='newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type ='submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output.encode())
                    print(output)

            if self.path.endswith('/delete'):
                restaurantIdPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIdPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = " "
                    output += "<html><body>"
                    output += "<h1> Continue and delete %s from Restaurants </h1>" % myRestaurantQuery.name

                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIdPath
                    output += "<input type ='submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output.encode())

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = " "
                output += "<html><body>"
                output += "<h1>Add new retaurant</h1>"

                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'></h2><input name ='newRestaurant' type = 'text'><input type='submit' value ='Create'> </form>"

                output += "</body></html>"

                # to turn string output into bytes(binary) the .encode removes the typeerror
                self.wfile.write(output.encode())
                # print(output)
                return

        except IOError:
            self.send_error(404, 'File not found' + self.path)

    def do_POST(self):

        if self.path.endswith('/delete'):
            restaurantIdPath1 = self.path.split("/")[2]
            myRestaurantQuery1 = session.query(
                Restaurant).filter_by(id=restaurantIdPath1).one()
            session.delete(myRestaurantQuery1)
            session.commit()

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

            print(myRestaurantQuery1.name + 'has been deleted')

        if self.path.endswith('/edit'):

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

            restaurantIdPath = self.path.split("/")[2]

            myRestaurantQuery = session.query(
                Restaurant).filter_by(id=restaurantIdPath).one()
            if myRestaurantQuery != []:
                myRestaurantQuery.name = messagecontent[0]
                session.add(myRestaurantQuery)
                session.commit()

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        if self.path.endswith('restaurants/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurant')

            addRestaurant = Restaurant(name=messagecontent[0])
            session.add(addRestaurant)
            session.commit()
            print('restaurant added')

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            # To redirect to the restaurant list
            self.send_header('Location', '/restaurants')
            self.end_headers()

      # output = " "
        #output += "<html><body>"
        #output += "<h2> Okay, how about this: </h2>"
        #output += "<h1> %s </h1>" % messagecontent[0]
        #output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
        #output += "</body></html>"

        # self.wfile.write(output.encode())
        # print(output)


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        # concatenating an int to string needs to first covert the int
        print('web server running on port %s ' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^c entered, stopping web server')
        server.socket.close()


if __name__ == '__main__':
    main()
