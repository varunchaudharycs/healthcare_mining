import requests
import os
import json
import time

from src.MetaMapWrapper import MetaMapWrapper

CURRENT_DIR = os.path.dirname(__file__)

# After 8710 every third file 1
start_index = 12000
end_index = 13500


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def index_json_file(file_path):
    mmw = MetaMapWrapper()

    with open(file_path) as json_file:
        data = json.load(json_file)
        failed_count = 0
        i = 0
        for post in data:
            # first index first 50000 reviews
            if i == end_index:
                break

            i += 1
            # skip already indexed data
            if i < start_index:
                continue

            # so that indexed corpus has variety of posts
            if i % 3 != 0:
                continue

            # wait for 3 seconds before every request
            # time.sleep(0.25)
            try:
                preprocessed_post = {}
                text_to_annotate = ''
                preprocessed_post['post_group'] = post['post_group']
                preprocessed_post['post_url'] = post['post_url']
                preprocessed_post['post_title'] = post['post_title']
                text_to_annotate += post['post_title']
                preprocessed_post['post_time'] = post['post_time']
                preprocessed_post['post_follow_count'] = post['post_follow_count']
                preprocessed_post['post_author'] = post['post_author']
                preprocessed_post['post_author_profile'] = post['post_author_profile']
                preprocessed_post['post_like_count'] = post['post_like_count']
                preprocessed_post['post_reply_count'] = post['post_reply_count']
                preprocessed_post['post_content'] = post['post_content']
                text_to_annotate += ' ' + post['post_content']

                comments = ''
                if 'post_comments' in post:
                    post_comments = post['post_comments']
                    for comment in post_comments:
                        comment_content = comment['comment_content']
                        comment_content = comment_content.replace("\n", " ")
                        comments += ' ' + comment_content
                    text_to_annotate += ' ' + comments
                preprocessed_post['post_comments'] = comments
                if len(text_to_annotate) > 0:
                    # important: remove non-ASCII chars as MetaMap causes tagging issue
                    text_to_annotate = remove_non_ascii(text_to_annotate)
                    extracted_data = mmw.annotate(text_to_annotate)

                    # don't index posts which does not have any symptoms mentioned in it as it does not add any value
                    # if 'symptoms' not in extracted_data:
                    #     print('Ignored indexing: ' + str(post))
                    #     continue

                    if 'symptoms' in extracted_data:
                        preprocessed_post['symptoms'] = extracted_data['symptoms']
                    if 'diseases' in extracted_data:
                        preprocessed_post['diseases'] = extracted_data['diseases']
                    if 'diagnostics' in extracted_data:
                        preprocessed_post['diagnostic_procedures'] = extracted_data['diagnostics']

                # send request to server
                r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "patient_info"},
                                  json=preprocessed_post)
                if r.status_code == 500:
                    failed_count += 1

            except Exception as e:
                print("Exception while indexing this forum post: " + str(post))
                print('Exception message: ' + str(e))
                failed_count += 1

    print("total number of failed requests: " + str(failed_count))

    # send final index commit request
    r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "index_commit"},
                      json={"status": "ok"})
    print("Commit status: " + str(r.status_code))


if __name__ == "__main__":
    # alternatively pass the path of crawled data file
    index_json_file(CURRENT_DIR + os.path.sep + "patient_info_forum_posts_content-1.json")
    # index_json_file(CURRENT_DIR + os.path.sep + "patient_info_forum_posts_content-2.json")
