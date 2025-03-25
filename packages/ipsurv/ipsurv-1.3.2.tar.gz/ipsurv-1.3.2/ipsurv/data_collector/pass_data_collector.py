from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.requester.requester import Requester
from ipsurv.core.entity import Target


class PassDataCollector(DataCollector):
    """
    :param name:
    :type name: str
    :param requester:
    :type requester: PassRequester
    :param args:
    :type args: argparse.Namespace
    """

    def __init__(self, name, requester, args):
        super().__init__(requester, args)

        self._name = name

    def get_name(self):
        return self._name.upper()

    def request_data(self, target, requires):
        # type: (Target, list) -> tuple
        return self.requester.request(target)

    def get_requires(self):
        return []

    def build_data(self, target, data, success, response, response_time):
        data.set(self._name.lower() + '_time', response_time)

        for k, v in response.items():
            self.put(data, response, k)

        self._append_error(data, response)


class PassRequester(Requester):
    def request(self, target):
        # type : Target
        """
        :param target:
        :type target: Target
        """

        return False, {}
