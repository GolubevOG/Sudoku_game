import random
import utils

def generate_primary_field():
    decset = [i for i in range(1,10)]
    random.shuffle(decset)
    pole_rows = []

    for _ in range(9):
        pst = []
        for __ in range(9):
            if _ <= 2:
                value = (_ * 3 + __ + 1) % 9
            elif 3 <= _ <= 5:
                value = (_ * 3 + __ + 2) % 9
            else:
                value = (_ * 3 + __ + 3) % 9
            if value == 0:
                value = 9
            pst.append(decset[value-1])
        pole_rows.append(pst)

    return pole_rows


def generate_field():
    pole_rows = generate_primary_field()
    # shuffling rows
    row_block0 = pole_rows[:3]
    random.shuffle(row_block0)
    row_block1 = pole_rows[3:6]
    random.shuffle(row_block1)
    row_block2 = pole_rows[6:]
    random.shuffle(row_block2)
    row_blocks = [row_block0, row_block1, row_block2]
    random.shuffle(row_blocks)
    # setting new rows and columns
    new_pole_rows = []
    new_pole_cols = []
    for row_block in row_blocks:
        new_pole_rows.extend(row_block)
    pole_rows = new_pole_rows
    pole_cols = utils.adjust_cols_from_rows(pole_rows)
    # shuffling columns
    col_block0 = pole_cols[:3]
    random.shuffle(col_block0)
    col_block1 = pole_cols[3:6]
    random.shuffle(col_block1)
    col_block2 = pole_cols[6:]
    random.shuffle(col_block2)
    col_blocks = [col_block0, col_block1, col_block2]
    random.shuffle(col_blocks)
    # setting new rows and columns
    for col_block in col_blocks:
        new_pole_cols.extend(col_block)
    pole_cols = new_pole_cols
    pole_rows = utils.adjust_rows_from_cols(pole_cols)

    return pole_rows

def set_difficulty(field_rows:list, difficulty:int):
    for row in range(9):
        indexes = [i for i in range(9)]
        random.shuffle(indexes)
        if difficulty == 1:
            indexes_to_erase = indexes[:3]
        elif difficulty == 2:
            indexes_to_erase = indexes[:5]
        elif difficulty == 3:
            if row % 2 == 0:
                indexes_to_erase = indexes[:7]
            else:
                indexes_to_erase = indexes[:6]
        for i in indexes_to_erase:
            field_rows[row][i] = '0'

    return field_rows

def main():
    field_rows = generate_field()
    utils.write_to_txt(field_rows, 'sudokunotsee.txt')
    see = set_difficulty(field_rows, 1)
    utils.write_to_txt(see, 'sudokusee.txt')

if __name__ == '__main__':
    main()