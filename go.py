"""
This call sends a message to the given recipient with vars and custom vars.
"""
from mailjet_rest import Client
import os
api_key = 'f2a5342ed960f5f9e5d164e68cc53c0c'#os.environ['MJ_APIKEY_PUBLIC']
api_secret = '9d8a18fa8ca82da86afeeaee21037c3a'#os.environ['MJ_APIKEY_PRIVATE']
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
		{
			"From": {
				"Email": "blazingkrane@gmail.com",
				"Name": "Housefree"
			},
			"To": [
				{
					"Email": "hussein.ibrahim6196@gmail.com",
					"Name": "passenger 1"
				}
			],
			"TemplateID": 4568001,
			"TemplateLanguage": True,
			"Subject": "Comfy Home Receipt",
			"Variables": {
    # "firstname": "Dear Customer",
    # "short_desc": "Studio",
    # "details": "(1 double bed) in Downtown San Francisco",
    # "quantity": "10",
    # "unitprice": "20.00",
    # "accommodation": "14.00",
    # "total": "170.00",
    # "new_points": "2",
    # "previous_points": "1",
    # "new_balance": "100",
    "name":"Haroskid"
  }
		}
	]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())