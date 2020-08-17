import requests
from datetime import datetime
from datetime import timedelta 



class ScoreCard:

	def __init__(self):
		self.matches_url = "https://cricapi.com/api/matches/"
		self.score_url   = "https://cricapi.com/api/cricketScore/"
		self.api_key     = "ukXEtxHYhaM2aNUDXQqQmVVqstx1"
		self.match_id = None

	def get_match_id(self):
		url_params = {"apikey":self.api_key}
		response = requests.get(self.matches_url,params=url_params)
		response_dict = response.json()
		#print(response_dict)
		team1 = None
		team2 = None
		id_flag = False
		for match in response_dict['matches']:
			#if (match['team-1']=='India' or match['team-2']=='India') and match['matchStarted']:
			today_date = (datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d")
			#today_date = date - timedelta(days=1)

			match_date = match['date'].split('T')[0]
			if today_date == match_date:
				self.match_id = match['unique_id']
				team1 = match['team-1']
				team2 = match['team-2']
				id_flag = True
				break
		if not id_flag:
			self.match_id = -1



		score = self.get_current_score(self.match_id)
		#print(score)
		send_data="Team1:"+team1+"\n"+"Team2:"+team2+"\n"+score
		return send_data


	def get_current_score(self,match_id):
		data = ""
		if match_id == -1:
			data = "No matches found today"
		else:
			url_params = {'apikey':self.api_key, 'unique_id':match_id}
			response = requests.get(self.score_url,params=url_params)
			response_dict = response.json()
			try:
				data = "Score : {} \nStatus :{}".format(response_dict['score'], response_dict['stat'])
			except KeyError as e:
				print(e)
		return data

if __name__=="__main__":
	score = ScoreCard()
	match_stats = score.get_match_id()
	print(match_stats)
	from twilio.rest import Client
	a_sid = "AC60be4b6c8412d7b3df18bbbd39faa133"
	auth_token = "68a84b68ef717b91c4c1a86a2d064c92"
	client = Client(a_sid,auth_token)
	#print(client)
	message = client.messages.create(body=match_stats, from_="whatsapp:+14155238886",to="whatsapp:+91 7521098331")

