# Jupyter Vote

Jupyter vote is a simple [eduVote](https://www.eduvote.de/) integration for Jupyter notebooks using [`IFrame`s](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.IFrame).

## Creating Polls

EduVote offers four types of polls, which can be created using the following methods. The parameters to these methods map directly to the query parameters of the poll URL which in turn directly configure the poll. The methods return an IFrame so it should be the last line in a cell, or the output needs to be explicitly displayed with [`display`](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.display).

- `vote.choice(question: str, choices: int, *, multiple: bool = False, percent: bool = False, once: bool = False) -> IFrame`
- `vote.yes_no(question: str, *, percent: bool = False, once: bool = False) -> IFrame`
- `vote.cloud(question: str, *, keep: bool = False, live: bool = False, wait: int = 60) -> IFrame`
- `vote.list(question: str, *, keep: bool = False, live: bool = False, wait: int = 60) -> IFrame`

Parameters:

- `question`: The question to be asked in the poll.
- `choices`: The number of choices to be provided.
- `multiple`: Whether multiple choices can be selected.
- `percent`: Whether to show the results in percent as opposed to counts.
- `once`: Whether the poll can only be answered once per device.
- `keep`: Whether to keep the cloud or list from the previous poll.
- `live`: Whether to show the results immediately or only after a manual reveal.
- `wait`: The time in seconds to wait before a device can submit another answer.

## Voting

The interface for voting can be displayed using the `vote.vote(id: str = None) -> IFrame` method. The `id` parameter is optional and can be used to specify the teacher ID. If no ID is provided, the function attempts to use the ID stored in module level variable `vote.vote_id`.

## Notes

The first time a poll is made, the credentials need to be entered in the EduVote interface. The credentials can be saved and should persist even between sessions.

The size of the IFrames can be adjusted by changing the `vote.poll_iframe_args` and `vote.vote_iframe_args` dictionaries which are passed directly to the `IFrame` constructor.
