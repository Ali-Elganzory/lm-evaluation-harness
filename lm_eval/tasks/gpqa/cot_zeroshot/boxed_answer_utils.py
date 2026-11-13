import re


BOX_START = re.compile(r"\\boxed\s*\{")
WRAPPER = re.compile(r"\\(?:text|mathrm|mathbf)\s*\{(.*)\}", re.DOTALL)
CHOICE = re.compile(r"([A-D])|\(\s*([A-D])\s*\)", re.IGNORECASE)


def extract_boxed_answer(text):
    final = text.rsplit("</think>", 1)[-1]
    if "<think>" in final:
        return None
    starts = list(BOX_START.finditer(final))
    if not starts:
        return None
    start = starts[-1].end()
    depth = 1
    for end in range(start, len(final)):
        depth += (final[end] == "{") - (final[end] == "}")
        if depth == 0:
            value = final[start:end].strip()
            while wrapper := WRAPPER.fullmatch(value):
                value = wrapper[1].strip()
            match = CHOICE.fullmatch(value)
            return (match[1] or match[2]).upper() if match else None
    return None


def process_results(doc, results):
    answer = extract_boxed_answer(results[0])
    return {
        "exact_match": int(answer == doc["answer"].strip("()")),
        "format_compliance": int(answer is not None),
    }
