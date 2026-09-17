from dataclasses import dataclass
from enum import Enum


class AttemptResult(Enum):
    FAILURE = "failure"
    SUCCESS = "success"


class EpisodeStatus(Enum):
    RECOVERED = "recovered"
    EXPIRED = "expired"
    OPEN = "open"


@dataclass(frozen=True)
class Attempt:
    attempt_id: str
    subscription_id: str
    occurred_at: int
    result: AttemptResult

@dataclass(frozen=True)
class RecoveryEpisode:
    subscription_id: str

    # Timestamp of the failure that started the episode.
    started_at: int

    # Timestamp when the episode expires if it is not recovered.
    deadline: int

    # Timestamp of recovery or expiration,
    # or None if the episode is still open.
    ended_at: int | None

    status: EpisodeStatus

    # Failure IDs in chronological order.
    failure_attempt_ids: tuple[str, ...]

    # The success that closed the episode, if one exists.
    recovery_attempt_id: str | None


def build_recovery_episodes(
    *,
    attempts: list[Attempt],
    recovery_window_length: int,
    as_of: int,
) -> list[RecoveryEpisode]:
    """
    Reconstruct recovery episodes from payment attempts.

    Parameters
    ----------
    attempts:
        An unordered collection of payment attempts.

    recovery_window_length:
        The positive duration of the recovery window, in seconds.

    as_of:
        Timestamp for which a snapshot of recovery episodes
        should be constructed.

    Returns
    -------
    A list of recovery episodes ordered by subscription_id, chronologically.

    Notes
    -----
    1. The same attempt_id may appear more than once.

    2. You may assume distinct attempts for the same subscription have
       different occurred_at values.

    3. A FAILURE starts a recovery episode if one is not already open.

    4. A SUCCESS during the recovery window recovers an open episode.
    """
    raise NotImplementedError


def run_examples() -> None:
    attempts = [
        Attempt(
            attempt_id='1',
            subscription_id='1',
            occurred_at=0,
            result=AttemptResult.FAILURE,
        ),
        Attempt(
            subscription_id='2',
            attempt_id='2',
            occurred_at=0,
            result=AttemptResult.FAILURE,
        ),
        Attempt(
            subscription_id='3',
            attempt_id='3',
            occurred_at=0,
            result=AttemptResult.SUCCESS,
        ),
        Attempt(
            subscription_id='1',
            attempt_id='4',
            occurred_at=2 * 86400,
            result=AttemptResult.FAILURE,
        ),
        Attempt(
            subscription_id='1',
            attempt_id='5',
            occurred_at=5 * 86400,
            result=AttemptResult.SUCCESS,
        ),
        Attempt(
            subscription_id='2',
            attempt_id='6',
            occurred_at=5 * 86400,
            result=AttemptResult.SUCCESS,
        ),
    ]

    # 1 Naive map
    # 1 Attempt -> 1 Episode (empty logic)

    recovery_episodes = [
        RecoveryEpisode(
            subscription_id=a.subscription_id,
            started_at=a.occurred_at,
            deadline=15 * 86400,         # 15 days
            ended_at=None,
            status=EpisodeStatus.OPEN,   # also RECOVERY or EXPIRED
            failure_attempt_ids=(),
            recovery_attempt_id=None
        ) for a in attempts
    ]

    print(recovery_episodes)


if __name__ == "__main__":
    run_examples()









