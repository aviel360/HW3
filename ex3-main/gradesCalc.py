#### PART 1 ####
# final_grade: Calculates the final grade for each student, and writes the output (while eliminating illegal
# rows from the input file) into the file in `output_path`. Returns the average of the grades.
#   input_path: Path to the file that contains the input
#   output_path: Path to the file that will contain the output
def valid (line: str) -> bool:
    chunks = line.split(',')
    if len(chunks[0]) != 8 or int(chunks[0][0]) == 0:
        return False
    if not "".join(chunks[1]).isalpha():
        return False
    if int(chunks[2]) < 1:
        return False
    if int(chunks[3]) < 51 or int(chunks[3]) > 100:
        return False
    return True
        
def makeLine(line, map):
    chunks = line.split(',')
    id = chunks[0]
    homework_avg = int(chunks[3])
    final_grade = (int(id[6])*10 + int(id[7]) + homework_avg)/2
    map[id] = id + ', ' + str(homework_avg) + ', ' + str(int(final_grade))

def final_grade(input_path: str, output_path: str) -> int:
    input_file = open(input_path, "r")
    output_file = open(output_path, "w")
    map = {}
    for line in input_file:
        line = "".join(line.split())
        if valid(line):
            makeLine(line, map)
    
    sorted_list = sorted(map.items())
    total_sum = 0
    students_counter = 0
    for key, line in sorted_list:
        output_file.write(line + "\n")
        total_sum += int(line.split(',')[2])
        students_counter += 1
    if students_counter == 0:
        return 0
    return total_sum//students_counter
        

    
        


    


#### PART 2 ####
# check_strings: Checks if `s1` can be constructed from `s2`'s characters.
#   s1: The string that we want to check if it can be constructed
#   s2: The string that we want to construct s1 from
def check_strings(s1: str, s2: str) -> bool:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', \
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    src = s1.lower()
    dst = s2.lower()
    for letter in letters:
        if src.count(letter) > dst.count(letter):
            return False
    return True

