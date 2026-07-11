from knowledge import SNRZ_DATA

def search_snrz(question):
    question = question.lower()

    for key, value in SNRZ_DATA.items():
        if key.lower() in question:
            return value

    return "ببورە، ئەم بابەتە لە SNRZ نەدۆزرایەوە."