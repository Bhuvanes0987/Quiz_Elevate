
import os
def evaluate_answers(answers):
    # Simple local scoring stub. Replace with Ollama API calls as needed.
    results = []
    for a in answers:
        qid = a.get('question_id')
        resp = a.get('response','')
        qtype = a.get('qtype','mcq')
        correct = a.get('correct_answer')
        score = 0
        max_score = 1
        feedback = ''
        if qtype == 'mcq':
            if correct and resp == correct:
                score = 1; feedback='Correct'
            else:
                feedback='Incorrect'
        elif qtype == 'fill':
            if correct and isinstance(correct, str) and correct.lower() in resp.lower():
                score = 1; feedback='Correct (fuzzy)'
            else:
                feedback='Check answer'
        else:
            score = 1; feedback='Evaluated (placeholder)'
        results.append({'question_id': qid, 'score': score, 'max_score': max_score, 'feedback': feedback})
    return results
