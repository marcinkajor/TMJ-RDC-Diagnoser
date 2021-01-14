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
"horizontal_mm": "34", "middle_line_mm": "123", "middle_line_alignment_relative_to_the_jaw": "R"},
"VerticalMandibleMovements": {"right_side_mm": "45", "left_side_mm": "45", "forward_mm": "66",
"right_side_right": "None", "left_side_right": "Muscle", "forward_right": "Join", "right_side_left": "Muscle",
"left_side_left": "Join", "forward_left": "Both"}, "SoundsInJointAbduction": {"left_opening_mm": "TEST_abduction_mm",
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
"PalpationPainExtraoralMuscles": {"temporalis_posterior_back_of_temple_right": "No pain",
"temporalis_middle_middle_of_temple_right": "Mild pain", "temporalis_anterior_front_of_temple_right": "Moderate pain",
"masseter_superior_cheek_under_cheekbone_right": "Severe pain",
"masseter_middle_cheek_side_of_face_right": "Moderate pain", "masseter_inferior_cheek_jawline_right": "Mild pain",
"posterior_mandibular_region_jaw_throat_region_right": "No pain", "submandibular_region_under_chin_right": "Mild pain",
"temporalis_posterior_back_of_temple_left": "No pain", "temporalis_middle_middle_of_temple_left": "Mild pain",
"temporalis_anterior_front_of_temple_left": "Moderate pain",
"masseter_superior_cheek_under_cheekbone_left": "Severe pain",
"masseter_middle_cheek_side_of_face_left": "Moderate pain", "masseter_inferior_cheek_jawline_left": "Mild pain",
"posterior_mandibular_region_jaw_throat_region_left": "No pain", "submandibular_region_under_chin_left": "Mild pain"},
"PalpationPainJointPain": {"lateral_pole_outside_right": "No pain",
"posterior_attachment_inside_ear_right": "Mild pain", "lateral_pole_outside_left": "Moderate pain",
"posterior_attachment_inside_ear_left": "Severe pain"},
"PalpationPainIntraoralPain": {"lateral_pterygoid_area_behind_upper_molars_right": "No pain",
"tendon_of_temporalis_tendon_right": "Mild pain", "lateral_pterygoid_area_behind_upper_molars_left": "Moderate pain",
"tendon_of_temporalis_tendon_left": "Severe pain"}'''

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
