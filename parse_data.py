import vk
import pandas as pd

if __name__ == "__main__":
    token = open('config.env', 'r').readline().strip()
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)
    nakur = True
    offset = 0
    records = []
    while nakur:
        wall = vk_api.wall.get(v="5.21", domain="kalikfan", offset=offset, count=100)
        if len(wall["items"]) != 100:
            nakur = False
        for item in wall["items"]:
            records.append(item["text"])
        offset += 100
    print(len(records))
    df = pd.DataFrame(records, columns=['text'])
    df.to_csv('data.csv')


