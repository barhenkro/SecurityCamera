from notifier import Notifier
from email_notifier import EmailNotifier
from face_detector import FaceDetector


def create_face_detector(settings):
    notifiers_settings = []
    notifiers = []

    if "notifiers" in settings:
        notifiers_settings = settings['notifiers']

    # build notifiers
    for notifier_name, notifier_attributes in notifiers_settings.iteritems():
        notifiers_registry = _get_notifiers_registry()
        if notifier_name in notifiers_registry:
            notifiers.append(notifiers_registry[notifier_name](**notifier_attributes))

    return FaceDetector(notifiers)


def _get_notifiers_registry():
    return {notifier_class.__name__: notifier_class for notifier_class in Notifier.__subclasses__()}
