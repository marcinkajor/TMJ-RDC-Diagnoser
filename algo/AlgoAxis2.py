class Axis2:
    def __init__(self, qs: list):
        self.q3 = int(qs[0])
        self.q7 = int(qs[1])
        self.q8 = int(qs[2])
        self.q9 = int(qs[3])
        self.q10 = int(qs[4])
        self.q11 = int(qs[5])
        self.q12 = int(qs[6])
        self.q13 = int(qs[7])

    def getDiagnosis(self) -> str:
        if self.q3 == 0:
            return "No TMD pain in prior 6 months"
        else:
            cpi = (self.q7 + self.q8 + self.q9) / 3 * 10
            disabilityDaysPoints = self.q10
            disabilityPoints = (self.q11 + self.q12 + self.q13) / 3 * 10
            totalDisabilityScore = self._daysToDisabilityScore(disabilityDaysPoints) + \
                                   self._pointsToDisabilityScore(disabilityPoints)

            return self._calculateChronicPainGradeClassification(cpi, totalDisabilityScore)

    @staticmethod
    def _daysToDisabilityScore(days: int) -> int:
        if (days >= 0) and (days <= 6):
            return 0
        elif (days >= 7) and (days <= 14):
            return 1
        elif (days >= 15) and (days <= 30):
            return 2
        else:
            return 3

    @staticmethod
    def _pointsToDisabilityScore(days: int) -> int:
        if (days >= 0) and (days <= 29):
            return 0
        elif (days >= 30) and (days <= 49):
            return 1
        elif (days >= 50) and (days <= 69):
            return 2
        else:
            return 3

    @staticmethod
    def _calculateChronicPainGradeClassification(cpi: int, disabilityPoints: int) -> str:
        if (cpi < 50) and (disabilityPoints < 3):
            return "Low disability - grade I (low intensity)"
        elif (cpi >= 50) and (disabilityPoints < 3):
            return "Low disability - grade II (high intensity)"
        elif disabilityPoints == 3 or disabilityPoints == 4:
            return "High disability - grade III (moderately limiting)"
        elif disabilityPoints == 5 or disabilityPoints == 6:
            return "High disability - grade III (severely limiting)"
