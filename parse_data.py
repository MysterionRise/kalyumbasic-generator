import logging
import re

import pandas as pd
from vk_api import VkApi

import settings

TEXT = "text"
ITEMS = "items"
API_VERSION = "5.130"
GROUP_DOMAIN = "kalikfan"
PARSE_COUNT = 100  # Count of posts/comments at request
LIKES_THRESHOLD = 10
URL_REGEX = r"[a-zA-Z]+\.[a-zA-Z]+"
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def get_group_id(vk_api):
    group = vk_api.groups.getById(v=API_VERSION, group_ids=GROUP_DOMAIN)[0]
    return "-" + str(group["id"])  # Group id must starts with "-"


def filter_ads(text):
    return "#калик_рекламик" not in text and "://" not in text and not re.search(URL_REGEX, text)


def scrap_data_from_source(output_f: str):
    """Scrap data from source and write it into a CSV file."""
    vk_session = VkApi(token=settings.VK_AUTH_TOKEN)
    vk_api = vk_session.get_api()
    offset = 0
    records = []
    is_data_remaining = True

    while is_data_remaining:
        wall = vk_api.wall.get(
            v=API_VERSION,
            domain=GROUP_DOMAIN,
            offset=offset,
            count=PARSE_COUNT,
        )
        if len(wall[ITEMS]) != PARSE_COUNT:
            is_data_remaining = False
        for item in wall[ITEMS]:
            text = item[TEXT]
            # Skip ads
            if filter_ads(text):
                records.append(item[TEXT])
                logging.info(f"Records count: {len(records)}")

        offset += PARSE_COUNT
    logging.info(f"Final records count: {len(records)}")
    df = pd.DataFrame(records, columns=[TEXT])
    df.to_csv(output_f)


if __name__ == "__main__":
    scrap_data_from_source(output_f="data.csv")
