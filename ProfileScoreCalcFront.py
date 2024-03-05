from schemas import frontProfileSchema, profileResponseSchema, MeasurementOverview

def getMeasurementLevel(p:frontProfileSchema, racingValueDict:dict, minArray, maxArray, lvlCnt, value):
    racingVal = racingValueDict[p.racial]
    for i in range(lvlCnt):
        if value>=minArray[1-p.gender][i]+racingVal and value<=maxArray[1-p.gender][i]+racingVal:
            return i
    return 0

def funcEyeSeparationRatio(p:frontProfileSchema):
    measureName = "Eye Separation Ratio(%)"
    defaultRacingVal = {"Caucasian":0, "African":1, "East Asian":-0.7,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[44.3, 43.6, 43.1, 42.6, 42, 41, 35],[45, 44.3, 43.8, 43.3, 42.7, 42, 35]]
    maxArray = [[47.4, 48.4, 48.9, 49.4, 50, 51, 58],[47.9, 48.6, 49.1, 49.6, 50.2, 51, 58]]
    scoreArray = [35, 17.5, 8.75, 4.375, 0, -8.75, -17.5]
    notes = [
        "Your eyes are harmoniously spaced relative to your facial width.",
        "While not perfectly ideal, your eyes are generally harmoniously spaced relative to your facial width.",
        "While not perfectly ideal, your eyes are still normally spaced relative to your facial width. They may begin to appear either slightly close set (low values) or wide set (high values).",
        "Your eyes have a slightly abnormal spacing relative to your facial width. They may begin to appear either close set (low values) or wide set (high values).",
        "Your eyes have a moderately abnormal spacing relative to your facial width. They may begin to appear either too close set (low values) or wide set (high values).",
        "Your eyes have an abnormal spacing relative to your facial width. They appear either too close set (low values) or wide set (high values).",
        "Your eyes have an extremely abnormal spacing relative to your facial width. They appear either too close set (low values) or wide set (high values).",
    ]
    advice = '''While extremely difficult to change the actual underlying morphology of your eyes, there are a few ways to improve this assessment:
    1) lose body-fat to create a thinner face, thereby increasing your ESR and making your eyes appear wider set. The opposite also holds true -- if you have overly wide set eyes, gaining some weight on your face can lead to the appearance of more normally spaced eyes.
    2) hairstyles to alter your perceived facial width. Along the same lines as facial fat, you can play around with hairstyles that add width to your face or reduce it. For example, if you have extremely wide set eyes, longer hairstyles that cover the sides of your face or add width can improve your perceived facial harmony. If your eyes are closer set, shorter hairstyles with shorter sides may suit your face better.
    3) Cheekbone implants to increase the width of your face. Or, zygomatic reduction surgery to do the opposite. 
    Overall, the only thing you can do is alter your facial width, but not the actual spacing of your eyes themselves.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.eyeSeparationRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.eyeSeparationRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcFacialThirds(p:frontProfileSchema):
    measureName = "Facial Thirds(%)"
    defaultRacingVal = {"Caucasian":0, "African":1, "East Asian":-0.7,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray_favor = [[29.5, 28, 26.5, 25, 23.5, 22.5, 18],[30, 29.5, 27, 25, 24, 23, 18]]
    maxArray_favor = [[36.5, 38, 39.5, 41, 42.5, 43.5, 50],[36, 37.5, 39, 41, 42, 43, 50]]
    minArray_basic = [[31.5, 30.5, 29, 26.5, 25, 24, 18],[31.5, 31, 29.5, 29.5, 28, 27, 18]]
    maxArray_basic = [[34.5, 35.5, 37, 39.5, 41, 42, 50],[34.5, 35, 36.5, 37.5, 38, 39, 50]]
    scoreArray = [30, 15, 7.5, 3.75, 0, -7.5, -15]
    notes = [
        "Your facial thirds are harmoniously distributed, leading to a balanced appearance of the upper, middle, and lower parts of your face.",
        "Although not ideal, your facial thirds are harmoniously distributed, leading to a balanced appearance of the upper, middle, and lower parts of your face.",
        "Although not ideal, your facial thirds are normally distributed, leading to a reasonably balanced appearance of the upper, middle, and lower parts of your face. One of your thirds may begin to appear overly short or long in relation to the others.",
        "Your facial thirds are slightly abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds likely appears overly short or long in relation to the others.",
        "Your facial thirds are abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds appears overly short or long in relation to the others.",
        "Your facial thirds are extremely abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds appears overly short or long in relation to the others.",
        "Your facial thirds are extremely abnormal in their distribution, leading to an unbalanced appearance of the upper, middle, and lower parts of your face. One of your thirds appears overly short or long in relation to the others.",
    ]
    advice = '''There are many ways to alter your facial thirds. The best course of action would depend on your specific case:
    1) hairstyle to add length to your forehead if your upper third is short or reduce it if your upper third is too tall. 
    2) facial hair to add perceived vertical height to the lower third.
    3) Rhinoplasty to reduce a droopy nasal tip, since the middle third begins at the bottom of the nasal tip. This would give a shorter middle third. 
    4) Custom jaw implants to add vertical height to your lower third if needed. Again, this must consider the harmony of other facial assessments.'''
    value = p.facialThirds
    if p.gender:
        if value[2] == max(value): 
            for i in range(lvlCnt):
                for index in range(3):
                    if value[index] < minArray_favor[1-p.gender][i] or value[index] > maxArray_favor[1-p.gender][i]: break
                    if index == 2: return MeasurementOverview(measureName, scoreArray[i], scoreArray[0], p.facialThirds, 
                               [minArray_favor[1-p.gender][0]+defaultRacingVal[p.racial], maxArray_favor[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[i], "N/A" if index == 0 else advice)
        else:
            for i in range(lvlCnt):
                for index in range(3):
                    if value[index] < minArray_basic[1-p.gender][i] or value[index] > maxArray_basic[1-p.gender][i]: break
                    if index == 2: return MeasurementOverview(measureName, scoreArray[i], scoreArray[0], p.facialThirds, 
                               [minArray_basic[1-p.gender][0]+defaultRacingVal[p.racial], maxArray_basic[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[i], "N/A" if index == 0 else advice)
    else:
        if value[2] == min(value):
            for i in range(lvlCnt):
                for index in range(3):
                    if value[index] < minArray_favor[1-p.gender][i] or value[index] > maxArray_favor[1-p.gender][i]: break
                    if index == 2: return MeasurementOverview(measureName, scoreArray[i], scoreArray[0], p.facialThirds, 
                               [minArray_favor[1-p.gender][0]+defaultRacingVal[p.racial], maxArray_favor[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[i], "N/A" if index == 0 else advice)
        else:
            for i in range(lvlCnt):
                for index in range(3):
                    if value[index] < minArray_basic[1-p.gender][i] or value[index] > maxArray_basic[1-p.gender][i]: break
                    if index == 2: return MeasurementOverview(measureName, scoreArray[i], scoreArray[0], p.facialThirds, 
                               [minArray_basic[1-p.gender][0]+defaultRacingVal[p.racial], maxArray_basic[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[i], "N/A" if index == 0 else advice)
def funcLateralCanthalTilt(p:frontProfileSchema):
    measureName = "Lateral Canthal Tilt(°)"
    defaultRacingVal = {"Caucasian":0, "African":1.5, "East Asian":2,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}    
    lvlCnt = 7
    minArray = [[5.2, 4, 3, 0, -2, -4, -10], [6, 4.8, 3.6, 1.5, 0, -3, -10]]
    maxArray = [[8.5, 9.7, 10.7, 13.7, 15.7, 17.9, 25],[9.6, 10.8, 12, 14.1, 15.6, 18.2, 25]]
    scoreArray = [25, 12.5, 6.25, 3.125, -5, -10, -20]
    notes = [
        "Your eyes have a harmonious tilt, meaning they are not overly droopy or upturned.",
        "Your eyes have a generally harmonious tilt, meaning they are not overly droopy or upturned.",
        "Although not perfectly ideal, your eyes have a normal tilt, meaning they are not overly droopy or upturned.",
        "Your eyes have a slightly abnormal tilt. They may begin to appear slightly droopy (low values) or overly upturned (high values)",
        "Your eyes have a slightly abnormal tilt. They may begin to appear slightly droopy (low values) or overly upturned (high values)",
        "Your eyes have an abnormal tilt.  They appear overly droopy (low values) or overly upturned (high values)",
        "Your eyes have an extremely  abnormal tilt.  They appear overly droopy (low values) or overly upturned (high values)",
    ]
    advice = '''A cosmetic lateral Canthoplasty is the primary way to increase the tilt of one's eyes. 
    Reducing the tilt of one's eyes is not as common, but it is possible by reducing the position of the outer eye corner.
    Blepharoplasty is also an option to address a sagging eyelid if the perceived tilt of one's eyes is more of an issue that the actual numerical value itself.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.lateralCanthalTilt)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.lateralCanthalTilt, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcFacialWHRatio(p:frontProfileSchema):
    measureName = "Facial Width-Height Ratio"
    defaultRacingVal = {"Caucasian":0, "African":0.03, "East Asian":-0.04,"South Asian":0.02, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[1.9, 1.85, 1.8, 1.75, 1.7, 1.66, 1.3],[1.9, 1.85, 1.8, 1.75, 1.7, 1.66, 1.3]]
    maxArray = [[2.06, 2.11, 2.16, 2.21, 2.26, 2.3, 2.3],[2.06, 2.11, 2.16, 2.21, 2.26, 2.3, 2.3]]
    scoreArray = [25, 12.5, 6.25, 3.125, 0, -7.5, -15]
    notes = [
        "You have an ideal FWHR, indicating a facial width and midface height that harmonize well with one another. Your midface region (i.e., FWHR) is not overly compact or elongated in shape.",
        "You have a near ideal FWHR, indicating a facial width and midface height that harmonize well with one another. Your midface region (i.e., FWHR) is not overly compact or elongated in shape.",
        "Although not ideal, you have a normal FWHR, indicating a facial width and midface height that harmonize reasonably well with one another. Your midface region (i.e., FWHR) may begin to appear slightly long or compact, but it is not an aesthetic flaw.",
        "You have a normal FWHR, indicating a facial width and midface height that harmonize reasonably well with one another. Your midface region (i.e., FWHR) may begin to appear slightly long or compact, but it is not a large aesthetic flaw.",
        "You have a slightly abnormal FWHR, indicating a facial width and midface height that do not harmonize that well. Your midface region (i.e., FWHR) likely appears overly long or overly compact. Still, this is not at the extremes.",
        "You have an abnormal FWHR, indicating a facial width and midface height that do not harmonize that well. Your midface region (i.e., FWHR) likely appears overly long or overly compact. Your ratio is beginning to stray into the extremes.",
        "You have an extremely abnormal FWHR, indicating a facial width and midface height that do not harmonize that well. Your midface region (i.e., FWHR) likely appears overly long or overly compact. Your ratio is at the extremes.",
    ]
    advice = '''There are a few ways to alter FWHR, but it is largely unchangeable due to it being linked heavily to one's bone structure:
    1) gaining or losing facial- fat can either increase or reduce your FWHR, respectively. 
    2) Cheekbone implants can increase facial width, thereby increasing FWHR slightly.
    3) upper lip filler can reduce the vertical distance of your midface, thereby increasing FWHR slightly. 
    4) lowering the brow position is not really surgically possible or advised, but if you can grow eyebrow hair more interior towards your nose, that can increase FWHR.
    Reducing FWHR is not as possible aside from losing facial fat and invasive zygomatic remodeling (cheekbone reduction surgery).'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.facialWHRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.facialWHRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcJawFrontalAngle(p:frontProfileSchema):
    measureName = "Jaw Frontal Angle(°)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[84.5, 80.5, 76.5, 72.5, 69.5, 66.5, 40],[86, 82.5, 79, 75.5, 72, 69, 40]]
    maxArray = [[95, 99, 103, 107, 110, 113, 150],[97, 100.5, 104, 107.5, 111, 114, 150]]
    scoreArray = [25, 12.5, 6.25, 3.125, 0, -7.5, -15]
    notes = [
        "Your jaw has an ideal contour in the front profile, indicated by a harmonious angle in this assessment.",
        "Your jaw has a near ideal contour in the front profile, indicated by a harmonious angle in this assessment.",
        "Your jaw has a slightly unideal contour in the front profile. It may be considered either slightly too flat (high values) or steep (low values).",
        "Your jaw has a slightly unideal contour in the front profile. It may be considered either slightly too flat (high values) or steep (low values).",
        "Your jaw has an unideal contour in the front profile. It is considered either slightly too flat (high values) or steep (low values).",
        "Your jaw has an extremely unideal contour in the front profile. It is considered either slightly too flat (high values) or steep (low values).",
        "Your jaw has an extremely unideal contour in the front profile. It is considered either slightly too flat (high values) or steep (low values).",
    ]
    advice = '''There are a few ways to improve the contour of your jaw:
    1) losing facial-fat can reveal your jaw contour better, often resulting in a more pleasant angle.
    2) Custom jaw implants to specifically design your jaw's desired shape.
    3) fixing malocclusion in the same way that it would address your MPA. Your JFA is heavily tied to your MPA.
    4) Chin implants -- a wider chin tends to reduce this angle, while a narrower chin increased it. Facial hair can also conceptually do this to some degree.
    5) Masseter reduction surgery. An overly wide jaw can tend to increase this angle. Conversely, increasing your jaw width through chewing exercises can increase this angle if yours is on the lower end.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.jawFrontalAngle)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.jawFrontalAngle, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcCheekboneHighSetedness(p:frontProfileSchema):
    measureName = "Cheekbone Height(%)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[81, 76, 70, 65, 60, 55, 10], [83, 79, 73, 68, 63, 58, 10]]
    maxArray = [[100, 81, 76, 70, 65, 60, 55], [100, 83, 79, 73, 68, 63, 58]]
    scoreArray = [20, 12.5, 6.25, 3.125, 0, -10, -15]
    notes = [
        "You have high cheekbones, which are generally preferred when it comes to facial aesthetics.",
        "Although not incredibly high-set, you still have reasonably high cheekbones, which are generally preferred when it comes to facial aesthetics.",
        "You do not have what would be considered high cheekbones, but your cheekbones are also not low-set. They could be considered medium to perhaps ever so slightly high set.",
        "You do not have what would be considered high cheekbones, but your cheekbones are also not low-set. They could be considered medium set.",
        "You have what would be classified as low set cheekbones, where the widest part of your face is likely more towards the base of your nose rather than closer to your eyes.",
        "You have what would be classified as low set cheekbones, where the widest part of your face is likely more towards the base of your nose rather than closer to your eyes. This can lead to a droopy or melted face appearance and your face generally lacks the structure that is considered attractive.",
        "You have what would be classified as extremely low set cheekbones, where the widest part of your face is likely more towards the base of your nose rather than closer to your eyes. This can lead to a droopy or melted face appearance and your face generally lacks the structure that is considered attractive.",
    ]
    advice = '''We will assume that the main goal is to achieve higher set cheekbones. To do this, you can either lose body fat to reveal the underlying cheekbone structure if you have high cheekbones. Or, you can use cheekbone implants to increase the protrusion and width of your face near your eyes. Making that the widest part of your face will give the appearance of high cheekbones.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.cheekBoneHeight)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.cheekBoneHeight, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcTotalFacialWHRatio(p:frontProfileSchema):
    measureName = "Total Facial Height-Width Ratio"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[1.33, 1.3, 1.26, 1.23, 1.2, 1.18, 1.0],[1.29, 1.26, 1.22, 1.19, 1.17, 1.15, 1.0]]
    maxArray = [[1.38, 1.41, 1.45, 1.48, 1.51, 1.53, 1.7],[1.35, 1.38, 1.42, 1.45, 1.47, 1.49, 1.7]]
    scoreArray = [15, 7.5, 3.75, 0, -3.75, -7.5, -15]
    notes = [
        "You have an ideal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is neither too long or compact.",
        "You have a near ideal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is neither too long or compact.",
        "Although not ideal, you have a normal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is perhaps ever so slightly too long (high values) or short (low values).",
        "You have a slightly abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is perhaps slightly too long (high values) or short (low values).",
        "You have an abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is too long (high values) or short (low values).",
        "You have an extremely abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is too long (high values) or short (low values).",
        "You have an extremely abnormal face shape when it comes to your face's height and width (Total FWHR/facial index). Your face is too long (high values) or short (low values).",
    ]
    advice = '''Improving total FWHR/facial index depends on the underlying cause and severity of your overly elongated or compact face shape:
    1) Losing facial fat can increase the ratio, while gaining facial fat can reduce it.
    2) Cheekbone implants or reduction can reduce or increase this ratio, respectively.
    3) Hairstyles can manipulate the perceived dimensions of your face similar to the facial thirds. If your face is overly long, a wider hairstyle may help and vice versa. 
    4) Facial hair can add height to your face is your ratio is too low.
    5) Correcting any hyper/hypo divergent growth pattern at the orthodontist or maxillofacial surgeon can increase the harmony of your face's vertical height.
    6) Overly clenching and wearing down your teeth can result in a deep bite and reduce your facial height, thereby reducing this ratio. Although, this is not suggested as a method of improvement; rather, it is more so to avoid a reduction in facial height along with jaw joint problems.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.totalFacialWHRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.totalFacialWHRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcBigonialWidth(p:frontProfileSchema):
    measureName = "Bigonial Width(%)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[85.5, 83.5, 80.5, 77.5, 75, 70, 50],[81.5, 79.5, 76.5, 73.5, 70.5, 69, 50]]
    maxArray = [[92, 94, 97, 100, 102.5, 105, 120],[88.5, 90.5, 93.5, 96.5, 99.5, 102, 120]]
    scoreArray = [15, 7.5, 3.75, 1.875, -2.5, -5, -10]
    notes = [
        "You have an ideal jaw width. Your jaw is neither too wide or narrow relative to your total facial width.",
        "You have a near ideal jaw width. Your jaw is neither too wide or narrow relative to your total facial width.",
        "Although not ideal, you have a normal width. Your jaw may be slightly too narrow (low values) or wide (high values).",
        "You have a normal width. Your jaw may be either slightly too narrow (low values) or wide (high values), but it does not likely appear abnormal in terms of facial harmony.",
        "You have an abnormal width. Your jaw can be considered either too narrow (low values) or wide (high values).",
        "You have an abnormal width. Your jaw can be considered either too narrow (low values) or wide (high values).",
        "You have an extremely abnormal width. Your jaw can be considered either too narrow (low values) or wide (high values).",
    ]
    advice = '''There are a few ways to alter this ratio:
    1) Increasing the cross-sectional muscle area of your masseter muscle through chewing tough foods can increase your jaw width if your ratio is low.
    2) Masseter reduction surgery can reduce your jaw width if it is too wide.
    3) Increasing your facial width through cheekbone implants can reduce your jaw's perceived width.
    4) Thicker sideburns can reduce your jaw's perceived width.
    5) A thicker beard can increase your jaw's perceived width.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.bigonialWidth)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.bigonialWidth, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcChin2PhiltrumRatio(p:frontProfileSchema):
    measureName = "Chin To Philtrum Ratio"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 6
    minArray = [[2.05, 1.87, 1.75, 1.55, 1.2, 1.0, 0.1],[2.0, 1.85, 1.7, 1.5, 1.2, 1.0, 0, 1]]
    maxArray = [[2.55, 2.73, 2.85, 3.2, 3.55, 3.85, 5.0],[2.5, 2.65, 2.8, 3, 3.15, 3.8, 5.0]]
    scoreArray = [12.5, 6.25, 3.125, 1.5625, -3, -6, -10]
    notes = [
        "Your chin is harmoniously proportioned relative to your philtrum. This indicates that neither your chin or philtrum are too long or short.",
        "While not perfectly ideal, your chin is harmoniously proportioned relative to your philtrum. This indicates that neither your chin or philtrum are not excessively long or short.",
        "While not perfectly ideal, your chin is normally proportioned relative to your philtrum. This indicates that neither your chin or philtrum are not excessively long or short.",
        "Your chin is somewhat abnormally proportioned relative to your philtrum. This can indicate that your chin is too short (low values) or tall (high values) relative to your philtrum.",
        "Your chin is abnormally proportioned relative to your philtrum. This can indicate that your chin is too short (low values) or tall (high values) relative to your philtrum.",
        "Your chin is abnormally proportioned relative to your philtrum. This can indicate that your chin is too short (low values) or tall (high values) relative to your philtrum.",
    ]
    advice = '''To alter this ratio we want to consider the chin and lips. Altering the position of the subnasale is not really possible.
    1) chin implants to increase this ratio.
    2) correcting malocclusion to fix any excessive or lacking chin projection and height.
    3) facial hair to increase perceived chin height and increase this ratio
    4) upper lip filler to increase this ratio
    5) lower lip filler to reduce this ratio'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.chin2PhiltrumRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.chin2PhiltrumRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcNeckWidthRatio(p:frontProfileSchema):
    measureName = "Neck Width(%)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[90, 85, 80, 75, 70, 65, 30], [75, 69, 67, 65, 62, 57, 30]]
    maxArray = [[100, 102, 105, 107, 75, 70, 130],[87, 93, 95, 97, 100, 103, 130]]
    scoreArray = [10, 5, 1, -5, -7, -9, -12]
    notes = [
        "You have an ideal neck width that adds balance to your facial appearance.",
        "You have a near ideal neck width that adds balance to your facial appearance.",
        "Although not perfectly harmonious, you have a normal neck width.",
        "Your neck can be considered slightly too narrow (low values) or too wide (high values).",
        "Your neck can be considered too narrow (low values) or too wide (high values).",
        "Your neck can be considered extremely narrow (low values) or extremely wide (high values).",
        "Your neck can be considered extremely narrow (low values) or extremely wide (high values).",
    ]
    advice = '''Altering your neck width is fairly straightforward. Losing body fat tends to make the neck thinner and vice versa. Exercising your neck through resistance training can increase its circumference and width in the front view.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.neckWidth)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.neckWidth, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcMouthNoseWidthRatio(p:frontProfileSchema):
    measureName = "Mouth-Nose Width Ratio"
    defaultRacingVal = {"Caucasian":0, "African":-0.05, "East Asian":-0.04,"South Asian":0, "Hispanic": -0.03, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[1.38, 1.34, 1.3, 1.26, 1.22, 1.18, 0.9],[1.45, 1.4, 1.35, 1.3, 1.25, 1.21, 0.9]]
    maxArray = [[1.53, 1.57, 1.61, 1.65, 1.69, 1.73, 2.2],[1.67, 1.72, 1.77, 1.82, 1.87, 1.91, 2.2]]
    scoreArray = [10, 5, 2.5, 1.25, 0, -5, -10]
    notes = [
        "Your mouth width harmonizes extremely well with your nose width.",
        "Your mouth width harmonizes well with your nose width.",
        "Your mouth width harmonizes reasonably well with your nose width. Your nose/mouth may be considered slightly too narrow or wide, resulting in a less than ideal proportion.",
        "Your mouth width does not harmonize that well with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
        "Your mouth width does not harmonize well with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
        "Your mouth width harmonizes poorly with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
        "Your mouth width harmonizes extremely poorly with your nose width. Your nose/mouth may be considered too narrow or wide, resulting in a less than ideal proportion.",
    ]
    advice = '''To alter this ratio, we primarily want to change the nasal width as altering mouth width is more invasive and does not tend to produce as favorable results.
    Rhinoplasty can be used to reduce your nasal width (higher ratios), or increase it (lower ratios). The latter is less common, but possible.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.mouthWidth2NoseWidthRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.mouthWidth2NoseWidthRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcMidfaceRatio(p:frontProfileSchema):
    measureName = "Midface Ratio"
    defaultRacingVal = {"Caucasian":0, "African":0.02, "East Asian":0.02,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[0.93, 0.9, 0.88, 0.85, 0.8, 0.77, 0.5],[1.0, 0.97, 0.95, 0.92, 0.87, 0.84, 0.5]]
    maxArray = [[1.01, 1.04, 1.06, 1.09, 1.14, 1.17, 1.5],[1.1, 1.13, 1.15, 1.18, 1.23, 1.26, 1.5]]
    scoreArray = [10, 5, 2.5, 1.25, 0, -5, -10]
    notes = [
        "You have a harmonious interior (or central) midface structure that is neither too compact or elongated.",
        "You have a generally harmonious interior (or central) midface structure that is neither too compact or elongated.",
        "You have a reasonably harmonious interior (or central) midface structure. It may be considered slightly too elongated (low values) or compact (high values).",
        "You have a slightly unharmonious interior (or central) midface structure. It may be considered too elongated (low values) or compact (high values).",
        "You have an unharmonious interior (or central) midface structure. It can be considered too elongated (low values) or compact (high values).",
        "You have an extremely unharmonious interior (or central) midface structure. It can be considered too elongated (low values) or compact (high values).",
        "You have an extremely unharmonious interior (or central) midface structure. It can be considered too elongated (low values) or compact (high values).",
    ]
    advice = '''Since we cannot really alter the distance between your pupils, the only way to really alter this ratio is through upper lip filler to increase the ratio.
    Some more invasive midface procedures like Lefort 1 can make the midface more vertically compact. thereby reducing the ratio further. Other forms of orthognathic surgery may result in some changes to the midface structure as well.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.midFaceRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.midFaceRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcEyebrowPositionRatio(p:frontProfileSchema):
    measureName = "Eyebrow Position Ratio"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0.3,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[0, 0.65, 0.95, 1.2, 1.5, 1.8, 2.1],[0.4, 0.3, 0, 1.15, 1.35, 1.85, 2.1]]
    maxArray = [[0.65, 0.95, 1.2, 1.5, 1.8, 2.1, 4.0],[0.85, 1, 1.35, 1.75, 2, 2.3, 4.0]]
    scoreArray = [10, 5, 2.5, 0, -2.5, -5, -7.5]
    notes = [
        "You have an ideal positioning of your eyebrows above your eyes. A lower position is typically preferred among younger demographics. Your eyebrows could generally be considered low-set, which typically leads to a more striking appearance.",
        "You have a near ideal positioning of your eyebrows above your eyes. Your eyebrows could be considered medium-low set in the male range, and medium set in the female range.",
        "You have a normal positioning of your eyebrows above your eyes. Your eyebrows could be considered medium set in the male range, and medium-high set in the female range.",
        "You have a normal positioning of your eyebrows above your eyes. Your eyebrows could be considered slightly high set in the male range, and high set in the female range.",
        "You have a slightly abnormal positioning of your eyebrows above your eyes. Your eyebrows could be considered high set. This may lead to the appearance of a more elongated midface region.",
        "You have an unideal positioning of your eyebrows above your eyes. Your eyebrows could be considered very high set. This may lead to the appearance of a more elongated midface region.",
        "You have an unideal positioning of your eyebrows above your eyes. Your eyebrows could be considered extremely high set. This may lead to the appearance of a more elongated midface region.",
    ]
    advice = '''This assessment is not really surgically alterable to be more favorable. However, in some cases where higher eyebrows result in an overall more harmonious face (factoring in other assessments), a brow lift can be a viable option.
    Filler around the brows can perhaps lower the brow position, but it is not something commonly done and it may throw off the appearance of your brow region.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.eyebrowPositionRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.eyebrowPositionRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcEyeSpacingRatio(p:frontProfileSchema):
    measureName = "Eye Spacing Ratio"
    defaultRacingVal = {"Caucasian":0.02, "African":0.02, "East Asian":0.32,"South Asian":0.02, "Hispanic": 0.02, "Middle eastern": 0.02,"Other":0.02}
    lvlCnt = 7
    minArray = [[0.9, 0.86, 0.81, 0.76, 0.65, 0.6, 0.4],[0.9, 0.86, 0.81, 0.76, 0.65, 0.6, 0.4]]
    maxArray = [[1.01, 1.05, 1.07, 1.14, 1.2, 1.4, 2],[1.01, 1.05, 1.07, 1.14, 1.2, 1.4, 2]]
    scoreArray = [10, 5, 2.5, 0, -2.5, -5, -10]
    notes = [
        "Your eyes have a harmonious spacing relative to one another.",
        "Your eyes have a generally harmonious spacing relative to one another.",
        "Although not ideal, your eyes have a normal spacing relative to one another. They may appear slightly close together (low values) or far apart (high values), but it is nothing extreme.",
        "Although not ideal, your eyes have a normal spacing relative to one another. They may appear somewhat close together (low values) or far apart (high values), but it is nothing extreme.",
        "Your eyes have an abnormal spacing relative to one another. They may appear either overly close together (low values) or far apart (high values).",
        "Your eyes have an extremely abnormal spacing relative to one another. They may appear either overly close together (low values) or far apart (high values).",
        "Your eyes have an extremely abnormal spacing relative to one another. They may appear either overly close together (low values) or far apart (high values).",
    ]
    advice = '''Aside from illusions in the form of makeup and lash length, there is no real way to change the structural distance between your eyes.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.eyeSpacingRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.eyeSpacingRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcEyeAspectRatio(p:frontProfileSchema):
    measureName = "Eye Aspect Ratio"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[2.8, 2.6, 2.4, 2.2, 2, 1.8, 0],[2.55, 2.35, 2.15, 1.95, 1.75, 1.8, 0]]
    maxArray = [[3.6, 3.8, 4, 4.2, 4.4, 4.6, 6],[3.2, 3.4, 3.6, 3.8, 4.0, 4.6, 6]]
    scoreArray = [10, 5, 2.5, 1.25, 0, -5, -10]
    notes = [
        "Your eyes have an ideal shape in terms of their width and height. Your eyes are neither too narrow and elongated or round in shape.",
        "Your eyes have a near ideal shape in terms of their width and height. Your eyes are neither too narrow and elongated or round in shape.",
        "Your eyes have a normal shape in terms of their width and height. Your eyes may be considered either slightly too round (low values) or narrow (high values) in shape.",
        "Your eyes have a slightly abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape.",
        "Your eyes have an abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape. Overly round eyes can begin to look too beady and overly narrow one's lack the ability to display emotional cues as well. Both extremes are generally not attractive.",
        "Your eyes have an extremely abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape. Overly round eyes can begin to look too beady and overly narrow one's lack the ability to display emotional cues as well. Both extremes are generally not attractive.",
        "Your eyes have an extremely abnormal shape in terms of their width and height. Your eyes may be considered either too round (low values) or narrow (high values) in shape. Overly round eyes can begin to look too beady and overly narrow one's lack the ability to display emotional cues as well. Both extremes are generally not attractive.",
    ]
    advice = '''Lower lid blepharoplasty can increase this ratio if a sagging lower lid is the culprit. 
    In the cases of overlying soft tissue in the upper lid region, blepharoplasty can increase the perceived height and roundness of your eyes.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.eyeAspectRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.eyeAspectRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcLowerUpperLipRatio(p:frontProfileSchema):
    measureName = "Lower-Upper Lip Ratio"
    defaultRacingVal = {"Caucasian":0, "African":-0.2, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[1.4, 1.1, 0.9, 0.7, 0.4, 0.1, 0.1],[1.35, 1.05, 0.85, 0.75, 0.35, 0.1, 0.1]]
    maxArray = [[2.0, 2.3, 2.5, 2.7, 3.0, 3.5, 5],[2.0, 2.3, 2.5, 2.7, 3.0, 3.5, 5]]
    scoreArray = [7.5, 3.75, 1.875, 0.9375, 0, -5, -10]
    notes = [
        "Your lower and upper lip are ideally proportioned relative to one another.",
        "Your lower and upper lip are near ideally proportioned relative to one another.",
        "Although not ideal, your lower and upper lip are normally proportioned relative to one another. Your upper lip may be slightly too full (high values) or thin (low values) relative to your upper lip.",
        "Your lower and upper lip are slightly abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
        "Your lower and upper lip are abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
        "Your lower and upper lip are abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
        "Your lower and upper lip are abnormally proportioned relative to one another. Your upper lip may be too full (high values) or thin (low values) relative to your upper lip. This may also indicate lacking upper lip volume of the upper lip itself rather than the inherent fullness of the lower lip.",
    ]
    advice = '''Lip filler aimed at increasing the upper or lower lip volume is the best way to address this proportion.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.lowerLip2UpperLipRatio)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.lowerLip2UpperLipRatio, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcDeviationIAA(p:frontProfileSchema):
    measureName = "Deviation Of IAA&JFA(°)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 6
    minArray = [[0, 2.5, 5, 10, 15, 20], [0, 2.5, 5, 10, 15, 20]]
    maxArray = [[2.5, 5, 10, 15, 20, 100], [2.5, 5, 10, 15, 20, 100]]
    scoreArray = [7, 3.75, 1.875, 0.9375, -3.75, -7.5]
    notes = [
        "You have an ideal harmony between your JFA and IAA.",
        "You have a near ideal harmony between your JFA and IAA.",
        "You have a normal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
        "You have a normal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
        "You have an abnormal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
        "You have an extremely abnormal harmony between your JFA and IAA. The difference between your angles may indicate something disharmonious about your eye spacing or jaw shape. You can reference the IAA, ESR, and JFA for more info.",
    ]
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.deviationOfJFA2IAA)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.deviationOfJFA2IAA, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A")
def funcEyebrowTilt(p:frontProfileSchema):
    measureName = "Eyebrow Tilt(°)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 6
    minArray = [[5, 3, 0, -2, -4, -15], [11, 9, 6, 4, 2, -15]]
    maxArray = [[13, 15, 18, 20, 22, 40], [18.7, 20.7, 23.7, 25.7, 27.7, 40]]
    scoreArray = [6, 3, 1.5, -3, -6, -9]
    notes = [
        "Your eyebrows have an ideal tilt. They are neither too upturned or droopy when accounting for inter-sex variability.",
        "Your eyebrows have a near ideal tilt. They are neither too upturned or droopy when accounting for inter-sex variability.",
        "Although not ideal, your eyebrows have a normal tilt. They may be considered slightly too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
        "Your eyebrows have a slightly abnormal tilt. They may be considered too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
        "Your eyebrows have an abnormal tilt. They may be considered too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
        "Your eyebrows have an extermely abnormal tilt. They may be considered too upturned (high values) or droopy (low values) when accounting for inter-sex variability.",
    ]
    advice = '''Altering the tilt of your brows can primarily be done through superficial techniques (e.g., plucking, shaving, shaping, waxing, threading, etc.).
    Sometimes though, the shape of your brows is tied to your brow ridge's actual morphology. In that case, there is not an easy way to change its shape. In the case of droopy eyebrows, an eyebrow lift can also help.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.eyebrowTilt)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.eyebrowTilt, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcBitemporalWidth(p:frontProfileSchema):
    measureName = "Bitemporal Width(%)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":-2, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[84, 82, 79, 77, 74, 71, 50], [79, 76, 73, 70, 67, 65, 50]]
    maxArray = [[95, 97, 100, 102, 105, 108, 125],[92, 95, 98, 101, 104, 106, 125]]
    scoreArray = [5, 2.5, 1.25, -2.5, -5, -7.5, -10]
    notes = [
        "Your forehead has an ideal width relative to your cheekbones. Your forehead is neither too narrow nor wide.",
        "Your forehead has a near ideal width relative to your cheekbones. Your forehead is neither too narrow nor wide.",
        "Although not ideal, your forehead has a normal width relative to your cheekbones. Your forehead may be considered either slightly too wide (high values) or narrow (low values).",
        "Your forehead has a slightly abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
        "Your forehead has an abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
        "Your forehead has an extremely abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
        "Your forehead has an extremely abnormal width relative to your cheekbones. Your forehead may be considered either too wide (high values) or narrow (low values).",
    ]
    advice = '''Altering your forehead width will mostly have to do with altering your hairline. While altering this proportion is generally not necessary unless it is an extreme case, there are a few ways to do so:
    1) laser hair removal to widen an overly narrow hairline.
    2) shaving your hairline
    3) using a hairstyle to cover your forehead
    4) altering your hair length. For example, wider bitemporal widths may suit shorter sides, while narrow foreheads may suit longer hairstyles.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.bitemporalWidth)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.bitemporalWidth, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcLowerThirdProporation(p:frontProfileSchema):
    measureName = "Lower Third Proportion(%)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 6
    minArray = [[30.6, 29.6, 28.4, 27.2, 26.6, 20],[31.2, 30.2, 29.2, 28.2, 27.2, 20]]
    maxArray = [[34, 35, 36.2, 37.4, 38, 45], [34.5, 35.5, 36.5, 37.5, 38.5, 45]]
    scoreArray = [5, 2.5, 1.25, -2.5, -5, -7.5]
    notes = [
        "Your lower third has a harmonious spacing between its features.",
        "Your lower third has a harmonious spacing between its features.",
        "Although not ideal, your lower third has a normal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either slightly too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
        "Your lower third has a slightly abnormal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
        "Your lower third has an abnormal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
        "Your lower third has an extremely abnormal spacing between its features. The upper portion (upper lip/philtrum) of your lower third may be either too short (low values) or long (high values) relative to the lower portion (chin/lower lip).",
    ]
    advice = '''Addressing this assessment is similar to others, with a few distinctions:
    1) altering chin height through the various aforementioned methods (i.e., surgery, facial hair)
    2) Rhinoplasty to reduce the droopiness of the nasal tip, thereby increasing this proportion.
    Altering lip size does not substantially affect this proportion.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.lowerThirdProportion)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.lowerThirdProportion, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcLpsilateralAlarAngle(p:frontProfileSchema):
    measureName = "Ipsilateral Alar Angle(°)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":0,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[84, 82, 79, 77, 75, 73, 50], [84, 82, 79, 77, 75, 73, 50]]
    maxArray = [[95, 97, 100, 102, 104, 106, 150],[95.5, 97.5, 100.5, 102.5, 104.5, 106.5, 150]]
    scoreArray = [2.5, 1.25, 0.63, 0, -1.25, -2.5, -5]
    notes = [
        "Your midface structure retains a harmonious balance.",
        "Your midface structure retains a harmonious balance.",
        "Although not perfectly ideal, your midface structure retains a normal balance. Your angle may indicate a slightly elongated nasal region and close set eyes (low values). Or, it may indicate a slightly short nose and wide set eyes (high values).",
        "Although not perfectly ideal, your midface structure retains a normal balance. Your angle may indicate a slightly elongated nasal region and close set eyes (low values). Or, it may indicate a slightly short nose and wide set eyes (high values).",
        "Your midface structure lacks balance. Your angle may indicate an elongated nasal region and close set eyes (low values). Or, it may indicate a short nose and wide set eyes (high values).",
        "Your midface structure lacks balance. Your angle may indicate an extremely elongated nasal region and close set eyes (low values). Or, it may indicate a short nose and wide set eyes (high values).",
        "Your midface structure lacks balance. Your angle may indicate an extremely elongated nasal region and close set eyes (low values). Or, it may indicate a short nose and wide set eyes (high values).",
    ]
    advice = '''Altering the spacing between your eyes is not really feasible, so the only way to change this measurement is to alter the position of your nasal tip. Namely, Rhinoplasty to reduce nasal tip droopiness can increase this angle.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.ipsilateralAlarAngle)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.ipsilateralAlarAngle, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)
def funcMedialCanthalAngle(p:frontProfileSchema):
    measureName = "Medial Canthal Angle(°)"
    defaultRacingVal = {"Caucasian":0, "African":0, "East Asian":8,"South Asian":0, "Hispanic": 0, "Middle eastern": 0,"Other":0}
    lvlCnt = 7
    minArray = [[20, 17, 15, 13, 11, 9, 5], [22, 20, 17, 15, 13, 11, 5]]
    maxArray = [[42, 50, 56, 63, 69, 75, 120], [44, 52, 58, 65, 71, 77, 120]]
    scoreArray = [10, 5, 2.5, -2.5, -5, -7.5, -10]
    notes = [
        "The inner corner of your eye is harmonious. It has distinct shape and angularity, while not being overly angular.",
        "The inner corner of your eye is generally harmonious. It has distinct shape and angularity, while not being overly angular.",
        "The inner corner of your eye is somewhat harmonious. It may either lack some distinct angularity (high values) or be overly sharp (low values).",
        "The inner corner of your eye is somewhat disharmonious. It may either lack some distinct angularity (high values) or be overly sharp (low values).",
        "The inner corner of your eye is  disharmonious. It either lacks some distinct angularity (high values) or is overly sharp (low values).",
        "The inner corner of your eye is very disharmonious. It either lacks some distinct angularity (high values) or is overly sharp (low values).",
        "The inner corner of your eye is extremely disharmonious. It either lacks some distinct angularity (high values) or is overly sharp (low values).",
    ]
    advice = '''There is no surgery specifically addressed at altering the medial canthus, but Canthoplasty or Blepharoplasty would alter this to some effect.'''
    index = getMeasurementLevel(p, defaultRacingVal, minArray, maxArray, lvlCnt, p.medialCanthalAngle)
    return MeasurementOverview(measureName, scoreArray[index], scoreArray[0], p.medialCanthalAngle, 
                               [minArray[1-p.gender][0]+defaultRacingVal[p.racial], maxArray[1-p.gender][0]+defaultRacingVal[p.racial]],
                               notes[index], "N/A" if index == 0 else advice)

def mainProcess(frontProfile:frontProfileSchema):
    mainProcess = profileResponseSchema()
    mainProcess.clear()
    mainProcess.update(funcEyeSeparationRatio(frontProfile))
    mainProcess.update(funcFacialThirds(frontProfile))
    mainProcess.update(funcLateralCanthalTilt(frontProfile))
    mainProcess.update(funcFacialWHRatio(frontProfile))
    mainProcess.update(funcJawFrontalAngle(frontProfile))
    mainProcess.update(funcCheekboneHighSetedness(frontProfile))
    mainProcess.update(funcTotalFacialWHRatio(frontProfile))
    mainProcess.update(funcBigonialWidth(frontProfile))
    mainProcess.update(funcChin2PhiltrumRatio(frontProfile))
    mainProcess.update(funcNeckWidthRatio(frontProfile))
    mainProcess.update(funcMouthNoseWidthRatio(frontProfile))
    mainProcess.update(funcMidfaceRatio(frontProfile))
    mainProcess.update(funcEyebrowPositionRatio(frontProfile))
    mainProcess.update(funcEyeSpacingRatio(frontProfile))
    mainProcess.update(funcEyeAspectRatio(frontProfile))
    mainProcess.update(funcLowerUpperLipRatio(frontProfile))
    mainProcess.update(funcDeviationIAA(frontProfile))
    mainProcess.update(funcEyebrowTilt(frontProfile))
    mainProcess.update(funcBitemporalWidth(frontProfile))
    mainProcess.update(funcLowerThirdProporation(frontProfile))
    mainProcess.update(funcLpsilateralAlarAngle(frontProfile))
    mainProcess.update(funcMedialCanthalAngle(frontProfile))
    return mainProcess.result()