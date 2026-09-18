from dataclasses import dataclass
from enum import Enum

import bisect
import random

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
    random.shuffle(attempts)

    sorted_attempts_by_subscription_id = {}

    for a in attempts:
        if a.occurred_at <= as_of:
            if a.subscription_id not in sorted_attempts_by_subscription_id:
                sorted_attempts_by_subscription_id[a.subscription_id] = []
            
            subscription_attempts = sorted_attempts_by_subscription_id[a.subscription_id]

            bisect.insort(subscription_attempts, a, key=lambda c: c.occurred_at)


    recovery_episodes = []
    for subscription_id, subscription_attempts in sorted_attempts_by_subscription_id.items():
        current_episode = None

        for a in subscription_attempts:
            if (current_episode == None):
                current_episode = {
                    "subscription_id": a.subscription_id,
                    "started_at": a.occurred_at,
                    "deadline": a.occurred_at + recovery_window_length,
                    "ended_at": None,
                    "status": EpisodeStatus.OPEN,
                    "failure_attempt_ids": [],
                    "recovery_attempt_id": None
                }
                recovery_episodes.append(current_episode)

            if a.result == AttemptResult.FAILURE:
                current_episode["failure_attempt_ids"].append(a.attempt_id)

                if current_episode["deadline"] < as_of:
                    current_episode["status"] = EpisodeStatus.EXPIRED
                    current_episode["ended_at"] = a.occurred_at
            else:
                current_episode["recovery_attempt_id"] = a.attempt_id
                current_episode["status"] = EpisodeStatus.RECOVERED
                current_episode["ended_at"] = a.occurred_at
                current_episode = None

    frozen_recovery_episodes = []
    for e in recovery_episodes:
        bisect.insort(frozen_recovery_episodes, RecoveryEpisode(**e), key=lambda c: c.subscription_id)

    print("*********************")
    print("AS OF", as_of)
    # print(len(frozen_recovery_episodes))
    # print(frozen_recovery_episodes)

    for e in frozen_recovery_episodes:
        print(e.subscription_id, e.status, e.failure_attempt_ids, e.recovery_attempt_id)

    return frozen_recovery_episodes


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
            occurred_at=0.5 * 86400,
            result=AttemptResult.FAILURE,
        ),
        Attempt(
            subscription_id='3',
            attempt_id='3',
            occurred_at=1.5 * 86400,
            result=AttemptResult.FAILURE,
        ),
        Attempt(
            subscription_id='1',
            attempt_id='4',
            occurred_at=1 * 86400,
            result=AttemptResult.FAILURE,
        ),
        Attempt(
            subscription_id='1',
            attempt_id='5',
            occurred_at=2 * 86400,
            result=AttemptResult.SUCCESS,
        ),
        Attempt(
            subscription_id='2',
            attempt_id='6',
            occurred_at=3 * 86400,
            result=AttemptResult.FAILURE,
        ),
    ]

    build_recovery_episodes(
        attempts=attempts,
        recovery_window_length=2 * 86400,
        as_of=0,
    )

    build_recovery_episodes(
        attempts=attempts,
        recovery_window_length=2 * 86400,
        as_of=1 * 86400,
    )

    build_recovery_episodes(
        attempts=attempts,
        recovery_window_length=2 * 86400,
        as_of=2 * 86400,
    )

    build_recovery_episodes(
        attempts=attempts,
        recovery_window_length=2 * 86400,
        as_of=3 * 86400,
    )


if __name__ == "__main__":
    run_examples()









