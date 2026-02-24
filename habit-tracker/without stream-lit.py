import requests
import datetime
TOKEN="YOUR TOKEN"
USERNAME="YOUR USERNAME"
pixela_end_point="https://pixe.la/v1/users"
GRAPH_ID="graph1"
today=datetime.datetime().now()
user_params={
    "token":"ENTER YOUR TOKEN",
    "username":"ENTER YOUR USERNAME",
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}


# response=requests.post(url=pixela_end_point,json=user_params)

graph_endpoint=f"{pixela_end_point}/{USERNAME}/graphs"

graph_config={
    "id":"graph1",
    "name":"cycling",
    "unit":"km",
    "type":"float",
    "color":"ajisai"
}

headers={
    "X-USER-TOKEN":TOKEN
}

# response=requests.post(url=graph_endpoint,json=graph_config,headers=headers)

pixel_endpoint=f"{pixela_end_point}/{USERNAME}/graphs/{GRAPH_ID}"

pixel_config={
    "date":today.strftime("%Y%m%d"),
    "quantity":float(input("how many did you cycled today"))
}

# response=requests.post(url=pixel_endpoint,json=pixel_config,headers=headers)
# print(response.text)

update_endpoint=f"{pixela_end_point}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
update_config={
    "quantity":"10"
}

# response=requests.delete(url=update_endpoint,headers=headers)
# print(response.text)
