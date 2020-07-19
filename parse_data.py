import vk
import pandas as pd

import settings


def read_data(output_f: str):
    session = vk.Session(access_token=settings.VK_AUTH_TOKEN)
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
    df.to_csv(output_f)


if __name__ == "__main__":
    read_data('data.csv')
