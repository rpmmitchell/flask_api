from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

#Users endpoint
class Users(Resource):
    #To do: hook this data up to mongoDB and retrieve from DB rather than local csv file
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data':data}, 200

    def post(self):
        parser = reqparse.RequestParser() # create our parser

        parser.add_argument('userId', required=True) # Add our Args
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args() #Adding these to dictionary

        # Setup our data frame with these values
        new_data = pd.DataFrame({
            'userId': args['userId'],
            'name': args['name'],
            'city': args['city'],
            'locations': [[]]
        })

        # Read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists"
            }, 401
        else:
            # Add the new values
            data = data.append(new_data, ignore_index=True)
            # Save back to CSV
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        data = pd.read_csv('users.csv')
        #What is this truly doing?
        if args['userId'] in list(data['userId']):
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            #Select our user
            user_data = data[data['userId'] == args['userId']]

            #Update the user location
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])

            #save back to csv
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                'message': f"'{args['userId']}' user not found"
            }, 404
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary

        data = pd.read_csv('users.csv')
        #What is this truly doing?
        if args['userId'] in list(data['userId']):
            #Select our user
            data = data[data['userId'] != args['userId']]

            #save back to csv
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                'message': f"'{args['userId']}' user not found"
            }, 404

    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('name', store_missing=False)  # name/rating are optional
        parser.add_argument('city', store_missing=False)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')
        # check that the location exists
        if args['userId'] in list(data['userId']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['userId'] == args['userId']]
            # if name has been provided, we update name
            if 'name' in args:
                user_data['name'] = args['name']
            # if rating has been provided, we update rating
            if 'city' in args:
                user_data['city'] = args['city']

            # update data
            data[data['userId'] == args['userId']] = user_data
            # now save updated data
            data.to_csv('user.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise we return 404 not found
            return {
                       'message': f"'{args['userId']}' user does not exist."
                   }, 404


#Locations endpoint
class Locations(Resource):
    def get(self):
        return 'I am in Location endpoint!'
    pass

api.add_resource(Users, '/users') #entry point for users
api.add_resource(Locations, '/locations')

if __name__ == '__main__':
    app.run()

