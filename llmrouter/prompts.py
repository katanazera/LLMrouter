QA_PROMPT_TEMPLATE ="""
You are an expert in answer evaluation. Compare the model's response with the reference answer:
Question: {input}
Reference answer: {reference}
Model's answer: {output}

Respond with "correct" only if the model's answer STRICTLY matches the reference answer, and "incorrect" otherwise.
"""

CLASSIFY_PROMPT_TEMPLATE= """
You are classifyer assistant, you just need to classify query as either:
- 'application': questions related to applications, how to fill the form, any needs to apply,portfolio questions etc.
- 'entrance_exams' only if the question sincerely asks about exams:
their content, format, schedule,skill level for entrance exam,preparation,interviews, etc.
Exclude jokes, sarcastic comments, or fictional requests.Use 'other' if the message does not show real informational intent.
- 'syllabus_courses' questions related to syllabus,courses, schedules, languages of lectures,national exams,state exams
- 'internship' questions related to internship, where it goes, when it starts.
- 'other' other questions which doesnt match previous topics.
"""