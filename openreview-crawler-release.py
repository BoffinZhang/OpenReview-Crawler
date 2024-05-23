import os
import time
import openreview
import argparse

# set your login info
username = ""
password = ""

# API V1
client_v1 = openreview.Client(
    baseurl='https://api.openreview.net',
    username=username,
    password=password
)

# # API V2
# client_v2 = openreview.api.OpenReviewClient(
#     baseurl='https://api2.openreview.net',
#     username=username,
#     password=password
# )

def view_note(id, client):
    note = client.get_note(id=id)
    print(note)


def download_pdf(note_list, download_dir, client):
    for note in note_list:
        title = note.to_json()["content"]["title"]
        title = title.replace(":", "")

        print("Loading:", title)
        try:
            f = client.get_attachment(id=note.to_json()["id"], field_name='pdf')
            with open(os.path.join(download_dir, f'{title}.pdf'),'wb') as op: 
                op.write(f)
            time.sleep(1)

        except Exception as e:
            print("failed")

def get_accepted_note_list(conference_name, conference_year, client):
    note_list = client.get_all_notes(
                    content={"venueid":f"{conference_name}.cc/{conference_year}/Conference"}
                )
    if len(note_list) == 0:
        print("No note found! ")
        exit(0)
    return note_list


def filter_keywords(note_list, keyword) -> list:
    filtered_list = []
    for note in note_list:
        title = note.to_json()["content"]["title"]
        title = str(title).lower()
        if keyword in title:
            filtered_list.append(note)
    return filtered_list


def main():

    parser = argparse.ArgumentParser("Open Review Paper Crawler")
    parser.add_argument("--conference", "-c", type=str, default="ICLR", help="Support [ICLR, ICML, NeurIPS, ...]")
    parser.add_argument("--year", "-y", type=str, default="2024")
    parser.add_argument("--keyword", "-k", type=str, default="time series")
    parser.add_argument("--dir", "-d", type=str, default="./")
    configs = parser.parse_args()

    print(f"{configs.conference}-{configs.year}", f"keyword: {configs.keyword}")
    print(f"Donwload DIR: {configs.dir}")

    conference_name = configs.conference
    conference_year = configs.year
    keyword = configs.keyword

    download_dir = os.path.join(configs.dir, f"{conference_name}-{conference_year}")
    
    client = client_v1
    note_list = get_accepted_note_list(conference_name, conference_year, client)
    note_list = filter_keywords(note_list, keyword)
    print(f"Paper count: {len(note_list)}.")

    os.makedirs(download_dir, exist_ok=True)
    download_pdf(note_list, download_dir, client)

if __name__=="__main__":
    main()

