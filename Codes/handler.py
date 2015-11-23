from __future__ import with_statement
import logging
import urllib
try:
    import json
except ImportError:
    import simplejson as json
    
from django.conf import settings
from django.core.mail import send_mail

from piston.handler import BaseHandler
from piston.utils import rc
from piston import resource
import xmpp,random,string,sys
from sana.api.util import fail, succeed, get_logger, validate


SERVER = 'gcm.googleapis.com'
PORT = 5235
USERNAME = 'GCM Sender Id'
PASSWORD = 'API Key'
REGISTRATION_ID = 'Broker registration id'


def random_id():
  rid = ''
  for x in range(8): rid+=random.choice(string.ascii_letters + string.digits)
  return rid

def message_callback(session, message):
  global unacked_messages_quota
  gcm = message.getTags('gcm')
  if gcm:
    gcm_json =  gcm[0].getData()
    msg = json.loads(gcm_json)
    if not msg.has_key('message_type'):
      send({'to':msg['from'],
        'message_type':'ack',
        'message_id':msg['message_id']})
  elif msg['message_type'] == 'ack' or msg['message_type'] == 'nack':
    unacked_messages_quota+=1

def send(json_dict):
  template = ("<message><gcm xmlns='google:mobile:data'>{1}</gcm></message>")
  client.send(xmpp.protocol.Message(node=template.format(client.Bind.bound[0], json.dumps(json_dict))))

def flush_queued_messages():
  global unacked_messages_quota
  while len(send_queue) and unacked_messages_quota > 0:
    send(send_queue.pop(0))
    unacked_messages_quota -= 1

client = xmpp.Client('gcm.googleapis.com',debug=['socket'])
client.connect(server=(SERVER,PORT), secure=1, use_srv=False)
auth = client.auth(USERNAME,PASSWORD)
if not auth:
  logging.error("XMPP Auth failed")
  sys.exit(1)

client.RegisterHandler('message',message_callback)


class NotificationHandler(BaseHandler):
    ''' Handles notification requests. The field names which will be recognized 
    while handling the request:
        
        Allowed methods: GET, POST
    '''
    allowed_methods = ('GET','POST',)

    def create(self, request):
        request.full_clean()
        form = request.data
        
        try:  
          send_queue.append({'to':REGISTRATION_ID,
            'message_id': random_id(),
            'data' : str(form)
            )
        except Exception as e:
          logging.error("Sending XMPP Message failed : %s",e)
          return fail("XMPP Message send fail")
        return  True
    def read(self, request, notification_id=None):
        ''' Requests notifications cached and sent from this server '''
        pass
notification_resource = resource.Resource(NotificationHandler)
    

