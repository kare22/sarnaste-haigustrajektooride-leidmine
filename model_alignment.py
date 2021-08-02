from local_alignment import get_local_alignment
import operator
import itertools

def get_counts(persons):
    counts = {}
    if len(persons.keys()):
        for p in persons:
            for diagnose in persons[p]:
                try:
                    counts[diagnose[0]] += 1
                except:
                    counts[diagnose[0]] = 1
    return counts

def create_motive(counts, min, max, max_length=999):
    motive = []
    for count in counts:
        if counts[count] >= min and counts[count] <= max:
            motive.append(count)
        if len(motive) >= max_length:
            break

    return motive

def get_cleaned_by_motive_diagnoses(sections, motive):
    persons = sections.copy()
    for p in persons:
        trajectory = []
        for diagnose in persons[p]:
            if diagnose[0] in motive:
                trajectory.append(diagnose)
        persons[p] = trajectory

        return persons

def find_most_similar_sequence_to_the_motive(motive, persons):
    results = {}
    p_motive = [tuple([diagnose]) for diagnose in motive]
    for p in persons:
        results[p] = get_local_alignment(persons[p], p_motive)
    return dict(sorted(results.items(), key=operator.itemgetter(1), reverse=True))


def get_model_alignment(sections, motive_limit = (0, 999), max_motive_length = 100, match_limit = (0, 100), order_reverse=False, name='get_model_alignment'):
    print('Started working on: %s' % (name))
    counts = get_counts(sections)
    motive = create_motive(counts, motive_limit[0], motive_limit[1], max_motive_length)

    # sections = get_cleaned_by_motive_diagnoses(sections, motive)
    # counts = get_counts(sections)
    # motive = create_motive(counts, motive_limit[0], motive_limit[1], max_motive_length)

    matches = find_most_similar_sequence_to_the_motive(motive, sections)
    best_matches = []
    for match in matches:
        if matches[match] >= match_limit[0] and matches[match] <= match_limit[1]:
            best_matches.append(match)
    if order_reverse:
        best_matches = best_matches[::-1]
    best_match_pairs = list(itertools.combinations(best_matches, 2))
    return best_match_pairs