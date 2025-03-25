from datetime import datetime, timedelta

# Generate timestamps for the last 5 days
now = datetime.now()
dates = [now - timedelta(days=i) for i in range(5)]  # Changed to use datetime objects directly

data_quiz_attempts = [
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": dates[0],
        "score": 5,     # 100% - success - all correct
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": dates[1],
        "score": 4,     # 80% - success
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": dates[2],
        "score": 3,     # 60% - primary
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": dates[3],
        "score": 2,     # 40% - warning
    },
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": dates[4],
        "score": 1,     # 20% - danger
    }
]

data_quiz_attempts += [
    {
        "quiz_id": 1,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 4,
    },
    {
        "quiz_id": 2,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 4,
    },
    {
        "quiz_id": 3,
        "user_id": 2,
        "attempted_at": datetime(2025, 2, 1),
        "score": 4,
    },
    {
        "quiz_id": 5,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 2,
    },
    {
        "quiz_id": 5,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 2,
    },
    {
        "quiz_id": 7,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 4,
    },
    {
        "quiz_id": 9,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 2,
    },
    {
        "quiz_id": 9,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 2,
    },
    {
        "quiz_id": 9,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 2,
    },
    {
        "quiz_id": 9,
        "user_id": 2,
        "attempted_at": datetime(2025, 1, 1),
        "score": 5,
    }
]
