def input_to_int_list(the_input, separator):
    if separator:
        return [int(i) for i in the_input.split(separator)]
    else:
        return [int(i) for i in the_input]
