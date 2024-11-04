import json

class Kysymys:
    """
    A class to represent a question with multiple choice answers.

    Attributes:
        id (int): The identifier of the question.
        kysymys (str): The question text.
        array (list): An array that has the indexes of right answers.
        vastausvaihtoehdot (list): A list of possible answers.
        lkm (int): The number of possible answers.
    """

    def __init__(self, id: int, kysymys: str, o: list, vastausvaihtoehdot: list):
        self._id = id
        self._kysymys = kysymys
        self._o = json.dumps(o)
        self._vastausvaihtoehdot = json.dumps(vastausvaihtoehdot)
        self._lkm = len(vastausvaihtoehdot)

    # Getter and setter for id
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    # Getter and setter for kysymys
    @property
    def kysymys(self) -> str:
        return self._kysymys

    @kysymys.setter
    def kysymys(self, value: str):
        self._kysymys = value

    # Getter and setter for o
    @property
    def o(self) -> list:
        return self._o

    @o.setter
    def o(self, value: list):
        self._o = value

    # Getter and setter for vastausvaihtoehdot
    @property
    def vastausvaihtoehdot(self) -> list:
        return self._vastausvaihtoehdot

    @vastausvaihtoehdot.setter
    def vastausvaihtoehdot(self, value: list):
        self._vastausvaihtoehdot = value
        self._lkm = len(value)  # Update lkm when vastausvaihtoehdot is set

    # Getter for lkm
    @property
    def lkm(self) -> int:
        return self._lkm