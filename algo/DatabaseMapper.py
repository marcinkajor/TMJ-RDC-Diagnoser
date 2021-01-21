class MapperStrategy:
    def __init__(self, fromDatabase: dict):
        pass

    def get(self):
        pass


class MapperE2(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "None": 0,
            "Right": 1,
            "Left": 2,
            "Both": 3
        }
        self.e2 = self.mapping[fromDatabase["InitialData"]["pain_side"]]

    def get(self) -> dict:
        return {"E2": self.e2}


class MapperE3(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "": 0,
            "Muscles": 1,
            "Jaw Joint": 2,
            "Both": 3
        }
        self.e3right = self.mapping[fromDatabase["InitialData"]["right_pain_area"]]
        self.e3left = self.mapping[fromDatabase["InitialData"]["left_pain_area"]]

    def get(self) -> dict:
        return {"E3right": self.e3right, "E3left": self.e3left}


class MapperE4(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "Straight": 0,
            "Right Lateral Deviation (uncorrected)": 1,
            "Right Corrected ('S') Deviation": 2,
            "Left Lateral Deviation (uncorrected)": 3,
            "Left Corrected ('S') Deviation": 4,
            "Other Type": 5
        }
        self.e4 = self.mapping[fromDatabase["AbductionMovement"]["abduction_movement"]]

    def get(self) -> dict:
        return {"E4": self.e4}


class MapperE5(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.mm = MapperE5.Mm(fromDatabase)
        self.pain = MapperE5.Pain(fromDatabase)

    def get(self) -> dict:
        return {"E5mm": self.mm.get(), "E5pain": self.pain.get()}

    # helper classes:
    class Mm:
        def __init__(self, fromDatabase: dict):
            self.e5a = int(fromDatabase["VerticalMovementRange"]["no_pain_opening_mm"])
            self.e5b = int(fromDatabase["VerticalMovementRange"]["max_active_opening_mm"])
            self.e5c = int(fromDatabase["VerticalMovementRange"]["max_passive_opening_mm"])
            self.e5d = int(fromDatabase["IncisorsGap"]["vertical_mm"])

        def get(self) -> dict:
            return {"E5a": self.e5a, "E5b": self.e5b, "E5c": self.e5c, "E5d": self.e5d}

    class Pain:
        def __init__(self, fromDatabase: dict):
            painMap = {
                "None": 0,
                "Muscle": 1,
                "Joint": 2,
                "Both": 3
            }
            self.e5PassiveRight = painMap[fromDatabase["VerticalMovementRange"]["max_passive_opening_right"]]
            self.e5PassiveLeft = painMap[fromDatabase["VerticalMovementRange"]["max_passive_opening_left"]]
            self.e5ActiveRight = painMap[fromDatabase["VerticalMovementRange"]["max_active_opening_right"]]
            self.e5ActiveLeft = painMap[fromDatabase["VerticalMovementRange"]["max_active_opening_left"]]

        def get(self) -> dict:
            return {"passive_right": self.e5PassiveRight, "passive_left": self.e5PassiveLeft,
                    "active_right": self.e5ActiveRight, "active_left": self.e5ActiveLeft}


class MapperE6(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.sound = MapperE6.Sound(fromDatabase)
        self.mm = MapperE6.Mm(fromDatabase)
        self.elimination = MapperE6.Elimination(fromDatabase)

    def get(self):
        return {"E6sounds": self.sound.get(), "E6mm": self.mm.get(), "E6eliminations": self.elimination.get()}

    # helper classes:
    class Sound:
        def __init__(self, fromDatabase: dict):
            soundsMap = {
                "None": 0,
                "Click": 1,
                "Coarse Crepitus": 2,
                "Fine Crepitus": 3
            }
            self.e6OpeningRight = soundsMap[fromDatabase["SoundsInJointAbduction"]["right_opening_sound"]]
            self.e6OpeningLeft = soundsMap[fromDatabase["SoundsInJointAbduction"]["left_opening_sound"]]
            self.e6ClosingRight = soundsMap[fromDatabase["SoundsInJointAbduction"]["right_closing_sound"]]
            self.e6ClosingLeft = soundsMap[fromDatabase["SoundsInJointAbduction"]["left_closing_sound"]]

        def get(self) -> dict:
            return {"opening_right": self.e6OpeningRight, "opening_left": self.e6OpeningLeft,
                    "closing_right": self.e6ClosingRight, "closing_left": self.e6ClosingLeft}

    class Mm:
        def __init__(self, fromDatabase: dict):
            self.e6OpeningRight = int(fromDatabase["SoundsInJointAbduction"]["right_opening_mm"])
            self.e6OpeningLeft = int(fromDatabase["SoundsInJointAbduction"]["left_opening_mm"])
            self.e6ClosingRight = int(fromDatabase["SoundsInJointAbduction"]["right_closing_mm"])
            self.e6ClosingLeft = int(fromDatabase["SoundsInJointAbduction"]["left_closing_mm"])

        def get(self) -> dict:
            return {"opening_right": self.e6OpeningRight, "opening_left": self.e6OpeningLeft,
                    "closing_right": self.e6ClosingRight, "closing_left": self.e6ClosingLeft}

    class Elimination:
        def __init__(self, fromDatabase: dict):
            clickEliminationMap = {
                "No": 0,
                "Yes": 1,
                "Not Applicable": 8
            }
            self.e6OpeningRight = clickEliminationMap[fromDatabase["SoundsInJointAbduction"]["right_opening_click_elimination"]]
            self.e6OpeningLeft = clickEliminationMap[fromDatabase["SoundsInJointAbduction"]["left_opening_click_elimination"]]
            self.e6ClosingRight = clickEliminationMap[fromDatabase["SoundsInJointAbduction"]["right_closing_click_elimination"]]
            self.e6ClosingLeft = clickEliminationMap[fromDatabase["SoundsInJointAbduction"]["left_closing_click_elimination"]]

        def get(self) -> dict:
            return {"opening_right": self.e6OpeningRight, "opening_left": self.e6OpeningLeft,
                    "closing_right": self.e6ClosingRight, "closing_left": self.e6ClosingLeft}


class MapperE7(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.mapping = {
            "L": "left",
            "R": "right"
        }
        self.middleLineMm = int(fromDatabase["IncisorsGap"]["middle_line_mm"])
        self.rightMm = int(fromDatabase["VerticalMandibleMovements"]["right_side_mm"])
        self.leftMm = int(fromDatabase["VerticalMandibleMovements"]["left_side_mm"])
        readAlignmentSide = fromDatabase["IncisorsGap"]["middle_line_alignment_relative_to_the_jaw"]
        self.side = self.mapping[readAlignmentSide]

    def get(self):
        return {
                "E7mm": {"right": self.rightMm, "left": self.leftMm},
                "E7middleLine": {self.side: self.middleLineMm}
        }


class MapperE8(MapperStrategy):
    def __init__(self, fromDatabase: dict):
        self.right = MapperE8.Movement("right_side", fromDatabase)
        self.left = MapperE8.Movement("left_side", fromDatabase)
        self.forward = MapperE8.Movement("forward", fromDatabase)

    def get(self) -> dict:
        return {"e8right": self.right.get(), "e8left": self.left.get(), "e8forward": self.forward.get()}

    # helper class:
    class Movement:
        def __init__(self, movement: str, fromDatabase: dict):
            self.mapping = {
                "None": 0,
                "Muscle": 1,
                "Joint": 2,
                "Both": 3
            }
            assert (movement in ["right_side", "left_side", "forward"])
            self.right = self.mapping[fromDatabase["VerticalMandibleMovements"][movement + "_right"]]
            self.left = self.mapping[fromDatabase["VerticalMandibleMovements"][movement + "_left"]]

        def get(self) -> dict:
            return {"right": self.right, "left": self.left}


class DatabaseRecordMapper:
    def __init__(self, mappingStrategy: MapperStrategy):
        self.mapper = mappingStrategy

    def dataMappedToAlgoInterface(self) -> dict:
        return self.mapper.get()
