import re
import vk
import pandas as pd

import settings

TEXT = "text"
ITEMS = "items"
API_VERSION = "5.21"
GROUP_DOMAIN = "kalikfan"
PARSE_COUNT = 100  # Count of posts/comments at request
LIKES_THRESHOLD = 10
URL_REGEX = r"[a-zA-Z]+\.[a-zA-Z]+"


def scrap_data_from_source(output_f: str):
    vk_api = vk.API(vk.Session(access_token=settings.VK_AUTH_TOKEN))
    nakur = True
    offset = 0
    records = []
    group = vk_api.groups.getById(v=API_VERSION, group_ids=GROUP_DOMAIN)[0]
    group_id = "-" + str(group["id"])  # Group id must starts with "-"

    while nakur:
        wall = vk_api.wall.get(v=API_VERSION, domain=GROUP_DOMAIN, offset=offset, count=PARSE_COUNT)

        if len(wall[ITEMS]) != PARSE_COUNT:
            nakur = False
        for item in wall[ITEMS]:
            text = item[TEXT]
            # Skip ads
            if "#калик_рекламик" in text or "://" in text or re.search(URL_REGEX, text):
                continue
            records.append(item[TEXT])

            post_id = str(item["id"])
            comments_nakur = True
            comments_offset = 0
            post_comments = []
            while comments_nakur:
                get_comments = vk_api.wall.getComments(v=API_VERSION, owner_id=group_id, post_id=post_id, need_likes=1,
                                                       count=PARSE_COUNT, offset=comments_offset)
                post_comments += get_comments[ITEMS]
                if len(get_comments[ITEMS]) != PARSE_COUNT:
                    comments_nakur = False
                comments_offset += PARSE_COUNT

            # Filter and sort comments by likes count:
            post_comments = [com for com in post_comments if com["likes"]["count"] > LIKES_THRESHOLD]
            post_comments = sorted(post_comments, key=lambda k: k["likes"]["count"], reverse=True)
            # Add most popular comments
            for comment in post_comments[:5]:
                comment_text = comment[TEXT]
                # In case of answers to comment or links
                if "[id" in comment_text or "://" in comment_text or re.search(URL_REGEX, comment_text):
                    continue
                records.append(comment_text)
        offset += PARSE_COUNT
    print(len(records))
    df = pd.DataFrame(records, columns=[TEXT])
    df.to_csv(output_f)


if __name__ == "__main__":
    scrap_data_from_source(output_f='data.csv')
