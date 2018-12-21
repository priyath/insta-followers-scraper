from instapy import InstaPy
from instapy.util import smart_run
from instapy.util import get_relationship_counts
import argparse

#utility functions
def getPercentageCount(followers, percent):
	return int((followers*percent)/100)

# login credentials
insta_username = ''
insta_password = ''

# parse arguments and get account name and percentage of followers to be extracted
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--account", required=True,
	help="name of the account to be scraped for followers")
ap.add_argument("-p", "--percentage", required=True,
	help="percentage of followers to be scraped")

args = vars(ap.parse_args())

targetAccount = ""
percentage = 100

if args["account"]:
	targetAccount = format(args["account"])
if args["percentage"]:
	percentage = format(args["percentage"])

print '[INFO] Extracting ' + percentage + '% of the followers from ' + targetAccount

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True)

print '[INFO]: Logging in..'
with smart_run(session):
	#get follower, following count
	followers_count, following_count = get_relationship_counts(session.browser, targetAccount, session.logger)
	amount = getPercentageCount(int(followers_count),int(percentage))
	print '[INFO] Going to extract ' + str(amount) + ' followers out of ' + str(followers_count)

	followers_list = session.grab_followers(username=targetAccount, amount=amount, live_match=True, store_locally=False)

	print '[INFO]: Followers grabbed successfully. Saving to file..'

	result = ''
	for el in followers_list:
		result = result + el + '\n'

	with open("./" + str(targetAccount) + "_followers.txt", "w") as text_file:
    		text_file.write(result)

	print '[INFO]: Followers list successfully saved to ' + targetAccount + '_followers.txt'

