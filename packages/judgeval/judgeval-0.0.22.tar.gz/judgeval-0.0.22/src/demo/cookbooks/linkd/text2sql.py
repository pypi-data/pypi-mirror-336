"""
ClassifierScorer implementation for basic Text-to-SQL evaluation.

Takes a natural language query, a corresponding LLM-generated SQL query, and a table schema + (optional) metadata.
Determines if the LLM-generated SQL query is valid and works for the natural language query.
"""
from judgeval.scorers import ClassifierScorer
from judgeval import JudgmentClient
from judgeval.scorers.judgeval_scorers.classifiers.text2sql.text2sql_scorer import Text2SQLScorer

judgment_client = JudgmentClient()

print(judgment_client.push_classifier_scorer(Text2SQLScorer, slug="text2sql-eric-linkd"))
print(judgment_client.fetch_classifier_scorer("text2sql-eric-linkd"))
