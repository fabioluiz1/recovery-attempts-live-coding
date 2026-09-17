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
    recovery = RecoveryEpisode(
        subscription_id="2",
        started_at=0,
        deadline=15 * 86400,         # 15 days
        ended_at=None,
        status=EpisodeStatus.OPEN,   # also RECOVERY or EXPIRED
        failure_attempt_ids=('1',),
        recovery_attempt_id=None
    )

    print(recovery)


if __name__ == "__main__":
    run_examples()









