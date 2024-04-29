import json
import matplotlib.pyplot as plt
import numpy as np
import time
from insidepolygon import pointInPoly

#starting time
start = time.time()

polygon = [
    [196, 14],
    [196, 48],
    [175, 44],
    [175, 18],
    [196, 14]
]

#create circles inside of polygon using greedy algorithm
def addCircles(num, polyg, grain = 5):
   #setting main parameters for continued reference
   minx = min(x[0] for x in polyg)
   maxx = max(x[0] for x in polyg)
   width = maxx-minx
   miny = min(x[1] for x in polyg)
   maxy = max(x[1] for x in polyg)
   height = maxy-miny

   #initializing array representing descritized points that are inside and outside the polygon
   #additionally used to indicate points already covered by circles during future iterations
   covered = np.zeros((int(width/grain),int(height/grain)))
   
   #coordinates of descritized points
   coords = [[],[]]

   #array of points outside the circle, used for plot representation of results
   outsidec = [[],[]]

   #iterating through points to record status of point (inside vs. outside)
   for i in range(len(covered)):
      for j in range(len(covered[0])):
         
         #using pointInPoly from insidepolygon.py, adjusting i and j to correspond to real coordinate
         if not pointInPoly([(i+1)*grain + minx, (j+1)*grain + miny],polyg):
            
            #-1 in covered represents a point outside of the polygon
            covered[i,j] = -1
            
            #appending actual coordinates to the outside array
            outsidec[0].append((i+1)*grain + minx)
            outsidec[1].append((j+1)*grain + miny)
         
         #appending all coordinates to coords array, primarily for plotting purposes
         coords[0].append((i+1)*grain + minx)
         coords[1].append((j+1)*grain + miny)
   
   #plot points that are inside and outside the polygon
   plt.scatter(coords[0], coords[1], marker=".")
   plt.scatter(outsidec[0], outsidec[1], color="red", marker=".")
   
   #number of circles placed
   count = 0
   
   #iterate until number of circles placed = parameter representing desired number of circles
   while count < num:
      #define size of X and Y for future reference
      X = len(covered)
      Y = len(covered[0])

      #define working optimal radius and its center for future comparison and eventual plot
      top_radius = 0
      top_center = [-1, -1]

      #number of new points included by top circle so far
      max_points = 0

      #k,l represent a new center for the circle
      #each point in the descritized array can serve as a center
      #future optimization: start scanning at the center and spiral outwards
      for k in range(1, X):
         for l in range(1, Y):
            
            #if the point is outside the polygon, go next
            if covered[k][l] == -1:
               continue
            new_center = [k,l]

            #max radius if all points happen to be inside
            #setting bounds for iteration
            max_radius = min(k, l, X-k, Y-l)
            
            #if even the max radius has no chance to beat high score, continue
            if(max_radius < np.sqrt(max_points/4)): #4 for wiggle room
               continue

            #found a circle that works
            found_circ = False
            
            #reseting local vars
            curr_rad = 0
            curr_covered = 0
            points_covered = 0

            #scan using expanding radius
            for r in range(max_radius):

               #circle doesnt include any points outside polygon
               works = True
               points_covered = 0
               for m in range(k-r-1, k+r+1):
                  for n in range(l-r-1,l+r+1):
                     if ((np.sqrt((m - k)**2 + (n - l)**2)) <= r):
                        if(covered[m][n] == -1):
                          
                           #if a smaller radius has a point outside the polygon
                           #all larger radiuses will also fail, so break
                           works = False
                           break
                        elif(covered[m][n] == 0):
                             
                              #if point not already covered, increment
                              points_covered += 1
               
               #accept if more points are covered
               if(works and points_covered > curr_covered):
                  found_circ = True
                  curr_rad = r
                  curr_covered = points_covered

               #if a smaller radius has a point outside the polygon
               #all larger radiuses will also fail, so break
               if(not works):
                  break

               #redundancy
               if found_circ and curr_covered > max_points:
                  top_radius = curr_rad
                  top_center = new_center
                  max_points = curr_covered
      
      #update what points are covered
      for m in range(top_center[0]-top_radius - 1, top_center[0]+top_radius + 1):
         for n in range(top_center[1]-top_radius - 1, top_center[1]+top_radius + 1):
            if ((np.sqrt((m - top_center[0])**2 + (n - top_center[1])**2)) < top_radius):
               covered[m][n] = 1
      
      #plot current circle
      circle = plt.Circle(((top_center[0] + 1)*grain + minx, (top_center[1] + 1)*grain + miny), top_radius*grain, color='g', fc="None", linewidth=2)
      fig = plt.gcf()
      ax = fig.gca()
      ax.add_patch(circle)
      


      #uncomment to plot some stats about progress
      count += 1
      # cov_county = 0
      # out_range = 0
      # print(covered.size)
      # if(count == num):
      #    for i in range(X):
      #       for j in range(Y):
      #          if(covered[i][j] == 1):
      #             cov_county += 1
      #          elif(covered[i][j] == -1):
      #             out_range += 1
      # print("COVERED COUNT")
      # print(cov_county)
      # print(out_range)

      # print("ROUND TWO")
      # print(count)

#GeoJSON
js = '''{
    "type":"Feature",
    "geometry":{
       "type":"Polygon",
       "coordinates":[
          [
             [
                -79.264152,
                35.930242
             ],
             [
                -79.262608,
                35.928868
             ],
             [
                -79.258311,
                35.928566
             ],
             [
                -79.258255,
                35.928919
             ],
             [
                -79.261733,
                35.930094
             ],
             [
                -79.259807,
                35.931502
             ],
             [
                -79.259722,
                35.932627
             ],
             [
                -79.258612,
                35.933468
             ],
             [
                -79.25491,
                35.930737
             ],
             [
                -79.254482,
                35.931576
             ],
             [
                -79.252241,
                35.932713
             ],
             [
                -79.2506,
                35.932765
             ],
             [
                -79.246366,
                35.934408
             ],
             [
                -79.245598,
                35.938056
             ],
             [
                -79.247033,
                35.941435
             ],
             [
                -79.245379,
                35.94332
             ],
             [
                -79.244563,
                35.945634
             ],
             [
                -79.24332,
                35.946958
             ],
             [
                -79.243544,
                35.94786
             ],
             [
                -79.24147,
                35.948619
             ],
             [
                -79.24166,
                35.950162
             ],
             [
                -79.239714,
                35.951513
             ],
             [
                -79.23951,
                35.952932
             ],
             [
                -79.236135,
                35.954741
             ],
             [
                -79.23492,
                35.95614
             ],
             [
                -79.233431,
                35.959027
             ],
             [
                -79.231715,
                35.959572
             ],
             [
                -79.229829,
                35.959079
             ],
             [
                -79.229325,
                35.957548
             ],
             [
                -79.226168,
                35.95832
             ],
             [
                -79.224768,
                35.959359
             ],
             [
                -79.22612,
                35.961135
             ],
             [
                -79.226512,
                35.96224
             ],
             [
                -79.224575,
                35.96328
             ],
             [
                -79.217569,
                35.963181
             ],
             [
                -79.215136,
                35.964755
             ],
             [
                -79.210947,
                35.966459
             ],
             [
                -79.210394,
                35.967271
             ],
             [
                -79.212726,
                35.968709
             ],
             [
                -79.212538,
                35.970174
             ],
             [
                -79.20952,
                35.972139
             ],
             [
                -79.209248,
                35.973943
             ],
             [
                -79.205148,
                35.973563
             ],
             [
                -79.206053,
                35.970052
             ],
             [
                -79.204383,
                35.970178
             ],
             [
                -79.203491,
                35.96908
             ],
             [
                -79.199206,
                35.970091
             ],
             [
                -79.197617,
                35.970025
             ],
             [
                -79.195867,
                35.972124
             ],
             [
                -79.194035,
                35.971867
             ],
             [
                -79.194226,
                35.967911
             ],
             [
                -79.188136,
                35.967639
             ],
             [
                -79.176624,
                35.955611
             ],
             [
                -79.170719,
                35.955763
             ],
             [
                -79.168142,
                35.96331
             ],
             [
                -79.166763,
                35.965513
             ],
             [
                -79.166157,
                35.967542
             ],
             [
                -79.164289,
                35.969938
             ],
             [
                -79.163197,
                35.97213
             ],
             [
                -79.160064,
                35.971766
             ],
             [
                -79.15837,
                35.972104
             ],
             [
                -79.154518,
                35.973859
             ],
             [
                -79.149536,
                35.97554
             ],
             [
                -79.144925,
                35.977735
             ],
             [
                -79.14115,
                35.977268
             ],
             [
                -79.141487,
                35.972259
             ],
             [
                -79.139438,
                35.972429
             ],
             [
                -79.137977,
                35.972942
             ],
             [
                -79.138415,
                35.975282
             ],
             [
                -79.139517,
                35.976731
             ],
             [
                -79.137258,
                35.97943
             ],
             [
                -79.134735,
                35.978542
             ],
             [
                -79.132876,
                35.981705
             ],
             [
                -79.127855,
                35.980491
             ],
             [
                -79.122911,
                35.979634
             ],
             [
                -79.122821,
                35.983019
             ],
             [
                -79.123981,
                35.988296
             ],
             [
                -79.124928,
                35.989453
             ],
             [
                -79.124145,
                35.991697
             ],
             [
                -79.121226,
                35.994484
             ],
             [
                -79.118887,
                35.995089
             ],
             [
                -79.118563,
                35.996199
             ],
             [
                -79.114717,
                35.997733
             ],
             [
                -79.115024,
                35.999776
             ],
             [
                -79.107423,
                35.999796
             ],
             [
                -79.106979,
                36.004751
             ],
             [
                -79.104252,
                36.003684
             ],
             [
                -79.101793,
                36.00548
             ],
             [
                -79.097285,
                36.006078
             ],
             [
                -79.094338,
                36.006056
             ],
             [
                -79.093045,
                36.00359
             ],
             [
                -79.088514,
                36.006756
             ],
             [
                -79.080976,
                36.011633
             ],
             [
                -79.077751,
                36.014677
             ],
             [
                -79.075555,
                36.017264
             ],
             [
                -79.072046,
                36.014143
             ],
             [
                -79.066057,
                36.006409
             ],
             [
                -79.066434,
                36.002103
             ],
             [
                -79.067148,
                36.001141
             ],
             [
                -79.071773,
                35.997673
             ],
             [
                -79.072533,
                35.995087
             ],
             [
                -79.075476,
                35.995369
             ],
             [
                -79.075439,
                35.989865
             ],
             [
                -79.075017,
                35.98702
             ],
             [
                -79.073082,
                35.990389
             ],
             [
                -79.072891,
                35.982239
             ],
             [
                -79.06887,
                35.975678
             ],
             [
                -79.067746,
                35.974428
             ],
             [
                -79.066636,
                35.973496
             ],
             [
                -79.064896,
                35.972427
             ],
             [
                -79.062784,
                35.97145
             ],
             [
                -79.062606,
                35.971098
             ],
             [
                -79.061759,
                35.969734
             ],
             [
                -79.060969,
                35.968761
             ],
             [
                -79.059752,
                35.966975
             ],
             [
                -79.057925,
                35.963005
             ],
             [
                -79.057284,
                35.959657
             ],
             [
                -79.058914,
                35.959742
             ],
             [
                -79.05893,
                35.958657
             ],
             [
                -79.057336,
                35.958654
             ],
             [
                -79.057765,
                35.956714
             ],
             [
                -79.057627,
                35.952386
             ],
             [
                -79.058538,
                35.947297
             ],
             [
                -79.055427,
                35.931666
             ],
             [
                -79.055429,
                35.929637
             ],
             [
                -79.056888,
                35.929074
             ],
             [
                -79.053867,
                35.926649
             ],
             [
                -79.054222,
                35.924714
             ],
             [
                -79.055866,
                35.921148
             ],
             [
                -79.056965,
                35.91519
             ],
             [
                -79.053125,
                35.908671
             ],
             [
                -79.054623,
                35.908177
             ],
             [
                -79.055147,
                35.90409
             ],
             [
                -79.057973,
                35.900807
             ],
             [
                -79.05759,
                35.898006
             ],
             [
                -79.058526,
                35.895986
             ],
             [
                -79.057439,
                35.893511
             ],
             [
                -79.057589,
                35.892885
             ],
             [
                -79.061234,
                35.88999
             ],
             [
                -79.06165,
                35.887567
             ],
             [
                -79.061414,
                35.885627
             ],
             [
                -79.061232,
                35.885075
             ],
             [
                -79.060701,
                35.883699
             ],
             [
                -79.061148,
                35.882384
             ],
             [
                -79.064685,
                35.878004
             ],
             [
                -79.066593,
                35.873321
             ],
             [
                -79.067063,
                35.872612
             ],
             [
                -79.068621,
                35.871175
             ],
             [
                -79.073581,
                35.867771
             ],
             [
                -79.077107,
                35.86366
             ],
             [
                -79.080425,
                35.862148
             ],
             [
                -79.081938,
                35.86078
             ],
             [
                -79.084786,
                35.856279
             ],
             [
                -79.085989,
                35.851867
             ],
             [
                -79.086377,
                35.851387
             ],
             [
                -79.086839,
                35.850898
             ],
             [
                -79.08719,
                35.850578
             ],
             [
                -79.090155,
                35.848124
             ],
             [
                -79.090857,
                35.846416
             ],
             [
                -79.089512,
                35.833473
             ],
             [
                -79.087849,
                35.829259
             ],
             [
                -79.087417,
                35.82465
             ],
             [
                -79.084693,
                35.817881
             ],
             [
                -79.084512,
                35.816067
             ],
             [
                -79.086059,
                35.81306
             ],
             [
                -79.08862,
                35.811633
             ],
             [
                -79.090924,
                35.814562
             ],
             [
                -79.093736,
                35.817011
             ],
             [
                -79.097067,
                35.818231
             ],
             [
                -79.097676,
                35.819873
             ],
             [
                -79.097153,
                35.821025
             ],
             [
                -79.098526,
                35.823013
             ],
             [
                -79.101343,
                35.824069
             ],
             [
                -79.099928,
                35.826864
             ],
             [
                -79.100543,
                35.827785
             ],
             [
                -79.102913,
                35.824267
             ],
             [
                -79.104173,
                35.819671
             ],
             [
                -79.102061,
                35.819507
             ],
             [
                -79.101816,
                35.814888
             ],
             [
                -79.103974,
                35.812749
             ],
             [
                -79.104593,
                35.811339
             ],
             [
                -79.110791,
                35.813427
             ],
             [
                -79.113973,
                35.815386
             ],
             [
                -79.115858,
                35.815977
             ],
             [
                -79.121984,
                35.81577
             ],
             [
                -79.127344,
                35.817134
             ],
             [
                -79.132939,
                35.816913
             ],
             [
                -79.13787,
                35.817036
             ],
             [
                -79.137813,
                35.820475
             ],
             [
                -79.139432,
                35.822348
             ],
             [
                -79.143504,
                35.825857
             ],
             [
                -79.144338,
                35.826
             ],
             [
                -79.143544,
                35.828095
             ],
             [
                -79.140861,
                35.832058
             ],
             [
                -79.137509,
                35.834959
             ],
             [
                -79.134284,
                35.83975
             ],
             [
                -79.13002,
                35.84214
             ],
             [
                -79.125028,
                35.844056
             ],
             [
                -79.126392,
                35.84637
             ],
             [
                -79.125074,
                35.849903
             ],
             [
                -79.129592,
                35.850559
             ],
             [
                -79.14129,
                35.850563
             ],
             [
                -79.150796,
                35.851453
             ],
             [
                -79.150401,
                35.855353
             ],
             [
                -79.146642,
                35.854318
             ],
             [
                -79.140723,
                35.854226
             ],
             [
                -79.13907,
                35.853598
             ],
             [
                -79.135371,
                35.854208
             ],
             [
                -79.124561,
                35.852865
             ],
             [
                -79.123321,
                35.857009
             ],
             [
                -79.123057,
                35.861263
             ],
             [
                -79.121541,
                35.863986
             ],
             [
                -79.131858,
                35.864854
             ],
             [
                -79.131834,
                35.865309
             ],
             [
                -79.189947,
                35.87088
             ],
             [
                -79.192499,
                35.86548
             ],
             [
                -79.191696,
                35.86442
             ],
             [
                -79.191487,
                35.861699
             ],
             [
                -79.192945,
                35.859848
             ],
             [
                -79.192709,
                35.857424
             ],
             [
                -79.190852,
                35.854171
             ],
             [
                -79.192034,
                35.852068
             ],
             [
                -79.19121,
                35.848826
             ],
             [
                -79.191615,
                35.846797
             ],
             [
                -79.191048,
                35.846002
             ],
             [
                -79.191716,
                35.843134
             ],
             [
                -79.196298,
                35.842171
             ],
             [
                -79.196891,
                35.841242
             ],
             [
                -79.196407,
                35.837962
             ],
             [
                -79.211389,
                35.841743
             ],
             [
                -79.229284,
                35.84599
             ],
             [
                -79.230608,
                35.849349
             ],
             [
                -79.233528,
                35.847677
             ],
             [
                -79.236825,
                35.848553
             ],
             [
                -79.2366,
                35.849836
             ],
             [
                -79.237502,
                35.851123
             ],
             [
                -79.240385,
                35.852554
             ],
             [
                -79.244975,
                35.853994
             ],
             [
                -79.248089,
                35.854514
             ],
             [
                -79.249597,
                35.855718
             ],
             [
                -79.250745,
                35.858679
             ],
             [
                -79.250501,
                35.86094
             ],
             [
                -79.249589,
                35.862225
             ],
             [
                -79.249008,
                35.866423
             ],
             [
                -79.250818,
                35.869678
             ],
             [
                -79.250895,
                35.871629
             ],
             [
                -79.249321,
                35.875468
             ],
             [
                -79.249479,
                35.876804
             ],
             [
                -79.251341,
                35.880369
             ],
             [
                -79.254404,
                35.883847
             ],
             [
                -79.255962,
                35.886274
             ],
             [
                -79.257946,
                35.891493
             ],
             [
                -79.25826,
                35.894042
             ],
             [
                -79.25786,
                35.897475
             ],
             [
                -79.256516,
                35.901043
             ],
             [
                -79.257376,
                35.902709
             ],
             [
                -79.260419,
                35.905614
             ],
             [
                -79.264575,
                35.907924
             ],
             [
                -79.264152,
                35.930242
             ]
          ]
       ]
    },
    "properties":{
       "city":"Chapel hill",
       "state":"NC",
       "county":"Orange",
       "country":"US",
       "zipCode":"27516"
    }
}'''

#process json into python 2d array
obj = json.loads(js)
polyg = obj['geometry']
coor = polyg['coordinates']
xs = [x[0] for x in coor[0]]
ys = [x[1] for x in coor[0]]

#plot polygon
plt.plot(xs, ys)

#run primary function (number of circles, polygon, grain of descritization)
addCircles(5, coor[0], .003)

#record end time
end = time.time()

# total time taken, uncomment to print time
# print("Execution time of the program is- ", end-start)

plt.show()
