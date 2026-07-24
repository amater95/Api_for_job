

class ErrorMessages:
    INVALID_DEPOSIT_AMOUNT = "Amount must be between 1000 and 9000"
    MAX_ACCOUNTS_LIMIT_REACHED = "User already has maximum number of accounts(2)"
    INVALID_TRANSFER_AMOUNT = "Amount must be between 500 and 10000"
    ONLY_ONE_CREDIT_BY_ONE_ACCOUNT = "Only one active credit allowed per user"
    FORBIDDEN_FOR_CREDIT = "An error occurred"
    DETAIL_FORBIDDEN_FOR_CREDIT = "Forbidden: ROLE_CREDIT access required"
    DONT_FULL_SUMM_CREDIT = "The amount is not enough. Credit balance: -{credit_summ}"
