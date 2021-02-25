from gui.wizard_pages.BaseWizardPage import PageWithSideOptions
from gui.wizard_pages.WizardPagesHelpers import *
from PyQt5.QtGui import QFont
from algo.DatabaseDeserializer import DatabaseDeserializer

painSeverities = ["No Pain", "Mild Pain", "Moderate Pain", "Severe Pain"]


class PalpationPainPage(PageWithSideOptions):
    def __init__(self, options, label):
        super().__init__()
        self.setTitle("7. Muscles & joint palpation pain")

        self.painOptions = SideOptions(options, painSeverities, self.defaultFont, "BKD protocol")
        self.registerSideOptions(isMandatory=True)

        additionalInfo = QLabel(label)
        additionalInfo.setFont(QFont("Arial", 11, QFont.Bold))

        rightLayout = QHBoxLayout()
        rightLayout.addLayout(self.painOptions.getLayout())
        mainLayout = QGridLayout()
        mainLayout.addWidget(additionalInfo, 0, 0)
        mainLayout.addLayout(rightLayout, 1, 0)
        self.setLayout(mainLayout)

    def clearAll(self):
        self.painOptions.clearAll()


class PalpationPainNoPainPage(PalpationPainPage):
    def __init__(self):
        options = "Mastoid process (lateral upper part)", "Frontal (pupil line, beneath hair)",\
                  "Vertex (1 cm lateral from skull prominence)"
        label = "No pain areas"
        super().__init__(options, label)

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        palpationPainNoPain = diagnosticData["PalpationPainNoPain"]
        mastoidProcessLateralRight = palpationPainNoPain["mastoid_process_lateral_upper_part_right"]
        frontalPupilLineRight = palpationPainNoPain["frontal_pupil_line_beneath_hair_right"]
        vertexRight = palpationPainNoPain["vertex_1_cm_lateral_from_skull_prominence_right"]
        mastoidProcessLateralLeft = palpationPainNoPain["mastoid_process_lateral_upper_part_left"]
        frontalPupilLineLeft = palpationPainNoPain["frontal_pupil_line_beneath_hair_left"]
        vertexLeft = palpationPainNoPain["vertex_1_cm_lateral_from_skull_prominence_left"]

        rightOptions = self.painOptions.getRightOptions().getOptions()
        rightOptions["Mastoid process (lateral upper part)"].getButton(mastoidProcessLateralRight).setChecked(True)
        rightOptions["Frontal (pupil line, beneath hair)"].getButton(frontalPupilLineRight).setChecked(True)
        rightOptions["Vertex (1 cm lateral from skull prominence)"].getButton(vertexRight).setChecked(True)

        leftOptions = self.painOptions.getLeftOptions().getOptions()
        leftOptions["Mastoid process (lateral upper part)"].getButton(mastoidProcessLateralLeft).setChecked(True)
        leftOptions["Frontal (pupil line, beneath hair)"].getButton(frontalPupilLineLeft).setChecked(True)
        leftOptions["Vertex (1 cm lateral from skull prominence)"].getButton(vertexLeft).setChecked(True)


class PalpationPainExtraoralMusclesPage(PalpationPainPage):
    def __init__(self):
        options = ['''Temporalis (posterior) - "Back of temple"''',
                                        '''Temporalis (middle) - "Middle of temple"''',
                                        '''Temporalis (anterior) - "Front of temple"''',
                                        '''Masseter (superior) - "Cheek/under cheekbone"''',
                                        '''Masseter (middle) - "Cheek/side of face"''',
                                        '''Masseter (inferior) - "Cheek/jawline"''',
                                        '''Posterior mandibular region - "Jaw/throat region"''',
                                        '''Submandibular region - "Under chin"''']
        label = "Extraoral muscle pain"
        super().__init__(options, label)

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        palpationPainExtraoral = diagnosticData["PalpationPainExtraoralMuscles"]

        temporalisPosteriorRight = palpationPainExtraoral["temporalis_posterior_back_of_temple_right"]
        temporalisMiddleRight = palpationPainExtraoral["temporalis_middle_middle_of_temple_right"]
        temporalisAnteriorRight = palpationPainExtraoral["temporalis_anterior_front_of_temple_right"]
        masseterSuperiorRight = palpationPainExtraoral["masseter_superior_cheek_under_cheekbone_right"]
        masseterMiddleRight = palpationPainExtraoral["masseter_middle_cheek_side_of_face_right"]
        masseterInferiorRight = palpationPainExtraoral["masseter_inferior_cheek_jawline_right"]
        posteriorMandibularRight = palpationPainExtraoral["posterior_mandibular_region_jaw_throat_region_right"]
        submandibularRegionRight = palpationPainExtraoral["submandibular_region_under_chin_right"]

        temporalisPosteriorLeft = palpationPainExtraoral["temporalis_posterior_back_of_temple_left"]
        temporalisMiddleLeft = palpationPainExtraoral["temporalis_middle_middle_of_temple_left"]
        temporalisAnteriorLeft = palpationPainExtraoral["temporalis_anterior_front_of_temple_left"]
        masseterSuperiorLeft = palpationPainExtraoral["masseter_superior_cheek_under_cheekbone_left"]
        masseterMiddleLeft = palpationPainExtraoral["masseter_middle_cheek_side_of_face_left"]
        masseterInferiorLeft = palpationPainExtraoral["masseter_inferior_cheek_jawline_left"]
        posteriorMandibularLeft = palpationPainExtraoral["posterior_mandibular_region_jaw_throat_region_left"]
        submandibularRegionLeft = palpationPainExtraoral["submandibular_region_under_chin_left"]

        rightOptions = self.painOptions.getRightOptions().getOptions()
        rightOptions['''Temporalis (posterior) - "Back of temple"'''].\
            getButton(temporalisPosteriorRight).setChecked(True)
        rightOptions['''Temporalis (middle) - "Middle of temple"'''].\
            getButton(temporalisMiddleRight).setChecked(True)
        rightOptions['''Temporalis (anterior) - "Front of temple"'''].\
            getButton(temporalisAnteriorRight).setChecked(True)
        rightOptions['''Masseter (superior) - "Cheek/under cheekbone"'''].\
            getButton(masseterSuperiorRight).setChecked(True)
        rightOptions['''Masseter (middle) - "Cheek/side of face"'''].\
            getButton(masseterMiddleRight).setChecked(True)
        rightOptions['''Masseter (inferior) - "Cheek/jawline"'''].\
            getButton(masseterInferiorRight).setChecked(True)
        rightOptions['''Posterior mandibular region - "Jaw/throat region"'''].\
            getButton(posteriorMandibularRight).setChecked(True)
        rightOptions['''Submandibular region - "Under chin"'''].\
            getButton(submandibularRegionRight).setChecked(True)

        leftOptions = self.painOptions.getLeftOptions().getOptions()
        leftOptions['''Temporalis (posterior) - "Back of temple"'''].\
            getButton(temporalisPosteriorLeft).setChecked(True)
        leftOptions['''Temporalis (middle) - "Middle of temple"'''].\
            getButton(temporalisMiddleLeft).setChecked(True)
        leftOptions['''Temporalis (anterior) - "Front of temple"'''].\
            getButton(temporalisAnteriorLeft).setChecked(True)
        leftOptions['''Masseter (superior) - "Cheek/under cheekbone"'''].\
            getButton(masseterSuperiorLeft).setChecked(True)
        leftOptions['''Masseter (middle) - "Cheek/side of face"'''].\
            getButton(masseterMiddleLeft).setChecked(True)
        leftOptions['''Masseter (inferior) - "Cheek/jawline"'''].\
            getButton(masseterInferiorLeft).setChecked(True)
        leftOptions['''Posterior mandibular region - "Jaw/throat region"'''].\
            getButton(posteriorMandibularLeft).setChecked(True)
        leftOptions['''Submandibular region - "Under chin"'''].\
            getButton(submandibularRegionLeft).setChecked(True)


class PalpationPainJointPainPage(PalpationPainPage):
    def __init__(self):
        options = ['''Lateral pole - "outside"''', '''Posterior attachment - "inside ear"''']
        label = "Joint pain"
        super().__init__(options, label)

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        palpationJointPain = diagnosticData["PalpationPainJointPain"]

        lateralPoleRight = palpationJointPain["lateral_pole_outside_right"]
        posteriorAttachmentRight = palpationJointPain["posterior_attachment_inside_ear_right"]
        lateralPoleLeft = palpationJointPain["lateral_pole_outside_left"]
        posteriorAttachmentLeft = palpationJointPain["posterior_attachment_inside_ear_left"]

        rightOptions = self.painOptions.getRightOptions().getOptions()
        rightOptions['''Lateral pole - "outside"'''].getButton(lateralPoleRight).setChecked(True)
        rightOptions['''Posterior attachment - "inside ear"'''].getButton(posteriorAttachmentRight).setChecked(True)

        leftOptions = self.painOptions.getLeftOptions().getOptions()
        leftOptions['''Lateral pole - "outside"'''].getButton(lateralPoleLeft).setChecked(True)
        leftOptions['''Posterior attachment - "inside ear"'''].getButton(posteriorAttachmentLeft).setChecked(True)


class PalpationPainIntraoralPainPage(PalpationPainPage):
    def __init__(self):
        options = ['''Lateral pterygoid area - "Behind upper molars"''', '''Tendon of temporalis - "Tendon"''']
        label = "Intraoral muscle pain"
        super().__init__(options, label)

    def doLoadWithData(self, patientId):
        serializer = DatabaseDeserializer(self.wizard().getDatabase())
        diagnosticData = serializer.getDiagnosticDataDictById(patientId)
        palpationIntraoralPain = diagnosticData["PalpationPainIntraoralPain"]

        lateralPterygoidRight = palpationIntraoralPain["lateral_pterygoid_area_behind_upper_molars_right"]
        tendonTemporalisRight = palpationIntraoralPain["tendon_of_temporalis_tendon_right"]
        lateralPterygoidLeft = palpationIntraoralPain["lateral_pterygoid_area_behind_upper_molars_left"]
        tendonTemporalisLeft = palpationIntraoralPain["tendon_of_temporalis_tendon_left"]

        rightOptions = self.painOptions.getRightOptions().getOptions()
        rightOptions['''Lateral pterygoid area - "Behind upper molars"'''].\
            getButton(lateralPterygoidRight).setChecked(True)
        rightOptions['''Tendon of temporalis - "Tendon"'''].\
            getButton(tendonTemporalisRight).setChecked(True)

        leftOptions = self.painOptions.getLeftOptions().getOptions()
        leftOptions['''Lateral pterygoid area - "Behind upper molars"'''].\
            getButton(lateralPterygoidLeft).setChecked(True)
        leftOptions['''Tendon of temporalis - "Tendon"'''].\
            getButton(tendonTemporalisLeft).setChecked(True)
