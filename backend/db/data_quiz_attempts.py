from datetime import datetime, timedelta

now = datetime.now()

# Last five days, quiz 1, score 1-5
data_quiz_attempts = [
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": now - timedelta(days=0),
        "score": 5,
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": now - timedelta(days=1),
        "score": 4,
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": now - timedelta(days=2),
        "score": 3,
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": now - timedelta(days=3),
        "score": 2,
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": now - timedelta(days=4),
        "score": 1,
    }
]

# March
data_quiz_attempts += [
    {
        "quiz_id": 2,
        "user_id": 2,
        "attempted_at": datetime(2025, 3, 20),
        "score": 0,
    },
    {
        "quiz_id": 2,
        "user_id": 2,
        "attempted_at": datetime(2025, 3, 20),
        "score": 0,
    },
    {
        "quiz_id": 2,
        "user_id": 2,
        "attempted_at": datetime(2025, 3, 20),
        "score": 3,
    },
    {
        "quiz_id": 2,
        "user_id": 3,
        "attempted_at": datetime(2025, 3, 20),
        "score": 3,
    },
    {
        "quiz_id": 2,
        "user_id": 3,
        "attempted_at": datetime(2025, 3, 20),
        "score": 3,
    },
]

# January
data_quiz_attempts += [
    {
        "quiz_id": 3,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 25),
        "score": 4,
    },
    {
        "quiz_id": 5,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 25),
        "score": 4,
    },
    {
        "quiz_id": 7,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 25),
        "score": 4,
    },
    {
        "quiz_id": 9,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 25),
        "score": 4,
    },
    {
        "quiz_id": 11,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 25),
        "score": 4,
    },
]

# February
data_quiz_attempts += [
    {
        "quiz_id": 3,
        "user_id": 3,
        "attempted_at": datetime(2025, 2, 18),
        "score": 2,
    },
    {
        "quiz_id": 5,
        "user_id": 3,
        "attempted_at": datetime(2025, 2, 18),
        "score": 2,
    },
    {
        "quiz_id": 7,
        "user_id": 3,
        "attempted_at": datetime(2025, 2, 18),
        "score": 2,
    },
    {
        "quiz_id": 9,
        "user_id": 3,
        "attempted_at": datetime(2025, 2, 18),
        "score": 2,
    },
    {
        "quiz_id": 11,
        "user_id": 3,
        "attempted_at": datetime(2025, 2, 18),
        "score": 2,
    },
]
