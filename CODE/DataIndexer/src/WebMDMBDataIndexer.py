import requests
import os
import json
import time

from src.MetaMapWrapper import MetaMapWrapper

CURRENT_DIR = os.path.dirname(__file__)
# Stored in Google drive due to large files
DATA_DIR = CURRENT_DIR + os.path.sep + 'posts_json'


# TODO: may be index again as many post may have failed to extract symptoms
# because of non-ASCII chars in it.
# TODO: maybe the file has group notion so the post should have group name?

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def index_json_file(file_path):
    # print(file_path)
    mmw = MetaMapWrapper()
    with open(file_path) as json_file:
        all_posts = json.load(json_file)
        failed_count = 0

        for post in all_posts:
            # wait for 2 seconds before every request
            time.sleep(1)
            try:
                preprocessed_review = {}
                preprocessed_review['post_url'] = post['post_url']
                post_obj = post['post']
                preprocessed_review['author'] = post_obj['author']
                preprocessed_review['post_time'] = post_obj['post_time']
                preprocessed_review['post_title'] = post_obj['post_title']
                post_content = post_obj['post_content']
                post_content = post_content.replace("\n", " ")
                preprocessed_review['post_content'] = post_content
                preprocessed_review['like_count'] = int(post_obj['like_count'])
                text_to_annotate = post_obj['post_title']
                text_to_annotate += ' ' + post_content
                preprocessed_review['tags'] = post_obj['tags']

                # put all comments together
                response_text = ''
                responses = post['responses']
                for response in responses:
                    resp_content = response['resp_content']
                    resp_content = resp_content.replace("\n", " ")
                    response_text += ' ' + resp_content
                text_to_annotate += ' ' + response_text
                preprocessed_review['response_text'] = response_text

                if len(text_to_annotate) > 0:
                    # important: remove non-ASCII chars as MetaMap causes tagging issue
                    text_to_annotate = remove_non_ascii(text_to_annotate)
                    extracted_data = mmw.annotate(text_to_annotate)
                    # don't index posts which does not have any symptoms mentioned in it as it does not add any value
                    if 'symptoms' not in extracted_data:
                        print('Ignored indexing: ' + str(post))
                        continue

                    if 'symptoms' in extracted_data:
                        preprocessed_review['symptoms'] = extracted_data['symptoms']
                    if 'diseases' in extracted_data:
                        preprocessed_review['diseases'] = extracted_data['diseases']
                    if 'diagnostics' in extracted_data:
                        preprocessed_review['diagnostic_procedures'] = extracted_data['diagnostics']

                # send request to server
                r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "webmd_mb"},
                                  json=preprocessed_review)
                if r.status_code == 500:
                    failed_count += 1

            except Exception as e:
                print("Exception while indexing this post: " + str(post))
                print('Exception message: ' + str(e))
                failed_count += 1

    print("total number of failed requests: " + str(failed_count))

    # send final index commit request
    r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "index_commit"},
                      json={"status": "ok"})
    print("Commit status: " + str(r.status_code))


if __name__ == "__main__":
    grouped_files = [
        'adhd-posts.json',
        'allerrgies-posts.json',
        'arthritis-posts.json',
        'asthma-posts.json',
        'bnsd-posts.json',
        'cancer-posts.json',
        'diabetes-posts.json',
        'digestive-posts.json',
        'earnosethroat-posts.json',
        'eye-posts.json',
        'fibromyalgia-posts.json',
        'heart-posts.json',
        'hepatitisc-posts.json',
        'hiv-posts.json',
        'kidney-posts.json',
        'lupus-posts.json',
        'mental-posts.json',
        'oralhealth-posts.json',
        'osteoporosis-posts.json',
        'painmanage-posts.json',
        'sclerosis-posts.json',
        'sexhealthstd-posts.json',
        'sleep-posts.json',
        'stroke-posts.json'
    ]

    for data_file in grouped_files:
        print('indexing: ' + data_file)
        index_json_file(DATA_DIR + os.path.sep + data_file)

    print("All the data files has been indexed!")