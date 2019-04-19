'''
resources.guid - the API engine
This module contains the functions that power the API endpoints.
'''
from flask import abort, jsonify, Blueprint, url_for
from flask_restful import (
    Resource, Api, reqparse, fields, marshal, marshal_with)

import models

# marshalling fields - can be extended for various kinds of metadata
mdobj_fields = {
    'guid': fields.String,
    'expire': fields.Integer,
    'user': fields.String,
}


def get_mdobj_or_404(id):
    '''
    This function either gets an MdObj instance by ID, or raises a 404 error.
    '''
    try:
        # get the MdObj by ID
        mdObj = models.MdObj.get(models.MdObj.guid == id)
    # if the MdObj doesn't exist,
    except models.MdObj.DoesNotExist:
        # raise a 404 error
        abort(404, "Provided GUID not found")
    # if no error is not raised,
    else:
        # return the MdObj
        return mdObj


class MdObj_resource(Resource):
    '''
    This is the main API endpoint controller for the MdObj database

    Methods:
    GET
    Used to Retrieve (cRud) entries

    PUT
    Used to Create or Update (CrUd) entries

    DELETE
    Used to Delete (cruD) entries
    '''
    @marshal_with(mdobj_fields)
    def get(self, id):
        '''
        The GET method uses the @marshal_with decorator to return an MdObj
        instance, selected by ID, with a 200 status code, or it raises a 404.
        '''
        return (get_mdobj_or_404(id), 200)

    @marshal_with(mdobj_fields)
    def put(self, id=None):
        '''
        The PUT method uses the @marshal_with decorator to create or update
        an MdObj instance. The logic on when it does what is the most
        complicated for sure, but at a high level it goes something like this:

        if PUT was called with a GUID argument:
            Try to update the entry with that GUID
            if an entry doesn't exist to update, create it
        if PUT was called without an GUID argument:
            create a new entry from the arguments
        '''
        # build a request parser
        self.reqparse = reqparse.RequestParser()
        # pull the user arguments
        self.reqparse.add_argument(
            'user',
            required=False,
            help='Please provide a user with your request',
            location=['json', 'args', 'headers', 'data']
        )
        # pull the expire argument
        self.reqparse.add_argument(
            'expire',
            required=False,
            help='invalid expiration date, please use a UNIX timetamp',
            location=['json', 'args', 'headers', 'data']
        )
        # save args to the resource object
        self.args = self.reqparse.parse_args()

        # if an expiration timestamp isn't set,
        if self.args['expire'] is None:
            # add the default (now+30 days)
            expire = models.Set_Expiration()
        # if an expiration timestamp is set explicitly,
        else:
            try:
                # convert the argument to an integer
                expire = int(self.args['expire'])
            except ValueError:
                abort(
                    400,
                    "invalid expiration date, please use a UNIX timetamp")

        # if no guid is provided,
        if id is None:
            # create a new instance with a randomly generated guid
            # (generated by default if no guid is provided)
            return (models.MdObj.create(
                # user is always required for new objects
                user=self.args['user'],
                # either from the arugment, or 30 days from now by default
                expire=expire,
            ),
                # return 201: created
                201)
        # if a guid has been provided,
        else:
            # test it for validity
            if not models.validate_GUID(id):
                abort(400, "Provided GUID is not valid")
            try:
                # a user is not always provided on updates.
                # if it's not supplied in arguments,
                if self.args['user'] is None:
                    # remove it from args
                    del self.args['user']
                # build the update query and execute
                # NOTE may throw a DoesNotExist (see except)
                models.MdObj.update(
                    **self.args).where(models.MdObj.guid == id).execute()
                # return the updated model
                return (models.MdObj.get(models.MdObj.guid == id), 200)
            # if an object matching the guid is not found,
            except models.MdObj.DoesNotExist:
                # create a new one
                return (models.MdObj.create(
                    # user is always required to create
                    # could do *args here, but explicit is better
                    user=self.args['user'],
                    guid=id,
                    expire=expire
                ),
                    # return 201: created
                    201)

    def delete(self, id=None):
        '''
        The DELETE method deletes an MdObj instance
        '''
        # build the delete query
        query = models.MdObj.delete().where(models.MdObj.guid == id)
        # execute the query
        query.execute()
        # return 204 response (no content)
        return ('', 204)


# build the API Blueprint from resources.guid
mdObj_api = Blueprint('resources.guid', __name__)
# build the api object
api = Api(mdObj_api)
# add the guid endpoints
api.add_resource(
    MdObj_resource,
    '/guid/<string:id>',
    endpoint='guid_update_delete',
)
api.add_resource(
    MdObj_resource,
    '/guid',
    endpoint='guid_create',
)
