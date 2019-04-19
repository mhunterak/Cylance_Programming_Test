'''
Python Developer Applicant Programming Test

by Maxwell Hunter 4/18/2019
for Cylance
'''
from flask import Flask
from flask_caching import Cache

import config
import models
# all the action happens here
from resources.guid import mdObj_api

# initialize the database
models.initialize()

# build the flask app
app = Flask(__name__)
# register the api blueprint
app.register_blueprint(mdObj_api)
# add caching
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
cache.init_app(app)


# add the index route to confirm the API is active,
# all the action happens in resources/guid.py
@app.route('/')
def my_guids():
    return "REST API Active"


if __name__ == '__main__':
    '''
    Runs the api server if name is main
    '''
    app.run(debug=config.DEBUG, host=config.HOST,
            port=config.PORT)  # pragma: no cover
