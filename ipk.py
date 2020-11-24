import socket
import json
import sys

server = "api.openweathermap.org"
try:
	city = sys.argv[2]
except Exception as e:
	print("Error: Missing arguments! (TIP: make run api_key=<API_KEY> city=<CITY>)")
	sys.exit(0)
	

#Function composes a HTTP request for the server
def makerequest(city):
    global server
    api = "/data/2.5/weather?q="
    units = "metric"
    api_key = sys.argv[1]   # api_key = "97fa3848fcb8fbf3d0acf1d3de840c15"
    request = "GET " + api + str(city) + "&APPID=" + api_key + "&mode=json&units=" + units + "\nHTTP / 1.1\n" + "Host: " + server + "\n\n"
    return request

# Function attempts a connection to the server and receives a message
def getconnetion(city):
    global server

    port = 80  # default port
    request_bytes = str.encode(makerequest(city))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server, port))
        s.sendall(request_bytes)
    except Exception as e:
        print("Could not establish connection! ", e)

    msg = s.recv(1024)
    return msg.decode("utf-8")

# Function takes to be displayed data from json format and puts them into dict
def make_dict_from_json(data):
    dictionary = json.loads(data)
    if dictionary.get("cod") != 200:
        print("Error " + str(dictionary.get("cod")) + ", " + dictionary.get("message"))
        if dictionary.get("cod") == "404":
            print("TIP: Cities with name longer than one word have to be written in quotes !")
        sys.exit(0)
    try:
        real_data = {
            "city": dictionary.get("name"),
            "description": dictionary.get("weather")[0].get("description"),   # weather is a list not a dict
            "temp": dictionary.get("main").get("temp"),
            "humidity": dictionary.get("main").get("humidity"),
            "pressure": dictionary.get("main").get("pressure"),
            "wind-s": dictionary.get("wind").get("speed"),
            "wind-d": dictionary.get("wind").get("deg"),
        }
    except Exception :
        print("Error: Missing key!")
        sys.exit(0)
    return real_data

# Function print out final output to stdout
def print_info(data):
    print(f'''{data['city']}
{data['description']}
temp:{data['temp']}°C
humidity:{data['humidity']}%
pressure:{data['pressure']} hPa
wind-speed: {data['wind-s']}km/h
wind-deg: {data['wind-d']}''')


if __name__ == '__main__':
    try:
        print_info(make_dict_from_json(getconnetion(city)))
    except Exception as e :
        print("Something went wrong ! ", e)
