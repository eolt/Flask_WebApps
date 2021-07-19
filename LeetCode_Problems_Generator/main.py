import bs4
from selenium.webdriver.support.ui import WebDriverWait

# Simple assignment
from selenium.webdriver import Safari

import requests
import random


def find_text(url, t):
    with Safari() as driver:
        WebDriverWait(driver, 10)
        driver.get(url)

        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')

        if t == 'problem':
            print(soup.find("div", {"class": "content__u3I1 question-content__JfgR"}).text)
        else:
            res = soup.find("div", {"class": "content__QRGW"})

            isAvailable = res.find("div").text[10:81] != 'This is not the real premium solution article ' \
                                                         'and is just a placeholder'

            if isAvailable:
                print(res.find("div").text[9:])
                return True

            return False


def main():
    url_Api = 'https://leetcode.com/api/problems/algorithms/'
    url_problems = 'https://leetcode.com/problems/'

    easy_questions = list()
    medium_questions = list()
    hard_questions = list()

    # dict_keys(['user_name', 'num_solved', 'num_total', 'ac_easy', 'ac_medium', 'ac_hard', 'stat_status_pairs',
    # 'frequency_high', 'frequency_mid', 'category_slug'])
    problems_json = requests.get(url_Api).json()
    # dict_keys(['stat', 'status', 'difficulty', 'paid_only', 'is_favor', 'frequency', 'progress'])
    questions = problems_json['stat_status_pairs']

    for question in questions:
        if question['paid_only'] is False:

            difficulty = question['difficulty']

            if difficulty['level'] == 1:
                easy_questions.append(question['stat'])
            elif difficulty['level'] == 2:
                medium_questions.append(question['stat'])
            elif difficulty['level'] == 3:
                hard_questions.append(question['stat'])

    random.shuffle(easy_questions)

    # dict_keys( ['question_id', 'question__article__live', 'question__article__slug',
    # 'question__article__has_video_solution', 'question__title', 'question__title_slug',
    # 'question__hide', 'total_acs', 'total_submitted', 'frontend_question_id', 'is_new_question'])

    title = easy_questions[0]['question__title']
    url = url_problems + easy_questions[0]['question__title_slug']

    print(title)
    print("Type: Easy")
    find_text(url, 'problem')

    print("Submit here : " + url)

    is_solution = False

    print("Solution")
    if easy_questions[0]['question__article__slug'] is not None and \
            easy_questions[0]['question__article__live'] is True:
        is_solution = find_text(url + '/solution', 'tacos')

    if not is_solution:
        print('Fiddlesticks! LeetCode has not posted a solution or it is not available for free.')
        print('You can view the discussions page to find if any one else has solved it.')
        print(url + "/discuss")
        print('\nOr feel free to seek your own sources for a solution.')


if __name__ == '__main__':
    main()
