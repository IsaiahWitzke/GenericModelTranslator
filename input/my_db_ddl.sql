CREATE TABLE bank_account (
    bank_account_id BIGSERIAL PRIMARY KEY,
    user_id BIGSERIAL NOT NULL,
    account_value INT NOT NULL
);

CREATE TABLE user (
    user_id BIGSERIAL PRIMARY KEY,
    user_first_name VARCHAR(255) NOT NULL,
    user_last_name VARCHAR(255) NOT NULL,
    user_addr VARCHAR(255) NULL
);