from mailjet_rest import Client
def registration_email_sender(user):
    api_key = 'cdcb4ffb9ac758e8750f5cf5bf07ac9f'
    api_secret = '8ec6183bbee615d0d62b2c72bee814c4'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "kis.team.telerik@gmail.com",
                    "Name": "Recipe Sharing App"
                },
                "To": [
                    {
                        "Email": f"{user.email}",
                        "Name": f"{user.username}"
                    }
                ],
                "Subject": f"Registration to OnlyPans",
                "HTMLPart": f"<h3>Thanks for registering to the Recipe sharing app.</h3><br />May the delivery force be with you!",
                "CustomID": f"UserID: {user.id}"
            }
        ]
    }
    mailjet.send.create(data=data)

def update_password_email_sender(user, password, email):
    api_key = 'cdcb4ffb9ac758e8750f5cf5bf07ac9f'
    api_secret = '8ec6183bbee615d0d62b2c72bee814c4'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "kis.team.telerik@gmail.com",
                    "Name": "Recipe Sharing App"
                },
                "To": [
                    {
                        "Email": f"{email}",
                        "Name": f"{user.username}"
                    }
                ],
                "Subject": f"Password Updated",
                "HTMLPart": f"<h3>You have successfully updated your password to {password}</h3><br />May the delivery force be with you!",
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    mailjet.send.create(data=data)


def registration_email_sender_to_admin(user):
    api_key = 'cdcb4ffb9ac758e8750f5cf5bf07ac9f'
    api_secret = '8ec6183bbee615d0d62b2c72bee814c4'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "kis.team.telerik@gmail.com",
                    "Name": "Recipe Sharing App"
                },
                "To": [
                    {
                        "Email": "kis.team.telerik@gmail.com",
                        "Name": "Kis"
                    }
                ],
                "Subject": f"New Registration UserID:{user.id}",
                "HTMLPart": f"<h3>New user {user.username} with id:{user.id} registered to the app</h3><br />May the delivery force be with you!",
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    mailjet.send.create(data=data)

