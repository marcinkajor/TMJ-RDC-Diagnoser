class MapperStrategy:
    def __init__(self, fromDatabase: dict):
        self.record = fromDatabase

    def readFromDatabase(self, majorKey: str, minorKey):
        # this method may rethrow concrete exception to be received in client's code
        value = None
        try:
            main = self.record[majorKey]
            try:
                value = main[minorKey]
                if value is None or len(value) == 0:
                    # these 2 parameters may not be present if the 'pain_side' is 'None'
                    if minorKey != "right_pain_area" and minorKey != "left_pain_area":
                        raise KeyError
            except KeyError:
                print("Missing a valid value under minor key: {} in {}".format(minorKey, majorKey))
        except KeyError as e:
            print("Missing major key: {}, Error: {}".format(majorKey, str(e)))
        return value

    def get(self):
        pass


class MapperE2(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE2, self).__init__(fromDatabase)
        self.mapping = {
            "None": 0,
            "Right": 1,
            "Left": 2,
            "Both": 3
        }

        self.e2 = self.mapping[self.readFromDatabase("InitialData", "pain_side")]

    def get(self) -> dict:
        return {"E2": self.e2}


class MapperE3(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE3, self).__init__(fromDatabase)
        self.mapping = {
            "": 0,
            "Muscles": 1,
            "Jaw Joint": 2,
            "Both": 3
        }
        self.e3right = self.mapping[self.readFromDatabase("InitialData", "right_pain_area")]
        self.e3left = self.mapping[self.readFromDatabase("InitialData", "left_pain_area")]

    def get(self) -> dict:
        return {"E3right": self.e3right, "E3left": self.e3left}


class MapperE4(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE4, self).__init__(fromDatabase)
        self.mapping = {
            "Straight": 0,
            "Right Lateral Deviation (uncorrected)": 1,
            "Right Corrected ('S') Deviation": 2,
            "Left Lateral Deviation (uncorrected)": 3,
            "Left Corrected ('S') Deviation": 4,
            "Other Type": 5
        }
        self.e4 = self.mapping[self.readFromDatabase("AbductionMovement", "abduction_movement")]

    def get(self) -> dict:
        return {"E4": self.e4}


class MapperE5(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE5, self).__init__(fromDatabase)
        self.mm = self._createMm()
        self.pain = self._createPain()

    def get(self) -> dict:
        return {"E5mm": self.mm.get(), "E5pain": self.pain.get()}

    def _createMm(self):
        return MapperE5.Mm(self)

    def _createPain(self):
        return MapperE5.Pain(self)

    # helper classes:
    class Mm:
        def __init__(self, mapper):
            self.mapper = mapper
            self.e5a = int(self.mapper.readFromDatabase("VerticalMovementRange", "no_pain_opening_mm"))
            self.e5b = int(self.mapper.readFromDatabase("VerticalMovementRange", "max_active_opening_mm"))
            self.e5c = int(self.mapper.readFromDatabase("VerticalMovementRange", "max_passive_opening_mm"))
            self.e5d = int(self.mapper.readFromDatabase("IncisorsGap", "vertical_mm"))

        def get(self) -> dict:
            return {"E5a": self.e5a, "E5b": self.e5b, "E5c": self.e5c, "E5d": self.e5d}

    class Pain:
        def __init__(self, mapper):
            self.mapper = mapper
            painMap = {
                "None": 0,
                "Muscle": 1,
                "Joint": 2,
                "Both": 3
            }
            self.e5PassiveRight = painMap[
                self.mapper.readFromDatabase("VerticalMovementRange", "max_passive_opening_right")]
            self.e5PassiveLeft = painMap[
                self.mapper.readFromDatabase("VerticalMovementRange", "max_passive_opening_left")]
            self.e5ActiveRight = painMap[
                self.mapper.readFromDatabase("VerticalMovementRange", "max_active_opening_right")]
            self.e5ActiveLeft = painMap[
                self.mapper.readFromDatabase("VerticalMovementRange", "max_active_opening_left")]

        def get(self) -> dict:
            return {"passive_right": self.e5PassiveRight, "passive_left": self.e5PassiveLeft,
                    "active_right": self.e5ActiveRight, "active_left": self.e5ActiveLeft}


class MapperE6(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE6, self).__init__(fromDatabase)
        self.sound = self._createSound()
        self.mm = self._createMm()
        self.elimination = self._createElimination()

    def get(self):
        return {"E6sounds": self.sound.get(), "E6mm": self.mm.get(), "E6eliminations": self.elimination.get()}

    def _createSound(self):
        return MapperE6.Sound(self)

    def _createMm(self):
        return MapperE6.Mm(self)

    def _createElimination(self):
        return MapperE6.Elimination(self)

    # helper classes:
    class Sound:
        def __init__(self, mapper):
            self.mapper = mapper
            soundsMap = {
                "None": 0,
                "Click": 1,
                "Coarse Crepitus": 2,
                "Fine Crepitus": 3
            }
            self.e6OpeningRight = soundsMap[
                self.mapper.readFromDatabase("SoundsInJointAbduction", "right_opening_sound")]
            self.e6OpeningLeft = soundsMap[
                self.mapper.readFromDatabase("SoundsInJointAbduction", "left_opening_sound")]
            self.e6ClosingRight = soundsMap[
                self.mapper.readFromDatabase("SoundsInJointAbduction", "right_closing_sound")]
            self.e6ClosingLeft = soundsMap[
                self.mapper.readFromDatabase("SoundsInJointAbduction", "left_closing_sound")]

        def get(self) -> dict:
            return {"opening_right": self.e6OpeningRight, "opening_left": self.e6OpeningLeft,
                    "closing_right": self.e6ClosingRight, "closing_left": self.e6ClosingLeft}

    class Mm:
        def __init__(self, mapper):
            self.mapper = mapper
            self.e6OpeningRight = int(self.mapper.readFromDatabase("SoundsInJointAbduction", "right_opening_mm"))
            self.e6OpeningLeft = int(self.mapper.readFromDatabase("SoundsInJointAbduction", "left_opening_mm"))
            self.e6ClosingRight = int(self.mapper.readFromDatabase("SoundsInJointAbduction", "right_closing_mm"))
            self.e6ClosingLeft = int(self.mapper.readFromDatabase("SoundsInJointAbduction", "left_closing_mm"))

        def get(self) -> dict:
            return {"opening_right": self.e6OpeningRight, "opening_left": self.e6OpeningLeft,
                    "closing_right": self.e6ClosingRight, "closing_left": self.e6ClosingLeft}

    class Elimination:
        def __init__(self, mapper):
            self.mapper = mapper
            clickEliminationMap = {
                "No": 0,
                "Yes": 1,
                "Not Applicable": 8
            }
            self.e6OpeningRight = clickEliminationMap[
                self.mapper.readFromDatabase("SoundsInJointAbduction", "right_opening_click_elimination")]
            self.e6OpeningLeft = clickEliminationMap[
                self.mapper.readFromDatabase("SoundsInJointAbduction", "left_opening_click_elimination")]
            # TODO: closing is supported only in Polish version of RDC form
            # self.e6ClosingRight = clickEliminationMap[
            #     self.mapper.readFromDatabase("SoundsInJointAbduction", "right_closing_click_elimination")]
            # self.e6ClosingLeft = clickEliminationMap[
            #     self.mapper.readFromDatabase("SoundsInJointAbduction", "left_closing_click_elimination")]

        def get(self) -> dict:
            return {"opening_right": self.e6OpeningRight, "opening_left": self.e6OpeningLeft}


class MapperE7(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE7, self).__init__(fromDatabase)
        self.mapping = {
            "L": "left",
            "R": "right"
        }
        self.middleLineMm = int(self.readFromDatabase("IncisorsGap", "middle_line_mm"))
        self.rightMm = int(self.readFromDatabase("VerticalMandibleMovements", "right_side_mm"))
        self.leftMm = int(self.readFromDatabase("VerticalMandibleMovements", "left_side_mm"))
        readAlignmentSide = self.readFromDatabase("IncisorsGap", "middle_line_alignment_relative_to_the_jaw")
        self.side = self.mapping[readAlignmentSide]

    def get(self):
        return {
                "E7mm": {"right": self.rightMm, "left": self.leftMm},  # right - 7a, left - 7b
                "E7middleLine": {self.side: self.middleLineMm}
        }


class MapperE8(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperE8, self).__init__(fromDatabase)
        self.right = self._createMovement("right_side")
        self.left = self._createMovement("left_side")
        self.forward = self._createMovement("forward")  # forward=protrusion

    def get(self) -> dict:
        return {"e8right": self.right.get(), "e8left": self.left.get(), "e8forward": self.forward.get()}

    def _createMovement(self, movement: str):
        return MapperE8.Movement(self, movement)

    # helper class:
    class Movement:
        def __init__(self, mapper, movement: str,):
            self.mapper = mapper
            self.mapping = {
                "None": 0,
                "Muscle": 1,
                "Joint": 2,
                "Both": 3
            }
            assert (movement in ["right_side", "left_side", "forward"])
            self.right = self.mapping[self.mapper.readFromDatabase("VerticalMandibleMovements", movement + "_right")]
            self.left = self.mapping[self.mapper.readFromDatabase("VerticalMandibleMovements", movement + "_left")]

        def get(self) -> dict:
            return {"right": self.right, "left": self.left}


class MapperPalpation(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperPalpation, self).__init__(fromDatabase)
        self.mapping = {
            "No Pain": 0,
            "Mild Pain": 1,
            "Moderate Pain": 2,
            "Severe Pain": 3
        }
        self.right = []
        self.left = []


class MapperPalpationE9(MapperPalpation):
    def __init__(self, fromDatabase: dict):
        super(MapperPalpationE9, self).__init__(fromDatabase)
        self.keysNoPostfix = ["temporalis_posterior_back_of_temple_", "temporalis_middle_middle_of_temple_",
                              "temporalis_anterior_front_of_temple_", "masseter_superior_cheek_under_cheekbone_",
                              "masseter_middle_cheek_side_of_face_", "masseter_inferior_cheek_jawline_",
                              "posterior_mandibular_region_jaw_throat_region_", "submandibular_region_under_chin_"
                              ]
        for key in self.keysNoPostfix:
            rightValue = self.mapping[self.readFromDatabase("PalpationPainExtraoralMuscles", key + "right")]
            leftValue = self.mapping[self.readFromDatabase("PalpationPainExtraoralMuscles", key + "left")]
            self.right.append(rightValue)
            self.left.append(leftValue)

    def get(self):
        return {"right": self.right, "left": self.left}

    @staticmethod
    def build(fromDatabase: dict):
        return MapperPalpationE9(fromDatabase)


# TODO: get rid of MapperPalpation boiler plate code:
class MapperPalpationE10a(MapperPalpation):
    def __init__(self, fromDatabase: dict):
        super(MapperPalpationE10a, self).__init__(fromDatabase)
        key = "lateral_pole_outside_"
        rightValue = self.mapping[self.readFromDatabase("PalpationPainJointPain", key + "right")]
        leftValue = self.mapping[self.readFromDatabase("PalpationPainJointPain", key + "left")]
        self.right.append(rightValue)
        self.left.append(leftValue)

    def get(self):
        return {"right": self.right, "left": self.left}

    @staticmethod
    def build(fromDatabase: dict):
        return MapperPalpationE10a(fromDatabase)


class MapperPalpationE10b(MapperPalpation):
    def __init__(self, fromDatabase: dict):
        super(MapperPalpationE10b, self).__init__(fromDatabase)
        key = "posterior_attachment_inside_ear_"
        rightValue = self.mapping[self.readFromDatabase("PalpationPainJointPain", key + "right")]
        leftValue = self.mapping[self.readFromDatabase("PalpationPainJointPain", key + "left")]
        self.right.append(rightValue)
        self.left.append(leftValue)

    def get(self):
        return {"right": self.right, "left": self.left}

    @staticmethod
    def build(fromDatabase: dict):
        return MapperPalpationE10b(fromDatabase)


class MapperPalpationE11(MapperPalpation):
    def __init__(self, fromDatabase: dict):
        super(MapperPalpationE11, self).__init__(fromDatabase)
        self.keysNoPostfix = ["lateral_pterygoid_area_behind_upper_molars_", "tendon_of_temporalis_tendon_"]
        for key in self.keysNoPostfix:
            rightValue = self.mapping[self.readFromDatabase("PalpationPainIntraoralPain", key + "right")]
            leftValue = self.mapping[self.readFromDatabase("PalpationPainIntraoralPain", key + "left")]
            self.right.append(rightValue)
            self.left.append(leftValue)

    def get(self):
        return {"right": self.right, "left": self.left}

    @staticmethod
    def build(fromDatabase: dict):
        return MapperPalpationE11(fromDatabase)


class MapperQ(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        super(MapperQ, self).__init__(fromDatabase)
        self.mappingQ = {
            "No": 0,
            "Yes": 1
        }

        self.q3 = self.mappingQ[self.readFromDatabase("Questionnaire", "pain_symptoms")]
        self.q14 = self.mappingQ[self.readFromDatabase("Questionnaire", "opening_problems")]

        self.q7 = int(self.readFromDatabase("Questionnaire2", "facial_pain_score"))
        self.q8 = int(self.readFromDatabase("Questionnaire2", "worst_pain_score"))
        self.q9 = int(self.readFromDatabase("Questionnaire2", "average_pain_score"))
        self.q10 = int(self.readFromDatabase("Questionnaire2", "days_without_activities"))
        self.q11 = int(self.readFromDatabase("Questionnaire2", "six_months_pain_interference"))
        self.q12 = int(self.readFromDatabase("Questionnaire2", "six_months_pain_recreation_change"))
        self.q13 = int(self.readFromDatabase("Questionnaire2", "six_months_pain_work_ability_change"))

    def get(self):
        return {"q3": self.q3, "q14": self.q14, "q7": self.q7, "q8": self.q8, "q9": self.q9, "q10": self.q10,
                "q11": self.q11, "q12": self.q12, "q13": self.q13}


class DatabaseRecordMapper:
    def __init__(self, mappingStrategy: MapperStrategy = None):
        self.mapper = mappingStrategy

    def dataMappedToAlgoInterface(self) -> dict:
        return self.mapper.get()

    def setMapper(self, mappingStrategy: MapperStrategy):
        self.mapper = mappingStrategy
        return self
