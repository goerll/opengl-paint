class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Vector addition using + operator"""
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Can only add Vec2 to Vec2")

    def __sub__(self, other):
        """Vector subtraction using - operator"""
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Can only subtract Vec2 from Vec2")
    
    def __mul__(self, other):
        """Dot product using * operator"""
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Can only multiply Vec2 with Vec2")

    def add(self, other):
        """Alternative method for vector addition"""
        return self.__add__(other)

    def subtract(self, other):
        """Alternative method for vector subtraction"""
        return self.__sub__(other)

    def length(self):
        """Calculate the length (magnitude) of the vector"""
        return (self.x**2 + self.y**2) ** 0.5

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"


class Vec3:
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        """Vector addition using + operator"""
        if isinstance(other, Vec3):
            return Vec3(self.r + other.r, self.g + other.g, self.b + other.b)
        else:
            raise TypeError("Can only add Vec3 to Vec3")

    def __sub__(self, other):
        """Vector subtraction using - operator"""
        if isinstance(other, Vec3):
            return Vec3(self.r - other.r, self.g - other.g, self.b - other.b)
        else:
            raise TypeError("Can only subtract Vec3 from Vec3")

    def __mul__(self, other):
        """Dot product using * operator"""
        if isinstance(other, Vec3):
            return self.r * other.r + self.g * other.g + self.b * other.b
        else:
            raise TypeError("Can only multiply Vec3 with Vec3")

    def add(self, other):
        """Alternative method for vector addition"""
        return self.__add__(other)

    def subtract(self, other):
        """Alternative method for vector subtraction"""
        return self.__sub__(other)

    def length(self):
        """Calculate the length (magnitude) of the vector"""
        return (self.r**2 + self.g**2 + self.b**2) ** 0.5

    def __repr__(self):
        return f"Vec3({self.r}, {self.g}, {self.b})"
