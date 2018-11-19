from Objects import grid
from Objects import mosquito as m


object = grid.Grid(5, 5)
mosquito = m.Mosquito((0, 4))
object.gridM[mosquito.location[0]][mosquito.location[1]] = mosquito

# Hoe je dingen uit object leert.
for i in range(len(object.gridM)):
    for j in range(len(object.gridM[i])):
        if type(object.gridM[i][j]) is not int:
            print(object.gridM[i][j])
            print(object.gridM[i][j].hungry)
