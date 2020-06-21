from O365 import Account, MSGraphProtocol, calendar
from calendar import Calendar
import datetime as dt

CLIENT_ID = '09b9898f-33aa-49a3-b789-ba7ff8dbab04'
SECRET_ID = '2ojw2Oa846EL~1itH~_26qv.k2GZ5-~N.q'
credentials = (CLIENT_ID, SECRET_ID)

account = None

def auth_init():

    callback = 'https://wittyapp.azurewebsites.net/api/HttpTrigger1'
    account = Account(credentials)
    url, states = account.con.get_authorization_url(requested_scopes=['Calendars.Read', 'Calendars.Read.Shared', 'Calendars.ReadWrite', 'Calendars.ReadWrite.Shared', 'User.Read'],
                                                   redirect_uri=callback)
    return url

def auth_end(url, m_state):
        
    account = Account(credentials)            

    # rebuild the redirect_uri used in auth_step_one
    callback = 'https://wittyapp.azurewebsites.net/api/HttpTrigger1'
   
    result = account.con.request_token(url, state=m_state, redirect_uri=callback)
    return result

def get_account():
    return Account(credentials)