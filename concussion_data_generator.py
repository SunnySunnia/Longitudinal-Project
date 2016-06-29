#! python
#
#  concussion_data_generator.py
#
#
#  Created by Bill Bosl on 06/12/2016.
#  Copyright (c) 2016 MindLight Medical. All rights reserved.
#
#  Generates simulated responses for Sport Concussion Questionnaire
#
#   General medical data
#   ID: Subject Number:
#   Age: in years
#   Gender:  [M, F]
#   Race: [0:unknown, 1:European, 2:African, 3:Native American, 4:Latino, 5:Asian, 6:Pacific Islander]
#   Neuropyschiatric_condition: [0: none, 1:epilepsy, 2: autism spectrum disorder, 3: ADHD, 4: cerebral palsy]
#   Meds: [0: none, 1: antiepileptics, 2: attention, 3: antipsychotic, 4: depression]
#   TBI: [0: no concussion, 1: mild, 2: moderate, 3: severe]
#   A.1 Time of injury: date
#   A.2 Sport/Team:
#   A.3 Number of Previous Concussions/Date(s): <enter list of dates, month and year are sufficient>
#   A.4 Headache        0-6
#   A.5 Pressure in head    0-6
#   A.6 Neck Pain       0-6
#   A.7 Nausea or Vomiting      0-6
#   A.8 Dizziness       0-6
#   A.9 Blurred Vision  0-6
#   A.10 Balance Problems       0-6
#   A.11 Sensitivity to Light   0-6
#   A.12 Feeling slowed down    0-6
#   A.13 Feeling like in a fog  0-6
#   A.14 Don't feel right  0-6
#   A.15 Difficulty concentrating       0-6
#   A.16 Difficulty remembering 0-6
#   A.17 Fatigue or low energy  0-6
#   A.18 Confusion      0-6
#   A.19 Drowsiness     0-6
#   A.20 Trouble falling asleep (if applicable) 0-6
#   A.21 More Emotional 0-6
#   A.22 Irritability   0-6
#   A.23 Sadness        0-6
#   A.24 Nervous or Anxious     0-6


# imports
import random
import datetime
import sys
import numpy as np

#--------------------------------------------
# This function computes a score from 0 to 6,
# but biases the score depending on the
# TBI severity.
#--------------------------------------------
def concussion_score(tbi, pcs, dt):

    # Mean recovery time for normal and pcs
    normal_recovery_time = 45 # time in days
    pcs_recovery_time = 270

    # weights for severity
    weight = np.zeros((4,7))
    weight[0] = [0.80, 0.85, 0.90, 0.92, 0.95, 0.98, 1.0] # none
    weight[1] = [0.20, 0.35, 0.55, 0.75, 0.90, 0.95, 1.0] # mild
    weight[2] = [0.10, 0.20, 0.30, 0.50, 0.75, 0.90, 1.0] # moderate
    weight[3] = [0.05, 0.10, 0.25, 0.45, 0.60, 0.80, 1.0] # severe

    # Fractional recovery time. This is a sigmoid function that starts at 1 and
    # decreases to 0 near the recovery time
    if pcs:
        decay = 0.02
        delta = 1.0/(1 + np.exp(0.02*(dt-pcs_recovery_time/2.0)))
    else:
        t_shift = normal_recovery_time/2.0
        decay = 0.2
        delta = 1.0/(1 + decay*np.exp(decay*(dt-normal_recovery_time/2.0)))

    r = delta*random.random()
    score = 0
    while r > weight[tbi][score]:
        score += 1

    #score = (1.0-delta)*score

    return score


#--------------------------------------------
# Here's where most of the work is done.
#--------------------------------------------
def generate_scores(argv):

    argc = len(argv)
    if argc < 2:
        filename = "concussion.csv"
    else:
        filename = argv[1]
    fout = open(filename, 'w')

    # Variable arrays
    Gender = ['m', 'f']
    n_questions = 24

    # How many subjects shall we create data for?
    nSubjects = 10000

    # Some initializations
    id1 = str(123456)
    id2_int = 1

    scores = np.zeros((nSubjects, n_questions))
    total_scores = np.zeros((4))
    n_severity = np.zeros((4))

    # Write the headers
    fout.write(" %17s," %("ID"))
    fout.write(" %17s," %("Date"))
    fout.write(" %17s," %("Injury date"))
    fout.write(" %4s," %("Age"))
    fout.write(" %4s," %("Gender"))
    fout.write(" %4s," %("Race"))
    fout.write(" %s," %("Conditions"))
    fout.write(" %s," %("Meds"))
    fout.write(" %4s," %("TBI"))
    for i in range(n_questions):
        key = "A.%d" %(i+1)
        fout.write("%7s," %(key))
    fout.write("\n")

    for n in range(nSubjects):

        # Concussion severity as determined by initial clinical judgement. 50% are non-concussion controls.
        # Of the remaining 50%, 80% are mild, 10% moderate, 10% severe
        r = random.random()
        if r < 0.5:
            TBI = 0
        else:
            r = random.random()
            if r < 0.8:
                TBI = 1
            elif r < 0.9:
                TBI = 2
            else:
                TBI = 3
        n_severity[TBI] += 1


        # Will this patient suffer from Post Concussion Syndrome? Chances are about 10%
        r = random.random()  # 0 < x < 1.0
        if r < 0.9: pcs = 0
        else: pcs = 1

        # For each subject, generate the data that doesn't change with each visit
        year = 2016

        # Create random id string, then increment by 1
        id2 = str(id2_int).zfill(8)
        ID = id1 + '-' + id2
        id2_int += 1

        # Create a new date
        month = random.randint(1,12)
        if month == 2:
            day = random.randint(1,28)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1,30)
        else:
            day = random.randint(1,31)
        day_injury = datetime.date(year=year,day=day,month=month)

        last_visit = day_injury


        # Now create data for each visit (some time after the last visit)
        if pcs: n_visits = random.randint(21, 31)
        else: n_visits = random.randint(4, 8)

        for visit in range(n_visits):

            # Create a new date: First visit should be within 2 days of the injury
            if visit == 0:
                days = random.randint(0,2)

            # each successive visit should be in 5-8 days up to 42 days (6 weeks), then 13-15 days up to 365 days
            elif visit < 7: # up to 6 weeks
                days = random.randint(5,8)
            else:  # up to about 30 total visits, every two weeks after the first 6 weeks
                days = random.randint(13,15)
            date = last_visit + datetime.timedelta(days)
            last_visit = date

            Age = random.randint(3,18)
            Gender = random.randint(0,1)
            Race = random.randint(0,6)
            Neuro_Conditions = random.randint(0,4)
            Meds = random.randint(0,5)

            fout.write(" %17s," %(ID))
            fout.write(" %17s," %(date))
            fout.write(" %17s," %(day_injury))
            fout.write(" %4s," %(Age))
            fout.write(" %4s," %(Gender))
            fout.write(" %4s," %(Race))
            fout.write(" %s," %(Neuro_Conditions))
            fout.write(" %s," %(Meds))
            fout.write(" %4s," %(TBI))

            for i in range(n_questions):
                # Create a biased integer scores, then print to the file
                dt = (date.toordinal() - day_injury.toordinal())
                value = concussion_score(TBI, pcs, dt)
                scores[n, i] = value
                if visit ==0: total_scores[TBI] += value
                fout.write("%5d, " %(value) )


            fout.write("\n")  # newline


    # Print some information to the screen for fun
    m = total_scores / n_questions
    for i in range(4):
        m[i] /= n_severity[i]
    print "Mean scores by severity. none = %f, mild = %f, mod = %f, severe = %f" %(m[0], m[1], m[2], m[3])

if __name__ == "__main__":
	generate_scores(sys.argv)
