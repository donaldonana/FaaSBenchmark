from profanity import profanity
import swiftclient
import json



def push(obj, ipv4):

    # Swift identifiant
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

	# Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)

    container = 'whiskcontainer'
 
    with open(obj, 'rb') as f:
        conn.put_object(container, obj, contents=f.read())
 
    return ("Ok")


def filter(text, char="*"):
    profanity.set_censor_characters("*")
    return profanity.censor(text)


def extract_indexes(text, char="*"):
    indexes = []
    in_word = False
    start = 0
    for index, value in enumerate(text):
        if value == char:
            if not in_word:
                # This is the first character, else this is one of many
                in_word = True
                start = index
        else:
            if in_word:
                # This is the first non-character
                in_word = False
                indexes.append(((start-1)/len(text),(index)/len(text)))
    return indexes
    
    
def main(args):
    
    message = "What a load of bullshit! You can't even get the simplest thing right."

    ipv4 = args.get("ipv4", "192.168.1.120")
    
    result = extract_indexes(filter(message))
    
    with open("index.json", "w") as f:
            json.dump(result, f)
            
    push("index.json", ipv4)

    return {"NumberofProfanities" : str(len(result))}

