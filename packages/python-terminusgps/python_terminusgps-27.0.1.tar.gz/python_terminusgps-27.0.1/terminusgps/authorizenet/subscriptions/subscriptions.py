from authorizenet import apicontractsv1, apicontrollers

from ..auth import get_merchant_auth
from ..utils import ControllerExecutionMixin


class Subscription(ControllerExecutionMixin):
    def __init__(self, id: str | int | None = None, *args, **kwargs) -> None:
        if id and isinstance(id, str) and not id.isdigit():
            raise ValueError(f"'id' must be a digit, got '{id}'.")
        self.id = int(id if id else self.create(*args, **kwargs))

    def create(
        self,
        name: str,
        amount: str,
        schedule: apicontractsv1.paymentScheduleType,
        profile_id: int | str,
        payment_id: int | str,
        address_id: int | str,
        trial_amount: str = "0.00",
    ) -> int:
        request = apicontractsv1.ARBCreateSubscriptionRequest(
            merchantAuthentication=get_merchant_auth(),
            subscription=apicontractsv1.ARBSubscriptionType(
                name=name,
                paymentSchedule=schedule,
                amount=amount,
                trialAmount=trial_amount,
                profile=apicontractsv1.customerProfileIdType(
                    customerProfileId=str(profile_id),
                    customerPaymentProfileId=str(payment_id),
                    customerAddressId=str(address_id),
                ),
            ),
        )
        controller = apicontrollers.ARBCreateSubscriptionController(request)
        response = self.execute_controller(controller)
        if response is None:
            raise ValueError("Failed to retrieve Authorizenet API response.")
        return int(response.subscriptionId)
