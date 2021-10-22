import re

_INT_PATTERN = re.compile(r"^-?(0|([1-9][0-9]*))$")


def is_int(txt: str):
    return _INT_PATTERN.match(txt) is not None


class Matcher:
    def matches(self, other: int) -> bool:
        raise NotImplementedError()


class EqMatcher(Matcher):
    def __init__(self, val: int):
        self.val = val

    def matches(self, other: int) -> bool:
        return self.val == other


class LoEMatcher(Matcher):
    def __init__(self, val: int):
        self.val = val

    def matches(self, other: int) -> bool:
        return other <= self.val


class GoEMatcher(Matcher):
    def __init__(self, val: int):
        self.val = val

    def matches(self, other: int) -> bool:
        return other >= self.val


class RangeMatcher(Matcher):
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def matches(self, other: int) -> bool:
        return self.lower >= other >= self.upper


def get_first_match(value_to_match, candidates, get_matcher_from_candidate):
    for candidate in candidates:
        if get_matcher_from_candidate(candidate).matches(value_to_match):
            return candidate
    raise KeyError(f"Unable to find a match for {value_to_match}")


def get_first_set_match(value_to_match, candidates, get_matches_from_candidate):
    for candidate in candidates:
        if value_to_match in get_matches_from_candidate(candidate):
            return candidate
    raise KeyError(f"Unable to find a match for {value_to_match}")


def get_first_set_match_or_over_under_flow(
    value_to_match, candidates, get_matches_from_candidate
):
    try:
        return get_first_set_match(
            value_to_match, candidates, get_matches_from_candidate
        )
    except KeyError:
        min_candidate = min(
            candidates, key=lambda c: min(get_matches_from_candidate(c))
        )
        if value_to_match <= min(get_matches_from_candidate(min_candidate)):
            return min_candidate
        max_candidate = max(
            candidates, key=lambda c: max(get_matches_from_candidate(c))
        )
        if value_to_match >= max(get_matches_from_candidate(max_candidate)):
            return max_candidate
    raise KeyError(f"Unable to find a match for {value_to_match}")
