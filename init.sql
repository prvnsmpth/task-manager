CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    token TEXT
);

CREATE TABLE status_requests (
    id SERIAL PRIMARY KEY,
    requested_by TEXT,
    requested_of TEXT,
    num_reportees INTEGER
);

CREATE TABLE status_updates (
    request_id INTEGER,
    responder TEXT,
    full_name TEXT,
    responses TEXT,
    done boolean
);
