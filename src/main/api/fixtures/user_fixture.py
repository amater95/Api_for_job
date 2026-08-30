import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.add_deposit_request import AddDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.test_data.test_data import TestData


@pytest.fixture
def create_user_request(api_manager):
     user_request = RandomModelGenerator.generate(CreateUserRequest)
     api_manager.admin_steps.create_user(user_request)
     return user_request


@pytest.fixture
def create_account_request(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def create_account_with_money_request(api_manager, create_user_request):
    account_request = api_manager.user_steps.create_account(create_user_request)
    add_deposit_request = AddDepositRequest(
        accountId = account_request.id,
        amount = TestData.DEPOSIT_SUMM)
    api_manager.user_steps.add_deposit(create_user_request, add_deposit_request)
    return api_manager.user_steps.add_deposit(create_user_request, add_deposit_request)


@pytest.fixture
def transfer_data_request(api_manager, create_account_request, create_account_with_money_request):
    request_data_transfer = RandomModelGenerator.generate(
        TransferRequest,
        fromAccountId = create_account_with_money_request.id,
        toAccountId = create_account_request.id
    )
    return request_data_transfer


@pytest.fixture
def create_credit_user_request(api_manager):
     user_request = RandomModelGenerator.generate(CreateUserRequest, role = TestData.CREDIT_USER_ROLE)
     api_manager.admin_steps.create_user(user_request)
     return user_request


@pytest.fixture
def create_credit_account_request(api_manager, create_credit_user_request):
    return api_manager.user_steps.create_account(create_credit_user_request)


@pytest.fixture
def credit_data_request(api_manager, create_credit_account_request):
    request_data_credit = RandomModelGenerator.generate(
        CreditRequest,
        accountId = create_credit_account_request.id
    )
    return request_data_credit


@pytest.fixture
def credit_data_for_dont_credit_role_request(api_manager, create_account_request):
    request_data_credit = RandomModelGenerator.generate(
        CreditRequest,
        accountId = create_account_request.id
    )
    return request_data_credit


@pytest.fixture
def create_account_for_second_credit(api_manager, create_credit_user_request, credit_data_request):
    api_manager.user_steps.credit_req(create_credit_user_request, credit_data_request)
    return credit_data_request


@pytest.fixture
def create_account_with_credit_request(api_manager, create_credit_user_request, credit_data_request):
    response = api_manager.user_steps.credit_req(create_credit_user_request, credit_data_request)
    return response


@pytest.fixture
def credit_repay_data_request(api_manager, create_account_with_credit_request):
    request_data_credit_repay = CreditRepayRequest(
        creditId = create_account_with_credit_request.creditId,
        accountId = create_account_with_credit_request.id,
        amount = create_account_with_credit_request.amount
    )
    return request_data_credit_repay


@pytest.fixture
def credit_repay_invalid_data_request(api_manager, create_account_with_credit_request):
    request_data_credit_repay = CreditRepayRequest(
        creditId = create_account_with_credit_request.creditId,
        accountId = create_account_with_credit_request.id,
        amount = create_account_with_credit_request.amount * 0.9
    )
    return request_data_credit_repay
