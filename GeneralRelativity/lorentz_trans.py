## sample script of Lorentz Transformation
## use natural units

import sympy as sym

def lorentz_transform_x(coor, v):
    """suppose in observer 1's frame, observer 2 is moving along x axis with velocity v21, and the origins of two frames coincide; this subroutine transform the coordinates of any event from frame 1 to frame 2.
    If you want to transform back from frame 2 to frame 1, just replace v with -v"""
    gam = 1/sym.sqrt(1-v**2)
    return  [gam*(coor[0]-v*coor[1]), gam*(coor[1]-v*coor[0]), coor[2], coor[3]]
    

t, l, v, u, ux, uy, uz = sym.symbols('t, l, v, u, ux, uy, uz') 

#=============== length contraction========================
# coordinates of ruler AB in its rest frame 2
a_fr2 = [ 0, 0, 0, 0] 
b_fr2 = [ 0, l, 0, 0]
#convert to frame 1
a_fr1 = lorentz_transform_x(a_fr2, -v)
b_fr1 = lorentz_transform_x(b_fr2, -v)
print("-------- LENGTH CONTRACTION ------------")
print("The length of the moving ruler is: " + str(sym.simplify(b_fr1[1] - a_fr1[1])))

#============== time dilation==============================
#coordinates in frame 1
depart_fr1 = [ 0, 0, 0, 0]
arrive_fr1 = [ t, v*t, 0, 0]
#convert to the clock's rest frame 2
depart_fr2 = lorentz_transform_x(depart_fr1, v)
arrive_fr2 = lorentz_transform_x(arrive_fr1, v)
print("-------- TIME DILATION ------------")
print("The clock (in its rest frame) has ticked: " + str(sym.simplify(arrive_fr2[0] - depart_fr2[0])))

#=============parallel velocity addition ===========================
coor_fr2 = [ t, u*t, 0, 0 ] ##object moving with velocity u in frame 2
coor_fr1 = lorentz_transform_x( coor_fr2, -v )
print("-------- PARALLEL VELOCITY ADDITION ------------")
print("v_total = " + str(sym.simplify( coor_fr1[1] / coor_fr1[0])))

#=============non-parallel velocity addition ===========================
coor_fr2 = [t, ux*t, uy*t, uz*t ]
coor_fr1 = lorentz_transform_x(coor_fr2, -v)
print("-------- NON-PARALLEL VELOCITY ADDITION ------------")
print("v_x_total = " + str(sym.simplify( coor_fr1[1]/coor_fr1[0] )))
print("v_y_total = " + str(sym.simplify( coor_fr1[2]/coor_fr1[0] )))
print("v_z_total = " + str(sym.simplify( coor_fr1[3]/coor_fr1[0] )))
