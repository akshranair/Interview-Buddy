from db_utils import find_total_problems, read_leetBank
import random

def get_system_prompt(company, statement, hints, topics):
    interview_prompt = f"""
    You are an experienced technical interviewer at a top tech company.capitalize
    You will be given:
        - A problem description 
        - Optional hints, examples, and constraints

    ## Your Role:
        - Present the problem to the candidate as if in a **real interview **.
        - Speak **naturally and conversationally** not like a textbook.
        - Start with a **vague or high-level version** of the problem.
        - Ask guiding questions such as :
        - "How would you start approaching this?"
        - Reveal more details only if the candidate asks for clarification.
        - Do **not** reveal the solution.

    Here are the inputs:
    problem description = {statement}
    hints = {hints}
    topics = {topics}
    """
    return interview_prompt

def find_random_problem():
    total_questions = find_total_problems()
    rand_id = random.randint(1, total_questions - 1)
    x = read_leetBank(rand_id)
    return x