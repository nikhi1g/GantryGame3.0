def main():
    import gantry
    import pickle
    import time

    scale_factor = 8
    offset = (0,0)

    def pen_up():
        gantry.set_pos_noblock(z=5)
        time.sleep(.05)
        while any(axis.is_moving() for axis in gantry.axes()):
            time.sleep(.005)
    def pen_down():
        gantry.set_pos_noblock(z=0)
        time.sleep(.05)
        while any(axis.is_moving() for axis in gantry.axes()):
            time.sleep(.005)

    def move(point, cords=None):

        x,y = point
        x *= scale_factor
        y *= scale_factor


        x += offset[0]
        y += offset[1]

        gantry.trap_move(x,y, cords)

        # # time.sleep(.1)
        # while any(axis.is_moving() for axis in gantry.axes()):
        #     time.sleep(.1)

        threshold = .1


        # while abs(gantry.x.get_pos() - x) > threshold or abs(gantry.y.get_pos() - y) > threshold:
        #     time.sleep(.001)
        
        
    segments = None
    import os
    import sys

    with open("path.pickle", "rb") as file:
        segments = pickle.load(file)
        # print(segments)



    gantry = gantry.Gantry()
    gantry.startup()
    print("started")


    # while True:
    #     gantry.set_pos_noblock(z=float(input()))

    pen_up()

    input("press return to start")

    pen_up()
    for i, seg in enumerate(segments):
        print(f"Currently on segment {i}/{len(segments)}")

        move(seg[0])
        # print(seg[0])
        pen_down()

        cords = None
        for point in seg[1:]:
            cords = move(point, cords)
        pen_up()

    print("done")
    pen_up()


    

if __name__ == "__main__":
    main()

