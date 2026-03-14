import weakref
from typing import Optional, ClassVar


class TechStats:

    __slots__ = (
        '__weakref__',
        '_id', 'Name', 'MaintainTechnologyName', 'ImageID',

        'TreeColumn', 'TreeRow',

        'RequiredTech', 'RequiredTech2',

        'UnlocksNukes',
        'UnlocksAccessToTheSea',

        'MaximumLevelOfCapitalCity',
        'MaximumLevelOfTheMilitaryAcademy',
        'MaximumLevelOfTheMilitaryAcademyForGenerals',

        'BattleWidth',
        'UnitsAttack', 'UnitsDefense',
        'GeneralAttack', 'GeneralDefense',
        'MaxMorale', 'Discipline',

        'Legacy',

        'ResearchCost',

        'Repeatable',
        'AI'
    )

    _instances: ClassVar[list] = []
    _needs_recalc: ClassVar[bool] = False

    def __init__(self, /,
        ID: Optional[int] = None,
        Name: str = "", MaintainTechnologyName: Optional[bool] = True, ImageID: int = 0,

        TreeColumn: int = 0, TreeRow: int = 0,

        RequiredTech: int = -1, RequiredTech2: int = -1,

        UnlocksNukes: bool = False,
        UnlocksAccessToTheSea: bool = False,

        MaximumLevelOfCapitalCity: Optional[int] = None,
        MaximumLevelOfTheMilitaryAcademy: Optional[int] = None,
        MaximumLevelOfTheMilitaryAcademyForGenerals: Optional[int] = None,

        BattleWidth: Optional[int] = None,
        UnitsAttack: Optional[int] = None, UnitsDefense: Optional[int] = None,
        GeneralAttack: Optional[int] = None, GeneralDefense: Optional[int] = None,
        MaxMorale: Optional[int] = None, Discipline: Optional[int] = None,

        Legacy: Optional[int] = None,

        ResearchCost: int = 0,
        Repeatable: bool = False,
        AI: int = 5
        ):
        self._id = self.assign_id(ID)
        self.Name, self.MaintainTechnologyName, self.ImageID = Name, MaintainTechnologyName, ImageID

        self.TreeColumn, self.TreeRow = TreeColumn, TreeRow

        self.RequiredTech, self.RequiredTech2 = RequiredTech, RequiredTech2

        self.UnlocksNukes = UnlocksNukes
        self.UnlocksAccessToTheSea = UnlocksAccessToTheSea

        self.MaximumLevelOfCapitalCity = MaximumLevelOfCapitalCity
        self.MaximumLevelOfTheMilitaryAcademy = MaximumLevelOfTheMilitaryAcademy
        self.MaximumLevelOfTheMilitaryAcademyForGenerals = MaximumLevelOfTheMilitaryAcademyForGenerals

        self.BattleWidth = BattleWidth
        self.UnitsAttack, self.UnitsDefense = UnitsAttack, UnitsDefense
        self.GeneralAttack, self.GeneralDefense = GeneralAttack, GeneralDefense
        self.MaxMorale, self.Discipline = MaxMorale, Discipline

        self.Legacy = Legacy

        self.ResearchCost = ResearchCost

        self.Repeatable = Repeatable
        self.AI = AI

        self._instances.append(weakref.ref(self))
        self.__class__._needs_recalc = True


    def assign_id(self, custom_id) -> int:
        if custom_id is not None and -1 < custom_id < len(self._instances):
            for inst in self.__class__._instances:
                if inst()._id >= custom_id:
                    inst()._id += 1
                    return custom_id
        else:
            return len(self._instances)


    @property
    def ID(self) -> int:
        if self.__class__._needs_recalc:
            self.__class__._recalculate_ids()
        return self._id


    @classmethod
    def _is_sorted(cls) -> bool:
        for index, instance in enumerate(cls._instances):
            if instance()._id != index:
                return False
        return True


    @classmethod
    def _recalculate_ids(cls):
        if cls._needs_recalc:
            while not cls._is_sorted():
                for index, instance in enumerate(cls._instances):
                    if index+1 < len(cls._instances):
                        next_instance = cls._instances[index+1]
                        if next_instance()._id > instance()._id:
                            next_instance()._id, instance()._id = instance()._id, next_instance()._id
                    if instance()._id != index:
                        instance()._id = index
            cls._needs_recalc = False


    def __del__(self):
        self.__class__._needs_recalc = True