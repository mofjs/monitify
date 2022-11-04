from abc import ABCMeta, abstractmethod


class BaseNotif(metaclass=ABCMeta):
    """BaseNotification class for sending message."""

    @abstractmethod
    def send_message(self, name: str, items: list[str]) -> None:
        """An only method should be implemented by the subclass."""
        pass
