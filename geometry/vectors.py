from typing import Union


class Vec2:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vec2') -> 'Vec2':
        """Vector addition using + operator"""
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Can only add Vec2 to Vec2")

    def __sub__(self, other: 'Vec2') -> 'Vec2':
        """Vector subtraction using - operator"""
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Can only subtract Vec2 from Vec2")

    def __mul__(self, other: Union['Vec2', float]) -> Union[float, 'Vec2']:
        """Dot product using * operator"""
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        else:
            raise TypeError("Can only multiply Vec2 with Vec2 or scalar")

    
    def length(self) -> float:
        """Calculate the length (magnitude) of the vector"""
        return (self.x**2 + self.y**2) ** 0.5

    def distance_to(self, other: 'Vec2') -> float:
        """Calculate the distance to another Vec2"""
        return (other - self).length()

    def distance_squared_to(self, other: 'Vec2') -> float:
        """Calculate the squared distance to another Vec2 (faster, no sqrt)"""
        dx = other.x - self.x
        dy = other.y - self.y
        return dx * dx + dy * dy

    def normalized(self) -> 'Vec2':
        """Return a normalized copy of this vector"""
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return Vec2(self.x / length, self.y / length)

    def lerp(self, other: 'Vec2', t: float) -> 'Vec2':
        """Linear interpolation between this vector and another"""
        return self + (other - self) * t

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"


class Vec3:
    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other: 'Vec3') -> 'Vec3':
        """Vector addition using + operator"""
        if isinstance(other, Vec3):
            return Vec3(self.r + other.r, self.g + other.g, self.b + other.b)
        else:
            raise TypeError("Can only add Vec3 to Vec3")

    def __sub__(self, other: 'Vec3') -> 'Vec3':
        """Vector subtraction using - operator"""
        if isinstance(other, Vec3):
            return Vec3(self.r - other.r, self.g - other.g, self.b - other.b)
        else:
            raise TypeError("Can only subtract Vec3 from Vec3")

    def __mul__(self, other: Union['Vec3', float]) -> Union[float, 'Vec3']:
        """Dot product using * operator"""
        if isinstance(other, Vec3):
            return self.r * other.r + self.g * other.g + self.b * other.b
        elif isinstance(other, (int, float)):
            return Vec3(self.r * other, self.g * other, self.b * other)
        else:
            raise TypeError("Can only multiply Vec3 with Vec3 or scalar")

    
    def length(self) -> float:
        """Calculate the length (magnitude) of the vector"""
        return (self.r**2 + self.g**2 + self.b**2) ** 0.5

    def __repr__(self) -> str:
        return f"Vec3({self.r}, {self.g}, {self.b})"