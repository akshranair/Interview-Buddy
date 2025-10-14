from db_utils import Build_LeetBank, delete_leetBank_data, write_leetBank
from utils import get_all_problems, fetch_problem_details_graphql, clean_html_text
from tqdm import tqdm

def save_all_leetcode():
    print("**** Building LeetBank DB***")
    Build_LeetBank()
    print("*** Deleting existing LeetBank Data****")
    delete_leetBank_data()
    print("**** Fetching all problems from LeetCode ***")
    questions = get_all_problems()
    print(f"Total Problems are {len(questions)}")
    for question in tqdm(questions):
        if not question['paidOnly']:
            titleSlug = question['titleSlug']
            question_info = fetch_problem_details_graphql(titleSlug)

            leetcode_id =  question_info['frontendQuestionId']
            title = question['title']
            difficulty = question['difficulty']
            problem_statement = clean_html_text(question_info.get("description",""))
            url = f"https://leetcode.com/problems/{titleSlug}"
            topics = ", ".join(topic['name'] for topic in question_info['topicTags'])
            hints = ", ".join(hint for hint in question_info['hints'])

            write_leetBank(leetcode_id, problem_statement, title,titleSlug, difficulty, hints, topics, url) 


if __name__ == "__main__":
    save_all_leetcode()