import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.test_data.error_messages import ErrorMessages
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.test_data.test_data import TestData


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_full(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_repay_data_request: CreditRepayRequest):
        response = api_manager.user_steps.credit_repay_full(create_credit_user_request, credit_repay_data_request)

        credit_from_db = Credit.get_one_from_db(db_session, account_id = credit_repay_data_request.accountId)

        assert response.amountDeposited == credit_repay_data_request.amount, f"Сумма погашения кредита {credit_repay_data_request.amount} должна быть = {response.amountDeposited}"
        assert credit_from_db.balance == TestData.START_DEPOSIT_AMOUNT, "Кредит не был погашен"


    def test_credit_repay_unfull(self, db_session: Session, api_manager:ApiManager, create_credit_user_request: CreateUserRequest, create_account_with_credit_request, credit_repay_invalid_data_request: CreditRepayRequest):
        response = api_manager.user_steps.credit_repay_unfull(create_credit_user_request, credit_repay_invalid_data_request)

        credit_from_db = Credit.get_one_from_db(db_session, account_id = credit_repay_invalid_data_request.accountId)

        assert response.json()["error"] == ErrorMessages.DONT_FULL_SUMM_CREDIT.format(credit_summ = int(create_account_with_credit_request.amount)), (
            f"Ожидалась ошибка {ErrorMessages.DONT_FULL_SUMM_CREDIT.format(credit_summ = int(create_account_with_credit_request.amount))}, "
            f"была получена {response.json()["error"]}"
        )
        assert credit_from_db.balance == - create_account_with_credit_request.amount, "Сумма кредита изменилась"
