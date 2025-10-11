def get_graphQL_uri():
    return "https://leetcode.com/graphql"

def get_graphQL_context(skip):
    query = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                total: totalNum
                questions: data {
                    acRate
                    difficulty
                    freqBar
                    frontendQuestionId: questionFrontendId
                    isFavor
                    paidOnly: isPaidOnly
                    status
                    title
                    titleSlug
                    topicTags {
                        name
                        id
                        slug
                    }
                    hasSolution
                    hasVideoSolution
                }
            }
        }
        """
    variables = {
    "categorySlug": "",
    "skip": skip,
    "limit": 1,
    "filters": {}
    }

    headers = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/problemset/all/"
    }


    return query, variables, headers

def get_graphQL_slug_context(title_slug):
    variables = {"titleSlug": title_slug}

    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/problems/{title_slug}/"
    }

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

    return query, variables, headers
