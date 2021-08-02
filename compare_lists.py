from scipy.stats import spearmanr

list1 = [('1', '88'),
 ('1', '93'),
 ('24', '113'),
 ('24', '160'),
 ('88', '93'),
 ('113', '160'),
 ('1', '24'),
 ('1', '36'),
         ('24', '1260'),
         ('88', '923'),
         ('113', '1620'),
         ('1', '224'),
         ('1', '336'),
 ('1', '46'),
 ('1', '58')]

list2 = [('1', '88'),
 ('13', '4389343498438948993'),
 ('24', '1143'),
 ('24', '1630'),
 ('88', '93233'),
 ('113', '16033223'),
 ('1', '242332'),
 ('15', '36454'),
 ('11', '445546'),
         ('113', '160323223'),
         ('1', '2422332'),
         ('15', '364254'),
         ('11', '4455346'),
         ('11', '445534633'),
 ('11', '585454')]


## To ensure that the data is in the same format we order the pairs
## so that smallest value is always first and all indexes are int
def clean_list(list):
    cleaned_list = []

    for pair in list:
        #Integers for comparison
        p1 = int(pair[0])
        p2 = int(pair[1])
        #Strings so that Spearman would consider each pair as a single element
        cleaned_list.append(str(p1) + str(p2) if p1 < p2 else str(p2) + str(p1))

    return cleaned_list


def compare_lists_distance(l1, l2):
    score = 0
    mismatch = len(l1)
    l1 = clean_list(l1)
    l2 = clean_list(l2)
    for (l1_index, el) in enumerate(l1):
        try:
            l2_index = l2.index(el)
            score += abs(l1_index - l2_index)
        except: #If match not found
            score += mismatch

    return score

def count_lists_similarities(l1, l2):
    count = 0
    l1 = clean_list(l1)
    l2 = clean_list(l2)
    for (l1_index, el) in enumerate(l1):
        try:
            l2_index = l2.index(el)
            if l1_index == l2_index:
                count += 1
        except:
            pass

    return count

def get_spearmanr_coeficent(l1, l2):
    l1 = clean_list(l1)
    l2 = clean_list(l2)
    return spearmanr(l1, l2)[0]

print(get_spearmanr_coeficent(list1, list2))
