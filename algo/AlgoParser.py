from algo.AlgoHelpers import parseRLExamination
from algo.AlgoAxis1 import E2, E3, E4, E5, E6, E7, E8
from algo.AlgoAxis1 import AxisOne
from algo.AlgoPalpation import createPalpations, combinePalpations
from algo.AlgoQ import Q
from algo.AlgoPatient import Person
from algo.AlgoKeys import Keys


def parseDatabase(axis1_data, palpation_data, q_data):
    persons = {}
    axisOnes = {}
    palpations = {}
    qs = {}
    for idx, (axis1Row, palpRow, qRow) in enumerate(zip(axis1_data, palpation_data, q_data)):
        # set personal data
        person = Person(axis1Row[Keys.Axis1.NAME], axis1Row[Keys.Axis1.SURNAME],
                        axis1Row[Keys.Axis1.AGE], axis1Row[Keys.Axis1.SEX])
        persons[axis1Row[Keys.Axis1.ID]] = person
        # parse and combine AxisI data
        e2 = E2(int(axis1Row[Keys.Axis1.E2]))
        e3 = E3()
        # TODO: encapsulate parseRLExamination in E3!
        e3left, e3right = parseRLExamination(str(axis1Row[Keys.Axis1.E3]))
        e3.addPain("left", e3left)
        e3.addPain("right", e3right)
        e4 = E4(int(axis1Row[Keys.Axis1.E4]))
        e5 = E5()
        e5.addOpening("E5a", int(axis1Row[Keys.Axis1.E5a]))
        e5.addOpening("E5b", int(axis1Row[Keys.Axis1.E5b]))
        e5.addOpening("E5c", int(axis1Row[Keys.Axis1.E5c]))
        e5.addOpening("E5d", int(axis1Row[Keys.Axis1.E5d]))
        e5passiveRight, e5passiveLeft = parseRLExamination(str(axis1Row[Keys.Axis1.E5cP]))
        e5activeRight, e5activeLeft = parseRLExamination(str(axis1Row[Keys.Axis1.E5cP]))
        e5.addOpeningPain("passive", e5passiveRight, e5passiveLeft)
        e5.addOpeningPain("active", e5activeRight, e5activeLeft)
        e6 = E6()
        e6.addSound("left", "open", int(axis1Row[Keys.Axis1.E6aL]), int(axis1Row[Keys.Axis1.E6aLmm]))
        e6.addSound("left", "close", int(axis1Row[Keys.Axis1.E6bL]), int(axis1Row[Keys.Axis1.E6bLmm]))
        e6.addSound("right", "open", int(axis1Row[Keys.Axis1.E6aR]), int(axis1Row[Keys.Axis1.E6aRmm]))
        e6.addSound("right", "close", int(axis1Row[Keys.Axis1.E6bR]), int(axis1Row[Keys.Axis1.E6bRmm]))
        e6.addClickElimination(str(axis1Row[Keys.Axis1.E6c]))
        e7 = E7(int(axis1Row[Keys.Axis1.E7a]), int(axis1Row[Keys.Axis1.E7b]),
                str(axis1Row[Keys.Axis1.E7d]))
        e8 = E8()
        e8.addSideMoveSound("right", str(axis1Row[Keys.Axis1.E8R]))
        e8.addSideMoveSound("left", str(axis1Row[Keys.Axis1.E8L]))
        e8.addSideMoveSound("protrusion", str(axis1Row[Keys.Axis1.E8Pr]))
        axis1_whole = AxisOne([e2, e3, e4, e5, e6, e7, e8])
        axisOnes[axis1Row[Keys.Axis1.ID]] = axis1_whole
        # parse and combine palpations
        e9 = createPalpations("E9", palpRow, Keys.Palpation.E9)
        e10a = createPalpations("E10a", palpRow, Keys.Palpation.E10a)
        e10b = createPalpations("E10b", palpRow, Keys.Palpation.E10b)
        e11 = createPalpations("E11", palpRow, Keys.Palpation.E11)
        palpations_whole = combinePalpations(e9, e10a, e10b, e11)
        palpations[palpRow[Keys.Palpation.ID]] = palpations_whole
        # set q
        q = Q(qRow[Keys.Q.SURNAME], qRow[Keys.Q.Q3], qRow[Keys.Q.Q14])
        qs[qRow[Keys.Q.ID]] = q
    return persons, axisOnes, palpations, qs
