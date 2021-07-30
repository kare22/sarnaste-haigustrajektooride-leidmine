from local_alignment import get_local_alignment
import operator
import itertools
from tqdm import tqdm

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

def create_motive(counts, threshold=0, max_length=999):
    motive = []
    for count in counts:
        if counts[count] >= threshold:
            motive.append(count)
        if len(motive) >= max_length:
            break

    return motive

def find_most_similar_sequence_to_the_motive(motive, persons, n):
    results = {}
    p_motive = [tuple([diagnose]) for diagnose in motive]
    for p in tqdm(persons):
        results[p] = get_local_alignment(persons[p], p_motive)
    return dict(sorted(results.items(), key=operator.itemgetter(1), reverse=True)[:n])


def get_model_alignment(sections, threshold, max_length, n=100, name='get_model_alignment'):
    print('Started working on: %s' % (name))
    counts = get_counts(sections)
    best_matches = find_most_similar_sequence_to_the_motive(create_motive(counts, threshold, max_length), sections, 16)
    best_match_pairs = list(itertools.combinations([match for match in best_matches], 2))[:n]
    return best_match_pairs