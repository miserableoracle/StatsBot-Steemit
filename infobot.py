# Imports 
from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
from steem.steemd import Steemd
from steembase.operations import Comment
import random, threading
import re
import time, sys, os, traceback, logging
import datetime 
from datetime import timedelta

# Global
PostingKey = os.environ.get('PostKey')
MainAuthor = os.environ.get('Author')
seednodes = [
	'https://api.steemit.com',
	'https://steemd.privex.io',
	'https://gtg.steem.house:8090',
	'https://steemd.steemitstage.com',
	'https://seed.bitcoiner.me',
	'https://gtg.steem.house:8090',
	'https://steemd.pevo.science',
	'https://rpc.steemliberator.com'
]
steem = Steem(seednodes, keys = PostingKey)
sd = Steemd(seednodes)
DebugAcc = os.environ.get('Debug_Author')
BlockInfo = Blockchain()
#nodes = configStorage.get('nodes')

class print_stats(threading.Thread):
	def __init__(self, url_string, summoner):
		threading.Thread.__init__(self)
		self.url_var = url_string
		self.initiator = summoner
		flag = 0
		global steem
		global DebugAcc
		global MainAuthor

	def run(self):
		self.GetStats()
	
	def Highest_Voting_Weight(self, activevotes):
		max_w = 0
		auth_name = ""
		for e in activevotes:
			if int(e['weight']) > max_w:
				max_w = int(e['weight'])
				auth_name = str(e['voter'])
		return auth_name
		
	def Lowest_Voting_Weight(self, activevotes):
		min_w = 1000000
		auth_name = ""
		for e in activevotes:
			if int(e['weight']) < min_w:
				min_w = int(e['weight'])
				auth_name = str(e['voter'])
		return auth_name
		
	def Get_Created_Date(self, created_string):
		format = "%d %m %Y %H:%M:%S"
		datetime_info = created_string.strftime(format)
		print(datetime_info)
		return "Hello"
		
	def GetStats(self):
		start_time = time.time()
		comment_string = ""
		postdetails = self.url_var.split("/")
		#postdetails = ['', '', 'ekklesiagora', 'on-poverty-gentrification-addiction-and-homelessness']
		#authortemp = '@ekklesiagora'
		print(postdetails)
		temp_dict = {'author': postdetails[2], 'permlink': postdetails[3]}
		getpost = Post(temp_dict, steem)
		print(getpost.items())
		totalvotes = len(getpost['active_votes'])
		comment_string += "<h3> Hello @"+self.initiator+" | Here are the stats of the <a href='https://steemit.com"+self.url_var+"'> Main Post </a></h3>"
		comment_string += "<h5> Total Votes: "+str(totalvotes)+"</h5>"
		
		if totalvotes == 0:
			pass
		else:
			if totalvotes == 1:
				high_weight = self.Highest_Voting_Weight(getpost['active_votes'])
				comment_string += "<h5> Highest Voting Weight: @"+str(high_weight)+"</h5>"
			else:
				high_weight = self.Highest_Voting_Weight(getpost['active_votes'])
				comment_string += "<h5> Highest Voting Weight: @"+str(high_weight)+"</h5>"
				low_weight = self.Lowest_Voting_Weight(getpost['active_votes'])
				comment_string += "<h5> Lowest Voting Weight: @"+str(low_weight)+"</h5>"
		
		comment_string += "<h5>Votes Details: </h5>"
		post_creation_date = self.Get_Created_Date(getpost['created'])
		print(comment_string)
		author_adj = postdetails[2].replace("@","")
		resteems = steem.get_reblogged_by(author_adj, postdetails[3])
		print(len(resteems))
		print("================================================================\n")
		comments_detail = steem.get_content_replies(author_adj, postdetails[3])
		print(len(comments_detail))
# MAIN
if __name__ == "__main__":
	while 1:
		try:
			for comment in steem.stream_comments():
				#match = re.search(r'(?i)(!)StatsBot(!*)', comment['body'])
				#if match is None:
				#	continue
				#else:
					#print("[Normal_Traces] StateBot Summoned. Initiating the process")
					if (comment.is_main_post()):
						continue
					else:
						url_string = comment['url'].split("#")
						print('https://steemit.com%s' %(url_string[0])) 
						thread_one = print_stats(url_string[0], comment['author'])
						thread_one.start()
						break
		except Exception as e:
			print("[Exception] Error Occurred @ Block No: ", BlockInfo.get_current_block_num())
			exc_type, exc_value, exc_traceback = sys.exc_info()
			print("[Exception] Type : ", exc_type)
			print("[Exception] Value : ", exc_value)
			print("[Exception] Traceback : ")
			traceback.print_tb(exc_traceback)
		break
