CREATE TABLE bank_account (
    bank_account_id BIGSERIAL PRIMARY KEY,
    account_holder_name VARCHAR(255) NOT NULL,
    account_holder_addr VARCHAR(255) NULL,
    account_value INT NOT NULL
);