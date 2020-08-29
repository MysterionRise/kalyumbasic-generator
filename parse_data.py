import vk
import pandas as pd

import settings


def read_data(output_f: str):
    session = vk.Session(access_token=settings.VK_AUTH_TOKEN)
    vk_api = vk.API(session)
    nakur = True
    group_domain = "kalikfan"
    offset = 0
    records = []
    group = vk_api.groups.getById(v="5.21", group_ids=group_domain)[0]
    group_id = "-" + str(group["id"])  # Group id must starts with "-"

    while nakur:
        wall = vk_api.wall.get(v="5.21", domain=group_domain, offset=offset, count=100)

        if len(wall["items"]) != 100:
            nakur = False
        for item in wall["items"]:
            text = item["text"]
            # Skip ads
            if "#калик_рекламик" in text or "://" in text:
                continue
            records.append(item["text"])

            post_id = str(item["id"])
            comments_nakur = True
            comments_offset = 0
            post_comments = []
            while comments_nakur:
                get_comments = vk_api.wall.getComments(v="5.21", owner_id=group_id, post_id=post_id, need_likes=1, count=100, offset=comments_offset)
                post_comments += get_comments["items"]
                if len(get_comments["items"]) != 100:
                    comments_nakur = False
                comments_offset += 100

            # Filter comments by likes count:
            post_comments = sorted(post_comments, key=lambda k: k["likes"]["count"], reverse=True)
            # Add most popular comments
            for comment in post_comments[:3]:
                comment_text = comment["text"]
                # In case of answers to comment or links
                if "[id" in comment_text or "://" in comment_text:
                    continue
                records.append(comment_text)
        offset += 100
    print(len(records))
    df = pd.DataFrame(records, columns=['text'])
    df.to_csv(output_f)


if __name__ == "__main__":
    read_data('data.csv')
