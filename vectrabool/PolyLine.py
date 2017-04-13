#!/usr/bin/python


class PolyLine:
    def __init__(self, points):
        # List of points, coded as tuples (x,y)
        self.points = points
        # The lists of all x (rep. y) coordinates
        self.x, self.y = [], []
        for p in points:
            self.x.append(p[0])
            self.y.append(p[1])

    def draw(self, show=False):
        """Draw the polyline in the current matplotlib figure.
        If show is set to True, show the graph."""
        p = plt.plot(self.x, self.y)
        plt.axis('equal')
        if show:
            plt.show(block=True)

    def draw_with_corners(self, corners, show=True):
        self.draw()
        plt.plot([c[0] for c in corners], [c[1] for c in corners], 'ro', marker='*')
        if show:
            plt.show(block=True)

    def get_points(self):
        return self.points


if __name__ == "__main__":
    print("This is class PolyLine.")
    p1 = PolyLine([(0, 4), (3, 2), (2, -2), (-1, -3)])
    p2 = PolyLine([(-3, 1), (1, 7), (6, 0)])
    print("Example with polylines {} and {}...".format(p1.points, p2.points))
    p1.draw()
    p2.draw()
    plt.show()
    print("Done.")
