import filepaths
import grid


object = grid.Grid(5, 5, 13, 20, 0.5)
for i in object.gridM:
    for j in i:
        if type(j) is not int:
            print(j.infected)

# VOORBEELD
# mosquito = m.Mosquito()
# object.gridM[0][4] = mosquito
#
# # Hoe je dingen uit object leert.
# for i in range(len(object.gridM)):
#     for j in range(len(object.gridM[i])):
#         if type(object.gridM[i][j]) is not int:
#             print(object.gridM[i][j])
#             print(object.gridM[i][j].hungry)
