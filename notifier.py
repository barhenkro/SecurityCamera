from abc import ABCMeta, abstractmethod


class Notifier(object):
    """Responsible for notifying the user about new log"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, log_id):
        """

        :param log_id: the id of the log at the log database
        :return: void
        """
        pass
