from ..abstractvalidator import AbstractValidator

class GenericXMLValidator(AbstractValidator):

    def __init__(self):
        pass

    # what we have to do:
    # - check if the file is well-formed
    # - find the schema if not given
    # - check if the file is valid according to the schema


class TEIValidator(GenericXMLValidator):
    pass

class LidoValidator(GenericXMLValidator):
    pass
