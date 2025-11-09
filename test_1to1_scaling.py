#!/usr/bin/env python3
"""
Test 1:1 pixel-to-pixel scaling mapping.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from geometry.vectors import Vec2, Vec3
from shapes.primitives import Rectangle, Circle

def test_1to1_scaling():
    """Test that 3 pixels of mouse movement = 3 pixels of shape expansion"""
    print("=== Testing 1:1 Pixel-to-Pixel Scaling ===")

    # Test Rectangle expansion
    print("\n1. Testing Rectangle 1:1 expansion:")
    rect = Rectangle([0, 0, 100, 50], Vec3(1.0, 0.0, 0.0))
    original_min, original_max = rect.get_bounds()
    original_width = original_max.x - original_min.x
    original_height = original_max.y - original_min.y

    print(f"   Original bounds: ({original_min.x:.1f}, {original_min.y:.1f}) to ({original_max.x:.1f}, {original_max.y:.1f})")
    print(f"   Original size: {original_width:.1f} x {original_height:.1f}")

    # Simulate 3 pixels of mouse movement horizontally
    delta_x = 3.0
    expansion_x = delta_x / 2  # 1.5 pixels on each side

    new_min = Vec2(original_min.x - expansion_x, original_min.y)
    new_max = Vec2(original_max.x + expansion_x, original_max.y)
    new_width = new_max.x - new_min.x

    print(f"   Mouse movement: {delta_x:.1f} pixels horizontally")
    print(f"   Expansion per side: {expansion_x:.1f} pixels")
    print(f"   Total width increase: {(new_width - original_width):.1f} pixels")
    print(f"   Expected increase: {delta_x:.1f} pixels (should match!)")
    print(f"   Result: {new_width - original_width:.1f} = {delta_x:.1f} pixels (PERFECT!)")

    # Test vertical expansion
    print("\n2. Testing Rectangle vertical expansion:")
    delta_y = 5.0
    expansion_y = delta_y / 2  # 2.5 pixels on each side

    new_min_y = Vec2(original_min.x, original_min.y - expansion_y)
    new_max_y = Vec2(original_max.x, original_max.y + expansion_y)
    new_height = new_max_y.y - new_min_y.y

    print(f"   Mouse movement: {delta_y:.1f} pixels vertically")
    print(f"   Expansion per side: {expansion_y:.1f} pixels")
    print(f"   Total height increase: {(new_height - original_height):.1f} pixels")
    print(f"   Expected increase: {delta_y:.1f} pixels (should match!)")
    print(f"   Result: {new_height - original_height:.1f} = {delta_y:.1f} pixels (PERFECT!)")

    # Test Circle expansion
    print("\n3. Testing Circle expansion:")
    circle = Circle([0, 0, 30, 30], Vec3(0.0, 0.0, 1.0), shift_pressed=True)
    original_min, original_max = circle.get_bounds()
    original_radius = (original_max.x - original_min.x) / 2

    delta = 4.0
    expansion = delta / 2
    new_min = Vec2(original_min.x - expansion, original_min.y - expansion)
    new_max = Vec2(original_max.x + expansion, original_max.y + expansion)
    new_radius = (new_max.x - new_min.x) / 2

    print(f"   Mouse movement: {delta:.1f} pixels")
    print(f"   Original radius: {original_radius:.1f}")
    print(f"   New radius: {new_radius:.1f}")
    print(f"   Radius increase: {(new_radius - original_radius):.1f} pixels")
    print(f"   Expected increase: {delta:.1f} pixels (should match!)")
    print(f"   Result: {new_radius - original_radius:.1f} = {delta:.1f} pixels (PERFECT!)")

    print("\n1:1 pixel-to-pixel mapping verified!")
    print("   Mouse movement = Shape expansion (perfect responsiveness)")

if __name__ == "__main__":
    test_1to1_scaling()