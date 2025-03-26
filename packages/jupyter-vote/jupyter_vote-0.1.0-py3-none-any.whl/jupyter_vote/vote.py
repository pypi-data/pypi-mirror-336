from IPython.display import IFrame

poll_iframe_args = {"width": "100%", "height": "450px"}
vote_iframe_args = {"width": "60%", "height": "400px"}
vote_id = None

_start_url = "https://www.vote.ac/start/index.php"
_vote_url = "https://www.vote.ac/index.php"


def choice(question: str, choices: int, *, multiple: bool = False, percent: bool = False, once: bool = False) -> IFrame:
    args = {"ft": question, "m": 1, "mc": int(multiple), "p": int(percent), "eid": int(once), "a": choices}
    return IFrame(src=_start_url, **poll_iframe_args, **args)


def yes_no(question: str, *, percent: bool = False, once: bool = False) -> IFrame:
    args = {"ft": question, "m": 2, "p": int(percent), "eid": int(once)}
    return IFrame(src=_start_url, **poll_iframe_args, **args)


def cloud(question: str, *, keep: bool = False, live: bool = False, wait: int = 60):
    args = {"ft": question, "m": 3, "fs": int(keep), "of": int(live), "w": wait}
    return IFrame(src=_start_url, **poll_iframe_args, **args)


def list(question: str, *, keep: bool = False, live: bool = False, wait: int = 60):
    args = {"ft": question, "m": 4, "fs": int(keep), "of": int(live), "w": wait}
    return IFrame(src=_start_url, **poll_iframe_args, **args)


def vote(id: str = None) -> IFrame:
    global vote_id
    id = id or vote_id
    args = {"id": id} if id else {}
    return IFrame(src=_vote_url, **vote_iframe_args, **args)
