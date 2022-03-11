#Adam Albawab | CSE 4308-002 | March 8, 2022
import sys
from queue import PriorityQueue

#Parse the input file to create the nested dictionary structure used in the uninformed search
def uninformedParsing(cFilename):
  city_dict={}
  try:
    with open(cFilename) as city_file:
      cLines = [line.rstrip() for line in city_file]
      for line in cLines:
        if "END OF INPUT" in line:
          break
        elements = line.split(" ")
        for element in elements:
          element = element.replace("_", " ")
          if elements[0] in city_dict:
            city_dict[elements[0]][elements[1]] = float(elements[2])
          else:
            city_dict[elements[0]] = {elements[1]: float(elements[2])}
          if elements[1] in city_dict:
            city_dict[elements[1]][elements[0]] = float(elements[2])
          else:
            city_dict[elements[1]] = {elements[0]: float(elements[2])}
  except IOError:
    sys.exit("\nError opening city input file.\nCheck file name.\n")
  return city_dict

#Parse the input file to create the nested dictionary structure that represents the cities and the heuristic dictionary used in the informed search
def informedParsing(cFilename,hFilename):
  city_dict=uninformedParsing(cFilename)
  heuristic_dict={}
  try:
    with open(hFilename) as heuristic_file:
      hLines = [line.rstrip() for line in heuristic_file]
      for line in hLines:
        if "END OF INPUT" in line:
          break
        elements = line.split(" ")
        for element in elements:
          element = element.replace("_", " ")
        heuristic_dict[elements[0]] = float(elements[1])
  except IOError:
    sys.exit("\nError opening heuristic input file.\nCheck file name.\n")
  return  city_dict, heuristic_dict

#Uniform cost search algorithm
def UCS(city_graph, origin, destination):
  fringe = PriorityQueue()
  fringe.put((0, origin))
  visited = {}
  visited[origin] = ("", 0)
  closed = []
  generatedCount = 1
  poppedCount = 0
  maxDepth = 0
  distance = "infinity"
  routeTaken = []
  junk = ""
  while not fringe.empty():
    if len(fringe.queue) > maxDepth:
      maxDepth=len(fringe.queue)
    junk, currentNode = fringe.get()
    poppedCount = poppedCount + 1
    if currentNode == destination:
      break
    elif currentNode in closed:
      continue
    closed.append(currentNode)
    for i in city_graph[currentNode]:
      generatedCount = generatedCount + 1
      fringe.put((city_graph[currentNode][i]+visited[currentNode][1],i))
      if i not in visited:
        cumulative = city_graph[currentNode][i] + visited[currentNode][1]
        visited[i] = (currentNode, cumulative) 
  if destination in visited:
    currentNode = destination
    distance = 0
    while currentNode != origin:
      distance = distance + city_graph[visited[currentNode][0]][currentNode]
      routeTaken.append(currentNode)
      currentNode = visited[currentNode][0]
  return poppedCount, generatedCount, distance, routeTaken

    
#A* search algorithm. Very similar to the UCS algorithm above with two changes made. Which are checking before adding to the fringe and factoring in the heuristic value
def aStar(city_graph, origin, destination, heuristic):
  fringe = PriorityQueue()
  fringe.put((0, origin))
  visited = {}
  visited[origin] = ("", 0)
  closed = []
  generatedCount = 1
  poppedCount = 0
  maxDepth = 0
  distance = "infinity"
  routeTaken = []
  junk = ""
  while not fringe.empty():
    if len(fringe.queue) > maxDepth:
      maxDepth=len(fringe.queue)
    junk, currentNode = fringe.get()
    poppedCount = poppedCount + 1
    if currentNode == destination:
      break
    elif currentNode in closed:
      continue
    closed.append(currentNode)
    for i in city_graph[currentNode]:
      generatedCount = generatedCount + 1
      if i not in visited:
        cumulative = city_graph[currentNode][i] + visited[currentNode][1]
        visited[i] = (currentNode, cumulative)
        fringe.put((city_graph[currentNode][i]+visited[currentNode][1]+heuristic[i],i)) 
  if destination in visited:
    currentNode = destination
    distance = 0
    while currentNode != origin:
      distance = distance + city_graph[visited[currentNode][0]][currentNode]
      routeTaken.append(currentNode)
      currentNode = visited[currentNode][0]
  return poppedCount, generatedCount, distance, routeTaken

#Simple function to format and print the results of the search
def displayInfo(poppedCount, generatedCount, distance, routeTaken, origin):
  print("\nNodes expanded: {}".format(poppedCount))
  print("Nodes generated: {}".format(generatedCount))
  print("Distance: {} km".format(distance))
  print("\nRoute:")
  currentNode = origin
  if len(routeTaken) == 0:
      print("No route found")
  else:
    for city in reversed(routeTaken):
      print("{} to {}, {} km".format(currentNode, city, city_graph[currentNode][city]))
      currentNode=city

#Conditionals to facilitate which search is done based upon number of command line arguments.
if len(sys.argv) == 4 or len(sys.argv) == 5: 
  input_filename = sys.argv[1]
  origin_city = sys.argv[2]
  destination_city = sys.argv[3]

  if len(sys.argv)==4:  
    city_graph = uninformedParsing(input_filename)
    poppedCount, generatedCount, distance, routeTaken = UCS(city_graph, origin_city, destination_city)
    displayInfo(poppedCount, generatedCount, distance, routeTaken,origin_city)
  
  elif len(sys.argv)==5:  
    heuristic_file = sys.argv[4]
    city_graph, heuristic = informedParsing(input_filename, heuristic_file)
    poppedCount, generatedCount, distance, routeTaken = aStar(city_graph, origin_city, destination_city, heuristic)  
    displayInfo(poppedCount, generatedCount, distance, routeTaken,origin_city)

else:
  print("Wrong number of arguments provided. Please try again!")  

