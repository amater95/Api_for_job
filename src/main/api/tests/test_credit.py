import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.test_data.error_messages import ErrorMessages
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.test_data.test_data import TestData


@pytest.mark.api
class TestCredit:
    def test_credit_req(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, create_credit_account_request, credit_data_request: CreditRequest):
        response = api_manager.user_steps.credit_req(create_credit_user_request, credit_data_request)

        credit_from_db = Credit.get_one_from_db(db_session, account_id = response.id)

        assert response.amount == response.balance == credit_data_request.amount, f"Сумма на балансе {response.balance} не равна сумме зачисления {credit_data_request.amount}"
        assert credit_from_db.amount == credit_data_request.amount, "Сумма кредита != запрашиваемой сумме"


    def test_second_credit_req(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, create_account_for_second_credit):
        response = api_manager.user_steps.second_credit_req(create_credit_user_request, create_account_for_second_credit)

        count_credit_from_db = Credit.count(db_session, account_id = create_account_for_second_credit.accountId)

        assert response.json()["error"] == ErrorMessages.ONLY_ONE_CREDIT_BY_ONE_ACCOUNT, f"Ожидалась ошибка {ErrorMessages.ONLY_ONE_CREDIT_BY_ONE_ACCOUNT}, а была получена {response.json()['error']}"
        assert count_credit_from_db == TestData.MAX_COUNT_CREDIT, "Пользователь имеет более 1 кредита"


    def test_credit_req_for_role_user(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, credit_data_for_dont_credit_role_request: CreditRequest):
        response = api_manager.user_steps.credit_req_for_role_user(create_user_request, credit_data_for_dont_credit_role_request)

        credit_from_db = Credit.get_one_from_db(db_session, account_id = credit_data_for_dont_credit_role_request.accountId)

        assert response.json()["title"] == ErrorMessages.FORBIDDEN_FOR_CREDIT and response.json()["detail"] == ErrorMessages.DETAIL_FORBIDDEN_FOR_CREDIT, (
            f"Ожидалась ошибка {ErrorMessages.FORBIDDEN_FOR_CREDIT}, а была получена {response.json()["title"]}"
        )
        assert credit_from_db is None, f"У пользователя с ролью {create_user_request.role} есть оформленный кредит"
