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
        abort(404)
    # if no error is not raised,
    else:
        # return the MdObj
        return mdObj


class MdObj_resource(Resource):
    '''
    This is the main API endpoint for the MdObj database
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
        an MdObj instance.
        '''
        # build a request parser
        self.reqparse = reqparse.RequestParser()
        # pull the user argument
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

        # if an expiration timestamp isn't set, add the default (now+30 days)
        if self.args['expire'] is None:
            expire = models.Set_Expiration()
        else:
            expire = int(self.args['expire'])

        # if no guid is provided
        if id is None:
            # create a new instance with a randomly generated guid
            return (models.MdObj.create(
                # user is always required for new objects
                user=self.args['user'],
                expire=expire,
            ), 201)
        # if a guid has been provided,
        else:
            try:
                # a user is not always provided on updates, remove it from args
                if self.args['user'] is None:
                    del self.args['user']
                # build the update query
                # - may throw a DoesNotExist (see except)
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
                ), 201)

    def delete(self, id=None):
        '''
        The DELETE method deletes a MdObj instance
        '''
        # build the delete query
        query = models.MdObj.delete().where(models.MdObj.guid == id)
        # execute the query
        query.execute()
        # return 204 response (no content)
        return ('', 204)


# build the API Blueprint
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
