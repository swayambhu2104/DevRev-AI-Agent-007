DEVREV_PROMPT = '''
Q: Find all tasks related to customer ABC Inc. and summarize them.

# solution in python:

def solution():
    # Find all tasks related to customer ABC Inc. and summarize them.
    PREV0 = works_list(
        created_by=["DEVU-123", "DEVU-456"],
    )
    PREV1 = summarize_objects(
        objects=PREV0
    )
    return PREV1

Q: %s

# solution in python:

'''.strip() + '\n\n\n'