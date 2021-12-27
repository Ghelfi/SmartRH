def normalize_skill_list(skills: list[str]) -> list[str]:
    res = list(set([e.lower() for e in skills]))
    return res