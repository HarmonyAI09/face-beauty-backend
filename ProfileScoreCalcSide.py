def gonial_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "East Asian":
        default_plus = 4
    measurement_name = "Gonial angle(°)"
    level_count = 7
    min_range_array = [
        [112, 109.5, 106, 102, 97, 92, 80],
        [114, 111, 108, 104, 99, 94, 80],
    ]
    max_range_array = [
        [123, 125.5, 129, 133, 138, 143, 160],
        [125, 128, 131, 135, 140, 146, 160],
    ]
    score_array = [40, 20, 10, 5, -20, -40, -70]
    notes = [
        "Your jaw has an ideal shape. Since your Gonial angle is neither too obtuse or acute, your jaw is likely neither too square or steep/rounded in shape.",
        "Your jawline has a near ideal shape. Your jaw's structure may be slightly more rounded or squared than is preferred, but it is still within a harmonious range.",
        "Although your jawline does not have the most preferred shape, it still has a normal shape. Your jaw's structure may be slightly more rounded or squared than is preferred, but it is still within a normal range.",
        "Although your jawline does not have the most preferred shape, it still is within a reasonably normal range. Your jaw's structure may be noticeably rounded or squared, but it may not be enough to indicate facial abnormality.",
        "Your jawline's shape would not generally be considered favorable. It is either too square (low value) or rounded and lacking angularity (high value).",
        "Your jawline is beginning to stray into the extremes and would not generally be considered harmonious. It is likely that your jaw is either too square or rounded in shape."
        "Your jawline shape is at the extremes and would not generally be considered harmonious. It is likely that your jaw is either too square or rounded in shape.",
    ]
    advice = """There are a few effective ways to improve your gonial angle. The best course to take depends on the severity and specifics of your case. 
                1) lose body-fat to reveal the underlying angularity of your jaw. 
                2) correct malocclusion if that is causing your angle to be overly obtuse. (i.e., consult maxillofacial surgeon or orthodontist)
                3) wear a bite guard if you grind your teeth. Bruxism can wear down your teeth and give your jaw an overly flat appearance.
                4) Wraparound jaw implants to artificially create a jaw shape of your choosing."""

    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def nasofrontal_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "East Asian":
        default_plus = 4
    elif racial == "African":
        default_plus = -4
    elif racial == "Middle eastern":
        default_plus = 4
    measurement_name = "Nasofrontal angle (°)"
    level_count = 6
    min_range_array = [[106, 101, 97, 94, 88, 70], [122, 117, 113, 110, 107, 70]]
    max_range_array = [[129, 134, 138, 141, 147, 170], [143, 148, 152, 155, 158, 170]]
    score_array = [15, 7.5, 3.75, 1.876, -7.5, -15]
    notes = [
        "The angle formed between your brow ridge and nose is pleasant. Your brow region is neither too soft or harsh.",
        "Although not ideal, the angle formed between your brow ridge and nose is generally pleasant. Your brow region is neither too soft or harsh.",
        "Although not ideal, the angle formed between your brow ridge and nose is within a normal range. Your brow region is may begin to appear too protrusive (low values) or soft (high values).",
        "Although not ideal, the angle formed between your brow ridge and nose is within a reasonably normal range. Your brow region is may appear too protrusive (low values) or soft (high values).",
        "The angle formed between your brow ridge and nose is outside of a normal range. Your brow region is may appear too protrusive (low values) or soft (high values).",
        "The angle formed between your brow ridge and nose is outside at the extremes, indicating a lack of facial harmony. Your brow region is may appear too protrusive (low values) or soft (high values).",
    ]
    advice = """While difficult to change the morphology of the brow region, there are a few ways to improve your nasofrontal angle. This is a sensitive area to change and it is not as common as other procedures.
                1) Rhinoplasty can change the shape of the area around your nasion and dorsum, which can alter the angle.
                2) custom forehead implants around the brow region can add projection and lower the angle if desired."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def mandibular_plane_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "East Asian":
        default_plus = 2
    measurement_name = "Mandibular plane angle (°)"
    level_count = 6
    min_range_array = [[15, 14, 12.5, 10, 8, 0], [15, 14, 12.5, 10, 8, 0]]
    max_range_array = [[22, 27, 30, 32.5, 35, 45], [23, 27, 30, 32.5, 35, 45]]
    score_array = [12.5, 6.25, 3.125, 1.5625, -12.5, -20]
    notes = [
        "The slope of your mandible is harmonious, being neither too flat or downward grown. This is usually indicative of a healthy jaw and normal growth pattern.",
        "While not perfectly ideal, the slope of your mandible is harmonious, being neither too flat or downward grown. This is usually indicative of a healthy jaw and normal growth pattern.",
        "While not an ideal shape, the slope of your mandible is within a normal range of values. At this point, the growth of your jaw may indicate some hyper/hypo-divergent growth patterns, but it also may not.",
        "The slope of your mandible is slightly outside of a normal range of values. At this point, the growth of your jaw may indicate some hyper/hypo-divergent growth patterns. Your jaw may be either too flat (low values) or too steep (high values).",
        "The slope of your mandible is outside of a normal range of values. At this point, the growth of your jaw indicates some hyper/hypo-divergent growth patterns. Your jaw may be either too flat (low values) or too steep (high values).",
        "The slope of your mandible is far outside of a normal range of values. At this point, the growth of your jaw indicates some hyper/hypo-divergent growth patterns. Your jaw may be either too flat (low values) or too steep (high values).",
    ]
    advice = """
There are a few effective ways to improve your MPA. The best course to take depends on the severity and specifics of your case. Most of the same advice from the GA would apply here since the MPA helps form the GA.

1) lose body-fat to reveal the underlying angularity of your jaw.

2) correct malocclusion if that is causing your angle to be overly obtuse. You especially want to address any hyper/hypo divergent growth patterns, where your jaw can become too elongated or short. This would yield the most profound effect since most unideal MPA have to do with one's teeth. (i.e., consult maxillofacial surgeon or orthodontist)

3) wear a bite guard if you grind your teeth. Bruxism can wear down your teeth and give your jaw an overly flat appearance.

4) Wraparound jaw implants to artificially create a jaw shape of your choosing.
"""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def ramus_mandible_ratio_score(ratio, gender, racial):
    ratio = round(ratio, 2)
    default_plus = 0
    measurement_name = "Ramus to Mandible ratio"
    level_count = 6
    min_range_array = [
        [0.59, 0.54, 0.49, 0.41, 0.33, 0.1],
        [0.52, 0.48, 0.42, 0.34, 0.26, 0.1],
    ]
    max_range_array = [
        [0.78, 0.83, 0.88, 0.96, 1.04, 1.5],
        [0.70, 0.75, 0.8, 0.88, 0.96, 1.5],
    ]
    score_array = [10, 5, 2.5, 1.25, -5, -10]
    notes = [
        "The length of your ramus relative your mandible is harmonious. Your ramus is neither too long or short.",
        "Although not ideal, the length of your ramus relative your mandible is generally harmonious. Your ramus is neither too long or short.",
        "Although not ideal, the length of your ramus relative your mandible is within a normal range of values. Your ramus is neither too long or short.",
        "The length of your ramus relative your mandible is beginning to fall outside of the normal range. Your ramus may be considered too short (low values) or too long (high values).",
        "The length of your ramus relative your mandible falls outside of the normal range. Your ramus can be considered too short (low values) or too long (high values).",
        "Although not ideal, the length of your ramus relative your mandible is within a normal range of values. Your ramus is neither too long or short.",
    ]
    advice = """
The main thing we would seek to improving here is improving the ramus length. Shaving off bone and reducing ramus length is not really a viable procedure. For those who do need ramus shortening a unilateral Le Fort I osteotomy has been attempted in the literature. To add ramus height there is really only one option:

custom wraparound jaw implants can add overall volume to the jaw. Keep in mind this would also add height to the mandible, thereby lengthening your face. That is worth considering given your other facial assessments.
"""
    for i in range(level_count):
        if (
            ratio >= min_range_array[1 - gender][i] + default_plus
            and ratio <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                ratio,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        ratio,
        measurement_name,
        advice,
    )
def facial_convexity_glabella_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "African":
        default_plus = 2
    elif racial == "East Asian":
        default_plus = 1
    elif racial == "Hispanic":
        default_plus = 3
    elif racial == "Middle eastern":
        default_plus = -3
    elif racial == "South Asian":
        default_plus = -2
    measurement_name = "Facial convexity (glabella) (°)"
    level_count = 6
    min_range_array = [[168, 161, 163, 160, 155, 140], [166, 163, 161, 159, 155, 140]]
    max_range_array = [[176, 179, 181, 183, 184, 195], [175, 178, 180, 182, 184, 195]]
    score_array = [10, 5, 2.5, -2.5, -10, -30]
    notes = [
        "You have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with no severe overjet or underbite.",
        "Although not perfectly harmonious, you have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with perhaps some minor overjet (low values) or underbite (high values).",
        "Although not perfectly harmonious, you have a normal shape of the side profile. Neither part of your face -- upper, middle, or lower are in extreme disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
        "Your side profile shape is beginning to stray outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
        "Your side profile shape is outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
        "Your side profile shape is far outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in extreme disharmony to one another. You certainly have some occlusal issues like perhaps an overjet (low values) or underbite (high values).",
    ]
    advice = """
To improve your facial convexity, we want to try and improve the balance in projection of your facial thirds. This is primarily done through altering the position of the upper jaw (maxilla) and lower jaw (mandible). 

Consulting an orthodontist or maxillofacial surgeon is the best bet as the course of action would depend on the severity of your case. Some options are:

1) Orthognathic surgery to forcibly alter the position of your upper/lower jaw to be in better alignment. This is more financially costly and invasive. This would be appropriate in cases of severe malocclusion.

2) braces may be the only thing needed to align your jaw.

3) other orthodontic contraptions can set your teeth in proper alignment.

4) facial hair around the chin can improve perceived chin projection, which can increase this angle into the harmonious range.

Again, these are suggestions and giving a precise course of action would require consulting a specialist and taking X-rays."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def submental_cervical_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    measurement_name = "Submental cervical angle (°)"
    level_count = 5
    min_range_array = [[91, 81, 81, 75, 50], [91, 81, 81, 75, 50]]
    max_range_array = [[110, 120, 130, 140, 160], [110, 120, 130, 140, 160]]
    score_array = [10, 5, 2.5, -5, -10]
    notes = [
        "The angle between your neck and lower jaw is harmonious and defined.",
        "Although not perfectly ideal, the angle between your neck and lower jaw is generally harmonious and defined.",
        "Although not perfectly ideal, the angle between your neck and lower jaw is within a normal range.",
        "The angle between your neck and lower jaw is outside of the normal range and may indicate lacking jaw definition.",
        "The angle between your neck and lower jaw is far outside of the normal range and may indicate lacking jaw definition.",
    ]
    advice = """A few courses of action can improve the definition around your neck. 

1) lose body fat.

2) neck liposuction.

3) Other non-surgical subdermal skin tightening techniques may provide some improvement.
"""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def nasofacial_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "African":
        default_plus = 2
    elif racial == "Asian":
        default_plus = -3
    measurement_name = "Nasofacial angle (°)"
    level_count = 6
    min_range_array = [[30, 36, 28, 26.5, 25.5, 10], [30, 36, 28, 26.5, 25.5, 10]]
    max_range_array = [[36, 40, 42, 43.5, 44.5, 60], [36, 40, 42, 43.5, 44.5, 60]]
    score_array = [9, 4.5, 2.25, 1.125, -4.5, -9]
    notes = [
        "This angle indicates a harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "While not perfectly ideal, your angle indicates a harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "While not perfectly ideal, your angle indicates a normal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This may indicate that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
        "Your angle indicates a slightly abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This may indicate that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
        "Your angle indicates an abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This indicates that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
        "Your angle indicates an extremely abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. This indicates that your jaw's position relative to your nose is unfavorable, but it does not provide additional information regarding the relative positioning of your jaw like the facial convexity angle.",
    ]
    advice = """
Along with correcting any malocclusion (reference facial convexity glabella), there are a few ways to improve your nasofacial angle. The best course of action would depend on the specifics of your case:

1) Chin implants if your angle is too obtuse can help reduce the angle and boost harmony. Keep in mind this would have to consider other facial assessments as the change does not occur in isolation.

2) Rhinplasty to alter your nose shape in a specific way to either increase or reduce this angle. One such example would be reducing your nasal projection, which tends to reduce the angle and vice versa."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def nasolabial_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "African":
        default_plus = -11
    elif racial == "Hispanic":
        default_plus = 4
    elif racial == "East Asian":
        default_plus = -4
    elif racial == "Middle eastern":
        default_plus = -8
    elif racial == "South Asian":
        default_plus = 6
    measurement_name = "Nasolabial angle (°)"
    level_count = 7
    min_range_array = [[94, 90, 85, 81, 70, 65, 30], [96, 92, 87, 83, 79, 74, 30]]
    max_range_array = [
        [117, 121, 126, 130, 140, 150, 190],
        [118, 122, 127, 131, 144, 154, 190],
    ]
    score_array = [7.5, 3.75, 1.875, 0.9375, -3.75, -7.5, -15]
    notes = [
        "Your nose has a pleasant and ideal shape. Your nose is likely not too upturned or droopy and your philtrum probably has a pleasant shape.",
        "Your nose has a pleasant shape. Your nose is likely not too upturned or droopy and your philtrum probably has a pleasant shape.",
        "While not ideal, your nose has a normal shape. Your nose may begin to appear noticeably upturned or droopy and your philtrum may have a less than ideal shape.",
        "While not ideal, your nose has a reasonably normal shape. Your nose may begin to appear noticeably upturned or droopy and your philtrum may have a less than ideal shape.",
        "Your nose has an abnormal shape. Your nose may be noticeably upturned (high values) or droopy (low values) and your philtrum may have a less than ideal shape.",
        "Your nose has an extremely abnormal shape. Your nose may be noticeably upturned (high values) or droopy (low values) and your philtrum may have a less than ideal shape.",
        "Your nose has an extremely abnormal shape. Your nose may be noticeably upturned (high values) or droopy (low values) and your philtrum may have a less than ideal shape.",
    ]
    advice = """
Altering your nasolabial angle is fairly straightforward since it is in the isolated region of your nose. A rhinoplasty primarily aimed at addressing the columella and nasal tip region can alter the nasolabial angle."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def orbital_vector_score(value, gender, racial):
    measurement_name = "Orbital vector"
    if value == "positive":
        return (
            7.5,
            "Your nose has a pleasant and ideal shape. Your nose is likely not too upturned or droopy and your philtrum probably has a pleasant shape.",
            7.5,
            "Positive",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "slightly positive":
        return (
            3.75,
            "You have a slightly positive orbital vector, indicating no infraorbital hollowing. This is a youthful feature that is generally considered attractive.",
            7.5,
            "Positive",
            value,
            measurement_name,
            """To improve the youthfulness of the undereye region, filler is really the only option. Hyaluronic acid filler injected in the infraorbital region can add volume and create a rejuvenating effect. This would have to be a yearly event as the filler dissipates. 

Another potential option is gaining body-fat. This will not provide a substantial benefit, but as your face gains soft tissue in the form of fat, so does the region under your eyes to some degree.""",
        )
    elif value == "neutral":
        return (
            1.875,
            "You have a neutral orbital vector, indicating no infraorbital hollowing. While you could have more soft tissue protrusion under your eyes, this is a feature that is generally considered attractive.",
            7.5,
            "Positive",
            value,
            measurement_name,
            """To improve the youthfulness of the undereye region, filler is really the only option. Hyaluronic acid filler injected in the infraorbital region can add volume and create a rejuvenating effect. This would have to be a yearly event as the filler dissipates. 

Another potential option is gaining body-fat. This will not provide a substantial benefit, but as your face gains soft tissue in the form of fat, so does the region under your eyes to some degree.""",
        )
    elif value == "slightly negative":
        return (
            -3.75,
            "You have a slightly negative orbital vector, indicating some infraorbital hollowing. While you could have more soft tissue protrusion under your eyes, this is not yet extreme hollowing.",
            7.5,
            "Positive",
            value,
            measurement_name,
            """To improve the youthfulness of the undereye region, filler is really the only option. Hyaluronic acid filler injected in the infraorbital region can add volume and create a rejuvenating effect. This would have to be a yearly event as the filler dissipates. 

Another potential option is gaining body-fat. This will not provide a substantial benefit, but as your face gains soft tissue in the form of fat, so does the region under your eyes to some degree.""",
        )
    elif value == "very negative":
        return (
            -7.5,
            "You have a very negative orbital vector, indicating noticeable infraorbital hollowing. This is generally considered an unattractive feature.",
            7.5,
            "Positive",
            value,
            measurement_name,
            """To improve the youthfulness of the undereye region, filler is really the only option. Hyaluronic acid filler injected in the infraorbital region can add volume and create a rejuvenating effect. This would have to be a yearly event as the filler dissipates. 

Another potential option is gaining body-fat. This will not provide a substantial benefit, but as your face gains soft tissue in the form of fat, so does the region under your eyes to some degree.""",
        )
    return (
        -7.5,
        "You have a very negative orbital vector, indicating noticeable infraorbital hollowing. This is generally considered an unattractive feature.",
        7.5,
        "Positive",
        value,
        measurement_name,
        """To improve the youthfulness of the undereye region, filler is really the only option. Hyaluronic acid filler injected in the infraorbital region can add volume and create a rejuvenating effect. This would have to be a yearly event as the filler dissipates. 

Another potential option is gaining body-fat. This will not provide a substantial benefit, but as your face gains soft tissue in the form of fat, so does the region under your eyes to some degree.""",
    )
def total_facial_convexity_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "African":
        default_plus = 5
    elif racial == "Hispanic":
        default_plus = 2
    elif racial == "East Asian":
        default_plus = 4
    elif racial == "Middle eastern":
        default_plus = -3
    elif racial == "South Asian":
        default_plus = -1
    measurement_name = "Total facial convexity"
    level_count = 7
    min_range_array = [
        [137.5, 135.5, 132.5, 129.5, 126.5, 124.5, 100],
        [137.5, 135.5, 132.5, 129.5, 126.5, 124.5, 100],
    ]
    max_range_array = [
        [148.5, 150.5, 153.5, 156.5, 159.5, 161.5, 180],
        [148.5, 150.5, 153.5, 156.5, 159.5, 161.5, 180],
    ]
    score_array = [7.5, 3.75, 1.875, -3.75, -7.5, -15, -30]
    notes = [
        "The harmony of your lateral profile is pleasant when considering your nose. This means that your nose harmonizes well with the projection of your brow ridge and chin.",
        "The harmony of your lateral profile is generally pleasant when considering your nose. This means that your nose harmonizes well with the projection of your brow ridge and chin.",
        "The harmony of your lateral profile is normal when considering your nose. This means that your nose harmonizes reasonably well with the projection of your brow ridge and chin.",
        "The harmony of your lateral profile is beginning to appear abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
        "The harmony of your lateral profile is abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
        "The harmony of your lateral profile is extremely abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
        "The harmony of your lateral profile is extremely abnormal when considering your nose. This means that your nose harmonizes unfavorably with the projection of your brow ridge and chin.",
    ]
    advice = """
The same concepts of improvement would apply here as for the facial convexity (glabella) assessment. However, since this is the total profile, altering the nose's projection can also improve this assessment if that is the issue. We want to be careful to recognize whether your unfavorable angle is due to your malocclusion or your nose projection though.

If your angle is too high, you can get a Rhinoplasty to reduce the projection of your nose.

If your angle is too low, increasing the projection of your nose is possible, but less common. I would caution against this if your angle is not extreme."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def mentolabial_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    measurement_name = "Mentolabial angle"
    level_count = 6
    min_range_array = [[108, 94, 80, 75, 65, 40], [93, 79, 70, 65, 62, 40]]
    max_range_array = [[130, 144, 158, 165, 175, 200], [125, 139, 153, 160, 175, 200]]
    score_array = [7.5, 3.75, 1.875, -1.875, -3.75, -7.5]
    notes = [
        "You have a pleasant contour of the chin. The indent formed between your chin is neither too deep or flat.",
        "You have a generally pleasant contour of the chin. The indent formed between your chin is neither too deep or flat.",
        "You have a normal contour of the chin. The indent formed between your chin could be a bit more normalized since it is either too indented (low values) or flat (high values).",
        "You have a slightly abnormal contour of the chin. The indent formed between your chin could be a bit more normalized since it is either too indented (low values) or flat (high values).",
        "You have an abnormal contour of the chin. The indent formed between your chin could be a bit more normalized since it is too indented (low values) or flat (high values).",
        "You have an extremely abnormal contour of the chin. The indent formed between your chin could be a bit more normalized since it is too indented (low values) or flat (high values).",
    ]
    advice = """
The main things we would seek to address here are the projection of your chin and lower lip. There are a few ways to improve this assessment:

1) losing body-fat can make the indent between your chin and lower lip subtly more pronounced.

2) chin implants can reduce the angle if yours is too high.

3) lower lip filler can reduce the angle if yours is too high.

4) chin reduction surgery to increase the angle. Lower lip atrophy can also achieve this effect, but that tends to occur naturally with age.

5) facial hair in males around the chin can give the illusion of increasing this angle.
"""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def facial_convexity_nasion_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "African":
        default_plus = 2
    elif racial == "Hispanic":
        default_plus = 3
    elif racial == "East Asian":
        default_plus = 1
    elif racial == "Middle eastern":
        default_plus = -3
    elif racial == "South Asian":
        default_plus = -2
    measurement_name = "Facial convexity (nasion)"
    level_count = 6
    min_range_array = [[163, 160, 158, 155, 152, 120], [161, 158, 156, 153, 152, 120]]
    max_range_array = [[179, 173, 175, 178, 181, 195], [179, 173, 175, 178, 181, 195]]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    notes = [
        "You have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with no severe overjet or underbite.",
        "Although not perfectly harmonious, you have a pleasant shape of the side profile. Neither part of your face -- upper, middle, or lower are in disharmony to one another. You also likely have a pleasant dental occlusion with perhaps some minor overjet (low values) or underbite (high values).",
        "Although not perfectly harmonious, you have a normal shape of the side profile. Neither part of your face -- upper, middle, or lower are in extreme disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
        "Your side profile shape is beginning to stray outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
        "Your side profile shape is outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in disharmony to one another. You may have some occlusal issues like perhaps a moderate overjet (low values) or underbite (high values).",
        "Your side profile shape is far outside of the normal range. This can indicate that some part of your face -- upper, middle, or lower are in extreme disharmony to one another. You certainly have some occlusal issues like perhaps an overjet (low values) or underbite (high values).",
    ]
    advice = """
The same concepts of improvement would apply here as for the facial convexity (glabella) assessment. However, there is one caveat. If your angle is low, and it is not primarily a result of a malocclusion, then is may be due to the recessed position of your nasion. In that case, a Rhinoplasty can add projection to the top of your nose.
"""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def nasal_projection_score(value, gender, racial):
    value= round(value, 2)
    default_plus = 0
    if racial == "African":
        default_plus = -0.1
    elif racial == "Hispanic":
        default_plus = -0.07
    elif racial == "East Asian":
        default_plus = -0.1
    measurement_name = "Nasal projection"
    level_count = 6
    min_range_array = [
        [0.55, 0.5, 0.45, 0.37, 0.3, 0.1],
        [0.52, 0.47, 0.42, 0.34, 0.3, 0.1],
    ]
    max_range_array = [
        [0.68, 0.75, 0.78, 0.86, 0.95, 1.4],
        [0.68, 0.75, 0.78, 0.86, 0.95, 1.4],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    notes = [
        "You have an ideal nasal projection. Your nose is not too pronounced or unprojected.",
        "You have a near ideal nasal projection. Your nose is not too pronounced or unprojected.",
        "While not ideal, you have a normal nasal projection. Your nose may be considered slightly too projected (high values) or unprojected (low values).",
        "You have a slightly abnormal nasal projection. Your nose may be slightly too projected (high values) or unprojected (low values).",
        "You have an abnormal nasal projection. Your nose is slightly too projected (high values) or unprojected (low values).",
        "You have an extremely abnormal nasal projection. Your nose is slightly too projected (high values) or unprojected (low values).",
    ]
    advice = """
Rhinoplasty to reduce nasal projection is the primary way to address an overly projected nose. Increasing nasal projection is not as common, but some form of Rhinoplasty would also apply."""
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i] + default_plus
            and value <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                value,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        value,
        measurement_name,
        advice,
    )
def nasal_wh_ratio_score(value, gender, racial):
    value= round(value, 2)
    default_plus = 0
    if racial == "African":
        default_plus = -0.05
    elif racial == "Hispanic":
        default_plus = -0.03
    elif racial == "East Asian":
        default_plus = -0.12
    elif racial == "Middle eastern":
        default_plus = -0.03
    measurement_name = "Nasal W to H ratio"
    level_count = 6
    min_range_array = [
        [0.62, 0.55, 0.49, 0.45, 0.4, 0.1],
        [0.68, 0.61, 0.55, 0.51, 0.45, 0.1],
    ]
    max_range_array = [
        [0.88, 0.95, 1.01, 1.05, 1.1, 1.6],
        [0.93, 1.0, 1.06, 1.1, 1.13, 1.6],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -5, -15]
    notes = [
        "You have an ideal Nasal WHR. The projection of your nose is proportionate relative to its height.",
        "You have a near ideal Nasal WHR. The projection of your nose is proportionate relative to its height.",
        "You have a normal Nasal WHR. The projection of your nose is reasonably proportionate relative to its height.",
        "You have a slightly abnormal Nasal WHR. The projection of your nose may be slightly too much (high values) or too little (low values) compared to its height.",
        "You have an abnormal Nasal WHR. The projection of your nose may be too much (high values) or too little (low values) compared to its height.",
        "You have an extremely abnormal Nasal WHR. The projection of your nose may be too much (high values) or too little (low values) compared to its height.",
    ]
    advice = """
Reducing the vertical height of the nose is not really possible aside from a Lefort 1 advancement or some kind of invasive maxillofacial surgery. 

The more superficial option is a Rhinoplasty to reduce nasal projection is the primary way to address an overly projected nose and create a lower ratio.

Increasing nasal projection is not as common, but some form of Rhinoplasty would also apply. to increase the ratio
"""
    for i in range(level_count):
        if (
            value >= min_range_array[1 - gender][i] + default_plus
            and value <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                value,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        value,
        measurement_name,
        advice,
    )
def ricketts_E_line_score(value, gender, racial):
    measurement_name = "Ricketts' E line"
    advice = """
Fixing any malocclusion generally helps to improve the harmony of your chin, lips, and nose.

Aside from that, lip filler, chin filler, and rhinoplasty can also be specifically catered to improve the harmony of your lip assessments. This concept would apply to all four of the lip assessments (EHSB).

Facial hair in males may also be a viable option to increase perceived chin projection if that is lacking."""
    if value == "ideal":
        return (
            5,
            "You have a pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "near ideal":
        return (
            2.5,
            "You have a reasonably pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            advice,
        )
    else:
        return (
            0,
            "You do not have a pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            advice,
        )
def holdaway_H_line_score(value, gender, racial):
    measurement_name = "Holdaway H line"

    if value == "ideal":
        return (
            5,
            "You have a pleasant harmony between your chin and lips according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "near ideal":
        return (
            2.5,
            "You have a reasonably pleasant harmony between your chin and lips according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    else:
        return (
            0,
            "You have an unpleasant harmony between your chin and lips according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
def steiner_S_line_score(value, gender, racial):
    measurement_name = "Steiner S line"
    if value == "ideal":
        return (
            5,
            "You have a pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "near ideal":
        return (
            2.5,
            "You have a reasonably pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    else:
        return (
            0,
            "You do not have a pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
def burstone_line_score(value, gender, racial):
    measurement_name = "Burstone line"
    if value == "ideal":
        return (
            5,
            "You have a pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "near ideal":
        return (
            2.5,
            "You have a reasonably pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
    else:
        return (
            0,
            "You do not have a pleasant harmony between your chin, lips, and nose according to this specific assessment.",
            5,
            "Ideal",
            value,
            measurement_name,
            "N/A",
        )
def nasomental_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "African":
        default_plus = -3
    elif racial == "East Asian":
        default_plus = 3
    measurement_name = "Nasomental angle (°)"
    level_count = 6
    min_range_array = [[125, 120, 118, 116, 114, 100], [125, 120, 118, 116, 114, 100]]
    max_range_array = [
        [132, 133.5, 134.5, 136.5, 138.5, 150],
        [132, 133.5, 134.5, 136.5, 138.5, 150],
    ]
    score_array = [5, 2.5, 1.25, 0.625, -2.5, -10]
    notes = [
        "This angle indicates a harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "This angle indicates a reasonably harmonious balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a pleasant jaw position, but not always. It mainly indicates that your nose is harmonious relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "While not ideal, this angle indicates a normal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have a normal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "This angle indicates a slightly abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It can indicate that you have an abnormal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "This angle indicates an abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It probably indicates that you have an abnormal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
        "This angle indicates an extremely abnormal balance between your nose and chin. This encompasses your nose shape, position, and your chin's position. It probably indicates that you have an extremely abnormal jaw position, but not always. It mainly indicates that your nose is normal relative to your chin, but doesn't provide additional information on whether your chin is harmonious relative to other parts of your face.",
    ]
    advice = """
Along with correcting any malocclusion (reference facial convexity glabella), there are a few ways to improve your nasomental angle. The best course of action would depend on the specifics of your case:

1) Chin implants if your angle is too acute can help increase the angle and boost harmony. Keep in mind this would have to consider other facial assessments as the change does not occur in isolation.

2) Rhinplasty to alter your nose shape in a specific way to either increase or reduce this angle. One such example would be reducing your nasal projection, which tends to increase the angle and vice versa. 

Generally, this angle is the same conceptually as the nasofacial, but the angles vary inversely."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def gonion_mouth_relationship_score(value, gender, racial):
    measurement_name = "Gonion to mouth relationship"

    if value == "below":
        return (
            5,
            "Your ramus has sufficient vertical growth.",
            5,
            "Below",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "in_line":
        return (
            1,
            "Your ramus has normal vertical growth, but could ideally have more length.",
            5,
            "Below",
            value,
            measurement_name,
            "Reference the notes for the ramus:mandible ratio. Improving this assessment also requires increasing ramus length.",
        )
    elif value == "above":
        return (
            0,
            "Your ramus has lacking vertical growth.",
            5,
            "Below",
            value,
            measurement_name,
            "Reference the notes for the ramus:mandible ratio. Improving this assessment also requires increasing ramus length.",
        )
    else:
        return (
            -5,
            "Your ramus has severely lacking vertical growth.",
            5,
            "Below",
            value,
            measurement_name,
            "Reference the notes for the ramus:mandible ratio. Improving this assessment also requires increasing ramus length.",
        )
def recession_relative_frankfort_plane_score(value, gender, racial):
    measurement_name = "Recession relative to frankfort plane"
    advice = """
This assessment tends to correlate to the facial convexity. To improve it, you can consider a few things:

1) fixing malocclusion
2) chin implants if your chin is in a retruded position

3) facial hair in males to add perceived chin projection

4) orthognathic surgery in severe cases with severely retruded chins"""
    if value == "none":
        return (
            5,
            "According to this assessment, you have no notable recession regarding the position of your chin relative to your nasion.",
            5,
            "None",
            value,
            measurement_name,
            "N/A",
        )
    elif value == "slight":
        return (
            1,
            "According to this assessment, you have slight recession regarding the position of your chin relative to your nasion.",
            5,
            "None",
            value,
            measurement_name,
            advice,
        )
    elif value == "moderate":
        return (
            0,
            "According to this assessment, you have moderate recession regarding the position of your chin relative to your nasion.",
            5,
            "None",
            value,
            measurement_name,
            advice,
        )
    else:
        return (
            -10,
            "According to this assessment, you have extreme recession regarding the position of your chin relative to your nasion.",
            5,
            "None",
            value,
            measurement_name,
            advice,
        )
def browridge_inclination_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    measurement_name = "Browridge inclination angle (°)"
    level_count = 7
    min_range_array = [[13, 10, 8, 6, 4, 2, 0], [10, 7, 5, 3, 1, 1, 0]]
    max_range_array = [[24, 27, 29, 31, 33, 36, 45], [22, 25, 27, 29, 31, 39, 45]]
    score_array = [4, 2, 1, 0.5, -2, -10, -20]
    notes = [
        "Your forehead is not overly sloped back or flat. It is harmonious in shape.",
        "While not ideal, your forehead is not overly sloped back or flat.",
        "While not ideal, your forehead has a normal shape. It is not overly sloped back (high values) or flat (low values).",
        "Your forehead has a slightly  abnormal shape. It is likely overly sloped back (high values) or flat (low values).",
        "Your forehead has an abnormal shape. It is likely overly sloped back (high values) or flat (low values).",
        "Your forehead has an extremely abnormal shape. It is either overly sloped back (high values) or flat (low values).",
        "Your forehead has an extremely abnormal shape. It is either overly sloped back (high values) or flat (low values).",
    ]
    advice = """
There are a few ways to improve the shape of your frontal bone, or forehead:

1) custom forehead implants to make your forehead flatter in shape if it is too sloped back. Achieving drastic results may not be that realistic. 

2) using a hairstyle that covers your forehead to distract from or hide this specific feature.

3) custom forehead implants localized near the brow region to increase the slant of your forehead if it is too flat. This would also have to consider other assessments like the nasofrontal angle and facial convexity."""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )
def nasal_tip_angle_score(angle, gender, racial):
    angle = round(angle, 2)
    default_plus = 0
    if racial == "Middle eastern":
        default_plus = -10
    measurement_name = "Nasal tip angle (°)"
    level_count = 6
    min_range_array = [[112, 108, 104, 100, 97, 70], [118, 115, 111, 108, 105, 70]]
    max_range_array = [[125, 129, 133, 137, 140, 170], [131, 134, 138, 141, 144, 170]]
    score_array = [4, 2, 1, 0.5, -2, -4]
    notes = [
        "You have a harmonious nasal tip that is not overly upturned or droopy.",
        "You have a generally harmonious nasal tip that is not overly upturned or droopy.",
        "You have a normal nasal tip angle, but it may be considered slightly too upturned (high values) or droopy (low values).",
        "You have an abnormal nasal tip angle, indicating that your nose is either too upturned (high values) or droopy (low values).",
        "You have an abnormal nasal tip angle, indicating that your nose is either too upturned (high values) or droopy (low values).",
        "You have an extremely abnormal nasal tip angle, indicating that your nose is either too upturned (high values) or droopy (low values).",
    ]
    advice = """
Rhinplasty specifically localized around the nasal tip is extremely common to address either an overly droopy or upturned nasal tip. This is also called nasal tip rotation rhinoplasty.
"""
    for i in range(level_count):
        if (
            angle >= min_range_array[1 - gender][i] + default_plus
            and angle <= max_range_array[1 - gender][i] + default_plus
        ):
            return (
                score_array[i],
                notes[i],
                score_array[0],
                [
                    min_range_array[1 - gender][0] + default_plus,
                    max_range_array[1 - gender][0] + default_plus,
                ],
                angle,
                measurement_name,
                "N/A" if i == 0 else advice,
            )
    return (
        score_array[-1],
        notes[-1],
        score_array[0],
        [
            min_range_array[1 - gender][0] + default_plus,
            max_range_array[1 - gender][0] + default_plus,
        ],
        angle,
        measurement_name,
        advice,
    )