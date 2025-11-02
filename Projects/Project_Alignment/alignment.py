import math


def make_unbanded(table, rows, columns, gap):
    for row in range(rows + 1):
        values = []
        for column in range(columns + 1):
            if row == 0:
                if column == 0:
                    values.append(0)
                else:
                    values.append(values[column - 1] + gap)
            elif column == 0:
                values.append(table[row - 1][0] + gap)
            else:
                values.append(None)
        table.append(values)
    return table


def make_banded(table,size, gap):
    start = (0,0)
    prev = 0
    table[start] = 0
    for i in range(1, size + 1):
        table[(start[0], i)] = prev + gap
        prev += gap
    prev = 0
    for i in range(1, size + 1):
        table[(i, start[1])] = prev + gap
        prev += gap
    return table


def unbanded_fill_table(table, rows, word1, columns, word2, match, sub, gap):
    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            if word1[row - 1] == word2[column - 1]:
                d = table[row - 1][column - 1] + match
            else:
                d = table[row - 1][column - 1] + sub
            u = table[row - 1][column] + gap
            l = table[row][column - 1] + gap
            table[row][column] = min(d, u, l)
    return table


def banded_fill_table(table, word1, word2, match, sub, gap, size):
    inf = math.inf
    len1 = len(word1)
    len2 = len(word2)
    box = (1,1)
    prev_box = (1,1)
    start_col = 1
    while True:
        for i in range(-size, size + 1):
            if prev_box[1] + i < 0 or prev_box[1] + i > len2 or prev_box[1] + i == 0:
                continue
            box = (prev_box[0], prev_box[1] + i)
            is_match = word1[box[0] - 1] == word2[box[1] - 1]
            if is_match:
                d = table.get((box[0] - 1, box[1] - 1)) + match
            else:
                d = table.get((box[0] - 1, box[1] - 1)) + sub
            if (box[0] - 1, box[1]) in table:
                u = table.get((box[0] - 1, box[1])) + gap
            else:
                u = inf
            if (box[0], box[1] - 1) in table:
                l = table.get((box[0], box[1] - 1)) + gap
            else:
                l = inf
            table[box] = min(d,u,l)
        if not prev_box[0] + 1 > len1 and not start_col + 1 > len2:
            box = (prev_box[0] + 1, start_col + 1)
            prev_box = (prev_box[0] + 1, prev_box[1] + 1)
            start_col += 1
        elif not prev_box[0] + 1 > len1:
            box = (prev_box[0] + 1, start_col)
            prev_box = (prev_box[0] + 1, start_col)
        elif not start_col + 1 > len2:
            box = (prev_box[0], start_col + 1)
            prev_box = (prev_box[0], start_col + 1)
            start_col += 1
        else:
            break
    return table


def get_value(table, type, row, column):
    if type == "matrix":
        return table[row][column]
    else:
        return table.get((row, column))


def traceback(table, type, word1, length, word2, width, match, sub, gap, gap_char):
    aligned_1 = ""
    aligned_2 = ""
    has_left = True
    has_up = True
    has_diag = True
    while length > 0 or width > 0:
        if type == "dict":
            has_left = (length, width - 1) in table
            has_up = (length - 1, width) in table
            has_diag = (length - 1, width - 1) in table
        is_matched = word1[length - 1] == word2[width - 1]
        if is_matched:
            cost = match
        else:
            cost = sub
        if length > 0 and width > 0 and has_diag and get_value(table, type, length, width) == get_value(table, type, length - 1, width - 1) + cost:
            aligned_1 = word1[length - 1] + aligned_1
            aligned_2 = word2[width - 1] + aligned_2
            length = length - 1
            width = width - 1
        elif width > 0 and has_left and get_value(table, type, length, width) == get_value(table, type, length, width - 1) + gap:
            aligned_1 = gap_char + aligned_1
            aligned_2 = word2[width - 1] + aligned_2
            width = width - 1
        elif has_up:
            aligned_1 = word1[length - 1] + aligned_1
            aligned_2 = gap_char + aligned_2
            length = length - 1
    return aligned_1, aligned_2


def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap_open_penalty=0,
        gap='-',
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap_open_penalty: how much it costs to open a gap. If 0, there is no gap_open penalty
        :param gap: the character to use to represent gaps in the alignment strings
    """

    s1 = len(seq1)
    s2 = len(seq2)
    if s1 == 0 or s2 == 0:
        if s1 == 0:
            return indel_penalty * s2, gap * s2, seq2
        else:
            return indel_penalty * s1, seq1, gap * s1
    if banded_width == -1:
        type = "matrix"
        table = make_unbanded([], s1, s2, indel_penalty)
        filled_table = unbanded_fill_table(table, s1, seq1, s2, seq2, match_award, sub_penalty, indel_penalty)
    else:
        if abs(s1-s2) > 5:
            return math.inf, None, None
        type = "dict"
        table = make_banded({}, banded_width, indel_penalty)
        filled_table = banded_fill_table(table, seq1, seq2, match_award, sub_penalty, indel_penalty, banded_width)
    cost = get_value(filled_table, type, s1, s2)
    word1, word2 = traceback(filled_table, type, seq1, s1, seq2, s2, match_award, sub_penalty, indel_penalty, gap)
    return cost, word1, word2