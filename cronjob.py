from apscheduler.schedulers.blocking import BlockingScheduler
import json, requests, simplejson
from message_handling import get_stocks

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    
    companies = json.load(open('stocks.json'))
    get_stocks(companies)

    jsonFile = open("/tmp/updated_stocks.json", "w+")
    jsonFile.write(json.dumps(companies))
    jsonFile.close()

    print(companies)

sched.start()


# from message_handling import detailed_status
# from message_handling import find_text
# from apscheduler.schedulers.blocking import BlockingScheduler
# import json, requests, simplejson

# facebook_key = os.environ['facebook_api']
# api_key = os.environ['api_key']


# def daily_update_create_message():
#     companies = json.load(open('stocks.json'))

#     message = find_text('update_diario', 'useful')
#     message += detailed_status(companies)
    
#     r = requests.post("https://graph.facebook.com/v2.6/me/message_creatives",
#         params={"access_token": facebook_key},
#         data=json.dumps({
#             "messages":[
#                 {
#                     "dynamic_text": {
#                         "text": message
#                     } 
#                 }
#             ]
#         }),
#         headers={'Content-type': 'application/json'})
#     if r.status_code == 200:
#         j = simplejson.loads(r.content)
#         return str(j["message_creative_id"])
#     else:
#         return 0

# def daily_update_send_message(message_creative_id):
#     r = requests.post("https://graph.facebook.com/v2.6/me/broadcast_messages",
#         params={"access_token": facebook_key},
#         data=json.dumps({
#             "message_creative_id": message_creative_id,
#             "notification_type": "REGULAR"
#         }),
#         headers={'Content-type': 'application/json'})
#     print (r)

# sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=20, minute=30)

# def job_function():
#     print ("Starting cronjob")
#     string = daily_update_create_message()
#     daily_update_send_message(string)

# sched.start()