import requests
response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open("temp.jpg", 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'k2XDaxdXet3NUy7WX34njqSJ'},
    )
if response.status_code == requests.codes.ok:
        with open('nobackground.jpg', 'wb') as out:
            out.write(response.content)
else:
        print("Error:", response.status_code, response.text)