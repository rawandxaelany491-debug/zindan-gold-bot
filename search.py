from knowledge import SNRZ_DATA


def search_snrz(question):
    question = question.strip().lower()

    for topic in SNRZ_DATA.values():

        keywords = topic.get("keywords", [])

        for keyword in keywords:
            if question == keyword.lower():
                return {
                    "text": topic["text"],
                    "image": topic.get("image")
                }

    return {
        "text": "❌ ببورە، ئەم بابەتە لە زانیارییەکانی SNRZ نەدۆزرایەوە.",
        "image": None
    }