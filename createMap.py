
def create(user_input):
    f = open(user_input)
    contents = f.readlines()
    f.close()
    Map = []
    
    for num in range(len(contents)):
        row = contents[num].split(',')
        for i in range(len(row)):
            if row[i].find('\n') != -1:
                chars=str(row[i])
                row[i] = chars[:-1]
        Map.append(row)
    return Map

def locate(Object,user_input):
    Object = Object
    position = create(user_input)
    for num in range(len(position)):
        for i in range(len(position[num])):
            if str(position[num][i]) == Object:
                return [num,i]