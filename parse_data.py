import vk
import re
import pandas as pd

import settings


def read_data(output_f: str):
    session = vk.Session(access_token=settings.VK_AUTH_TOKEN)
    vk_api = vk.API(session)
    api_version = "5.21"
    group_domain = "kalikfan"
    url_regex = r"[a-zA-Z]+\.[a-zA-Z]+"
    nakur = True
    offset = 0
    parse_count = 100  # Count of posts/comments at request
    likes_needed = 10
    records = []
    group = vk_api.groups.getById(v=api_version, group_ids=group_domain)[0]
    group_id = "-" + str(group["id"])  # Group id must starts with "-"

    while nakur:
        wall = vk_api.wall.get(v=api_version, domain=group_domain, offset=offset, count=parse_count)

        if len(wall["items"]) != parse_count:
            nakur = False
        for item in wall["items"]:
            text = item["text"]
            # Skip ads
            if "#калик_рекламик" in text or "://" in text or re.search(url_regex, text):
                continue
            records.append(item["text"])

            post_id = str(item["id"])
            comments_nakur = True
            comments_offset = 0
            post_comments = []
            while comments_nakur:
                get_comments = vk_api.wall.getComments(v=api_version, owner_id=group_id, post_id=post_id, need_likes=1,
                                                       count=parse_count, offset=comments_offset)
                post_comments += get_comments["items"]
                if len(get_comments["items"]) != parse_count:
                    comments_nakur = False
                comments_offset += parse_count

            # Filter and sort comments by likes count:
            post_comments = [com for com in post_comments if com["likes"]["count"] > likes_needed]
            post_comments = sorted(post_comments, key=lambda k: k["likes"]["count"], reverse=True)
            # Add most popular comments
            for comment in post_comments[:5]:
                comment_text = comment["text"]
                # In case of answers to comment or links
                if "[id" in comment_text or "://" in comment_text or re.search(url_regex, comment_text):
                    continue
                records.append(comment_text)
        offset += parse_count
    print(len(records))
    df = pd.DataFrame(records, columns=['text'])
    df.to_csv(output_f)


if __name__ == "__main__":
    read_data('data.csv')
