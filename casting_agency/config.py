import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

"""
this setup file generated by The Configration Of Auth0 and Their Tokens 
"""
auth0_config = {
    "AUTH0_DOMAIN" : "m2k.us.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "movie",
    "CALLBACK_URL":"http://127.0.0.1:5000/",
    "CLIENT_ID":"mjDSnhJ7FmMyGB2bXYfiAStHX5huaSDy"
}



"""
DATABASE Connection and Configrations throught Postgress and my sql server
"""
database_setup = {
   "database_name" : "casting_db",#database Name here
   "user_name" : "postgres", # default postgres user name
   "password" : "admin", # if applicable. If no password, just type in None
   "port" : "localhost:5432" # default postgres port
}

# bearer_tokens = {
#     "casting_assistant" : "Bearer ",
#     "executive_producer" : "Bearer ",
#     "casting_director" : "Bearer "
# }