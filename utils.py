import requests
from bs4 import BeautifulSoup
from resources import get_graphQL_uri, get_graphQL_context
from db_utils import delete_leetBank_data, write_leetBank, Build_LeetBank

def get_response(url, variables, query, headers):
    response = requests.post(
        url,
        json = {"variables":variables, "query":query},
        headers=headers,
        timeout=100)
    
    return response

def clean_html_text(html_text):
    text = BeautifulSoup(html_text, "html.parser").get_text()
    clean_text = text.replace('\n', ' ')
    clean_text = clean_text.replace('\xa0', ' ')
    return clean_text


def find_total_problems() -> int:
    url = get_graphQL_uri()
    limit = 1
    query, variables, headers = get_graphQL_context(limit)
    response = get_response(url,variables, query, headers)
    data = response.json()
    return data['data']['problemsetQuestionList']['total']

def get_all_problems():
    url = get_graphQL_uri()
    limit = find_total_problems()
    query, variables, headers = get_graphQL_context(limit)
    response = get_response(url,variables, query, headers)
    data = response.json()
    questions = data['data']['problemsetQuestionList']['questions']
    return questions

def save_all_leetcode():
    Build_LeetBank()
    delete_leetBank_data()
    questions = get_all_problems()
    for question in questions:
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

def fetch_problem_details_graphql(title_slug):
    """
    Fetch detailed problem information using GraphQL
    
    Args:
        title_slug (str): The problem's title slug (e.g., "two-sum")
    
    Returns:
        dict: Detailed problem info
    """
    try:
        url = get_graphQL_uri()
        
        # GraphQL query for detailed problem info
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                difficulty
                likes
                dislikes
                exampleTestcases
                topicTags {
                    name
                    slug
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                hints
                solution {
                    id
                    content
                }
                similarQuestions
            }
        }
        """
        
        variables = {"titleSlug": title_slug}
        
        headers = {
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/problems/{title_slug}/"
        }
        
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            question = data.get("data", {}).get("question", {})
            
            if question:
                return {
                    "questionId": question.get("questionId", ""),
                    "frontendQuestionId": question.get("questionFrontendId", ""),
                    "title": question.get("title", ""),
                    "description": question.get("content", ""),
                    "difficulty": question.get("difficulty", ""),
                    "likes": question.get("likes", 0),
                    "dislikes": question.get("dislikes", 0),
                    "exampleTestcases": question.get("exampleTestcases", ""),
                    "hints": question.get("hints", []),
                    "codeSnippets": question.get("codeSnippets", []),
                    "topicTags": question.get("topicTags", []),
                    "hasSolution": question.get("solution") is not None,
                    "similarQuestions": question.get("similarQuestions", "")
                }
    except Exception as e:
        print(f"Error fetching problem details via GraphQL: {e}")
        return None
