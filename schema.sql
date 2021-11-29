CREATE TABLE user (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    interface TEXT NOT NULL,
    websocket TEXT NOT NULL,
    currency TEXT NOT NULL,
    theme TEXT NOT NULL
);

CREATE TABLE interface (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    key TEXT NOT NULL,
    secret TEXT NOT NULL,
    passphrase TEXT NOT NULL
);

CREATE TABLE strategy (
    id INTEGER PRIMARY KEY NOT NULL,
    table_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    product_id TEXT NOT NULL,
    frequency TEXT NOT NULL,
    principal REAL NOT NULL,
    apy REAL NOT NULL,
    period INTEGER NOT NULL
);
