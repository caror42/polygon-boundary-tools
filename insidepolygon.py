
# Checking if a point is inside a polygon
def pointInPoly(point, polygon):
    num_vertices = len(polygon)
    x, y = point[0], point[1]
    inside = False
    
    #check if x or y is entirely out of range of the polygon to save time
    if(x < min([a[0] for a in polygon]) or x > max([a[0] for a in polygon]) or y < min([a[1] for a in polygon]) or y > max([a[1] for a in polygon])):
        print("completely out of bounds")
        return False
    
    # Store the first point in the polygon and initialize the second point
    p1 = polygon[0]
 
    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        
        # Get the next point in the polygon
        p2 = polygon[i % num_vertices]
 
        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1[1], p2[1]):
            
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1[1], p2[1]):
                
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1[0], p2[0]):
                    
                    # Calculate the x-intersection of the line connecting the point to the edge
                    #confirm non-horizontal edge to avvoid divide by zero error
                    if(p2[1]-p1[1] != 0):
                        x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                        
                        # Check if the point is on the same line as the edge or to the left of the x-intersection
                        if p1[0] == p2[0] or x <= x_intersection:
                            # Flip the inside flag
                            inside = not inside
                    else:
                        inside = not inside
 
        # Store the current point as the first point for the next iteration
        p1 = p2
 
    # Return the value of the inside flag
    return inside
 
#point to test
point = [176, 43]
 
# Define a polygon
polygon = [
    [186, 14],
    [186, 44],
    [175, 44],
    [175, 14],
    [186, 14]
]
 
# Check if the point is inside the polygon
if pointInPoly(point, polygon):
    print("Point is inside the polygon")
else:
    print("Point is outside the polygon")