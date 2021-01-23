# double braces needed
# source :https://stackoverflow.com/questions/16356810/string-format-a-json-string-gives-keyerror
TEST_PERSONAL_DATA = '''"PersonalData": {"name": "John", "surname": "Wick", "age": "45", "pesel": "TEST_pesel",
                        "sex": "Male"}'''

TEST_DIAGNOSTIC_DATA = '''"InitialData": {"pain_side": "TEST_pain_side", "right_pain_area": "TEST_right_pain_area",
"left_pain_area": "TEST_left_pain_area"},
"AbductionMovement": {"abduction_movement": "TEST_abduction_movement", "specific_description": ""},
"VerticalMovementRange": {"used_foretooth": "21", "no_pain_opening_mm": "TEST_vertical_movement_range_mm",
"max_active_opening_mm": "TEST_vertical_movement_range_mm",
"max_passive_opening_mm": "TEST_vertical_movement_range_mm", "max_active_opening_right": "TEST_opening",
"max_passive_opening_right": "TEST_opening",
"max_active_opening_left": "TEST_opening", "max_passive_opening_left": "TEST_opening"},
"IncisorsGap": {"vertical_mm": "TEST_incisal_overlap",
"horizontal_mm": "34", "middle_line_mm": "TEST_middle_line_mm",
"middle_line_alignment_relative_to_the_jaw": "TEST_middle_line_side"},
"VerticalMandibleMovements": {"right_side_mm": "TEST_vertical_mandible_mm", "left_side_mm": "TEST_vertical_mandible_mm",
"forward_mm": "66",
"right_side_right": "TEST_vertical_movement_pain", "left_side_right": "TEST_vertical_movement_pain",
"forward_right": "TEST_vertical_movement_pain", "right_side_left": "TEST_vertical_movement_pain",
"left_side_left": "TEST_vertical_movement_pain", "forward_left": "TEST_vertical_movement_pain"},
"SoundsInJointAbduction": {"left_opening_mm": "TEST_abduction_mm",
"left_closing_mm": "TEST_abduction_mm", "right_opening_mm": "TEST_abduction_mm", "right_closing_mm": "TEST_abduction_mm",
"left_opening_click_elimination": "TEST_elimination",
"left_closing_click_elimination": "TEST_elimination", "right_opening_click_elimination": "TEST_elimination",
"right_closing_click_elimination": "TEST_elimination", "left_opening_sound": "TEST_abduction_sound",
"left_closing_sound": "TEST_abduction_sound", "right_opening_sound": "TEST_abduction_sound",
"right_closing_sound": "TEST_abduction_sound"}, "SoundsInJointHorizontalMovements":
{"right_side_right": "None", "left_side_right": "Clear crepitations", "forward_right": "Slight crepitations",
"right_side_left": "Slight crepitations", "left_side_left": "Clear crepitations", "forward_left": "Click"},
"PalpationPainNoPain": {"mastoid_process_lateral_upper_part_right": "No pain",
"frontal_pupil_line_beneath_hair_right": "Mild pain", "vertex_1_cm_lateral_from_skull_prominence_right":
"Moderate pain", "mastoid_process_lateral_upper_part_left": "Severe pain",
"frontal_pupil_line_beneath_hair_left": "Moderate pain", "vertex_1_cm_lateral_from_skull_prominence_left": "Mild pain"},
"PalpationPainExtraoralMuscles": {"temporalis_posterior_back_of_temple_right": "TEST_palpation_E9",
"temporalis_middle_middle_of_temple_right": "TEST_palpation_E9", "temporalis_anterior_front_of_temple_right":
"TEST_palpation_E9", "masseter_superior_cheek_under_cheekbone_right": "TEST_palpation_E9",
"masseter_middle_cheek_side_of_face_right": "TEST_palpation_E9",
"masseter_inferior_cheek_jawline_right": "TEST_palpation_E9",
"posterior_mandibular_region_jaw_throat_region_right": "TEST_palpation_E9",
"submandibular_region_under_chin_right": "TEST_palpation_E9",
"temporalis_posterior_back_of_temple_left": "TEST_palpation_E9",
"temporalis_middle_middle_of_temple_left": "TEST_palpation_E9",
"temporalis_anterior_front_of_temple_left": "TEST_palpation_E9",
"masseter_superior_cheek_under_cheekbone_left": "TEST_palpation_E9",
"masseter_middle_cheek_side_of_face_left": "TEST_palpation_E9",
"masseter_inferior_cheek_jawline_left": "TEST_palpation_E9",
"posterior_mandibular_region_jaw_throat_region_left": "TEST_palpation_E9",
"submandibular_region_under_chin_left": "TEST_palpation_E9"},
"PalpationPainJointPain": {"lateral_pole_outside_right": "TEST_palpation_E10a",
"posterior_attachment_inside_ear_right": "TEST_palpation_E10b", "lateral_pole_outside_left": "TEST_palpation_E10a",
"posterior_attachment_inside_ear_left": "TEST_palpation_E10b"},
"PalpationPainIntraoralPain": {"lateral_pterygoid_area_behind_upper_molars_right": "TEST_palpation_E11",
"tendon_of_temporalis_tendon_right": "TEST_palpation_E11",
"lateral_pterygoid_area_behind_upper_molars_left": "TEST_palpation_E11",
"tendon_of_temporalis_tendon_left": "TEST_palpation_E11"}'''

TEST_RECORD = '''{{{}, {}}}'''.format(TEST_PERSONAL_DATA, TEST_DIAGNOSTIC_DATA)


def generateTestRecordE2(pesel: str, painSide: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_pain_side", painSide)


def generateTestRecordE3(pesel: str, option: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_right_pain_area", option).\
        replace("TEST_left_pain_area", option)


def generateTestRecordE4(pesel: str, option: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_abduction_movement", option)


def generateTestRecordE5(pesel: str, mm: str, pain: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_vertical_movement_range_mm", mm).\
        replace("TEST_incisal_overlap", mm).replace("TEST_opening", pain)


def generateTestRecordE6(pesel: str, mm: str, elimination: str, sound: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_abduction_mm", mm).\
        replace("TEST_elimination", elimination).replace("TEST_abduction_sound", sound)


def generateTestRecordE7(pesel: str, mm: str, middleLineSide: str):
    assert(middleLineSide in ["L", "R"])
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_vertical_mandible_mm", mm). \
        replace("TEST_middle_line_mm", mm).replace("TEST_middle_line_side", middleLineSide)


def generateTestRecordE8(pesel: str, pain: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_vertical_movement_pain", pain)


def generateTestRecordPalpationE9(pesel: str, pain: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_palpation_E9", pain)


def generateTestRecordPalpationE10a(pesel: str, pain: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_palpation_E10a", pain)


def generateTestRecordPalpationE10b(pesel: str, pain: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_palpation_E10b", pain)


def generateTestRecordPalpationE11(pesel: str, pain: str):
    return TEST_RECORD.replace("TEST_pesel", pesel).replace("TEST_palpation_E11", pain)
