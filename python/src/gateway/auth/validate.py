import os, requests

def token(request):
    if not "Authorizaiton" in request.headers:
        return None, ("Eksik Kimlik Bilgileri", 401)
    
    token = request.headers["Authorizaiton"]

    if not token:
        return None, ("Eksik Kimlik Bilgileri", 401)
    
    response =  requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorizaiton": token},
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)