import json
import os
import tweetpony

def authenticate():
	try:
		api = tweetpony.API("ukxWFXkJjCodYkC6OoLaFi4rU", "PYosUJ4VmIdz5O9pgHTndT10YFA4kBYcKITRyGKE1OWJBcfLYG")
		url = api.get_auth_url()
		print "Visit this URL to obtain your verification code: %s" % url
		verifier = raw_input("Input your code: ")
		api.authenticate(verifier)
	except tweetpony.APIError as err:
		print "Oh no! You could not be authenticated. Twitter returned error #%i and said: %s" % (err.code, err.description)
	else:
		auth_data = {'3248069732-LFDeuYNSo7UDRXGGa9vu3rCoQPJE45pdeZkMAmY': api.access_token, 'ye8eaw50OsDPyvCnuaYeRqSmcZobuCOi007p45CbhjnnC': api.access_token_secret}
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".auth_data.json"), 'w') as f:
			f.write(json.dumps(auth_data))
		print "Hello, @%s! You have been authenticated. You can now run the other example scripts without having to authenticate every time." % api.user.screen_name

def get_api():
	if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".auth_data.json")):
		authenticate()
	with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".auth_data.json"), 'r') as f:
		auth_data = json.loads(f.read())
	try:
		api = tweetpony.API("ukxWFXkJjCodYkC6OoLaFi4rU", "PYosUJ4VmIdz5O9pgHTndT10YFA4kBYcKITRyGKE1OWJBcfLYG", auth_data['3248069732-LFDeuYNSo7UDRXGGa9vu3rCoQPJE45pdeZkMAmY'], auth_data['ye8eaw50OsDPyvCnuaYeRqSmcZobuCOi007p45CbhjnnC'])
	except tweetpony.APIError as err:
		print "Oh no! You could not be authenticated. Twitter returned error #%i and said: %s" % (err.code, err.description)
	else:
		return api
	return False
