
def get_local_stretch_alignment(p1, p2):
    score = 0
    
    #Parameters
    match = 1
    mismatch = 0
    gap_penalty = -1
    
    #Initialisation
    matrix = [[0 for i in range(len(p2) + 1)] for j in range(len(p1) + 1)] #x -> p1, y -> p2
    for i in range(len(p1) + 1):
        matrix[i][0] = i * gap_penalty
    for i in range(len(p2) + 1):
        matrix[0][i] = i * gap_penalty
        
    #Fill
    for i in range(len(p1)):
        for j in range(len(p2)):
            p1_diagnosis = p1[i][0]
            p2_diagnosis = p2[j][0]
            left = matrix[i][j+1] + gap_penalty
            right = matrix[i+1][j] + gap_penalty
            diagonal = matrix[i][j] + (match if p1_diagnosis == p2_diagnosis else mismatch)
            matrix[i+1][j+1] = max(left, right, diagonal, 0)

    while True:
        current_alignment_score = 0
        #Find the biggest alignment value
        MAX = None
        MAX_co = None
        for (index, row) in enumerate(matrix):
            row_max = max(row)
            if MAX == None or row_max > MAX:
                MAX = row_max
                MAX_co = (row.index(MAX), index) #(x, y)

        #Traceback
        END = MAX
        END_co = MAX_co
        if MAX <= 0: #if all values are added
            break
        while END_co[0] != 0 and END_co[1] != 0:
            #Be aware, when calling out matrix, we need to declare row first therefore we get y from coordinates first
            if matrix[END_co[1]-1][END_co[0]-1] + match == END: #diagonal (match)
                #if we reach 0, we keep the last END_co or MAX_co by default
                #NB! this can olny hapen with a match
                #further more, there must be at least one 0 remaining -> matrix[0][0]
                if matrix[END_co[1]-1][END_co[0]-1] == 0:
                    break
                END = matrix[END_co[1]-1][END_co[0]-1]
                END_co = (END_co[0]-1, END_co[1]-1) #(x, y)
                current_alignment_score += 1
            elif matrix[END_co[1]-1][END_co[0]-1] + mismatch == END: #diagonal (mismatch)
                END = matrix[END_co[1]-1][END_co[0]-1]
                END_co = (END_co[0]-1, END_co[1]-1) #(x, y)
            elif matrix[END_co[1]-1][END_co[0]] + gap_penalty == END: #top
                END = matrix[END_co[1]-1][END_co[0]]
                END_co = (END_co[0], END_co[1]-1) #(x, y)
            elif matrix[END_co[1]][END_co[0]-1] + gap_penalty == END: #left
                END = matrix[END_co[1]][END_co[0]-1]
                END_co = (END_co[0]-1, END_co[1]) #(x, y)
            else:
                matrix[END_co[1]][END_co[0]] = 0
                matrix[END_co[1]-1][END_co[0]-1] = 0
                matrix[END_co[1]-1][END_co[0]] = 0
                matrix[END_co[1]][END_co[0]-1] = 0
                break

        #replace all used letter celles with 0-s
        y_del = MAX_co[1] - END_co[1] + 1
        x_del = MAX_co[0] - END_co[0] + 1
        for i in range(y_del):
            for j in range(x_del):
                matrix[MAX_co[1]-i][MAX_co[0]-j] = 0
        #increase score and reset values
        score += current_alignment_score

    return score