"""
Configuration file for Traffic Simulation
Contains all constants, settings, and road layout definitions
"""

import pygame

# Window Settings - Will be set to fullscreen in main
WIDTH, HEIGHT = 0, 0  # Will be set dynamically
FPS = 60
FULLSCREEN = False

# Road Configuration
ROAD_WIDTH = 60
LANE_OFFSET = ROAD_WIDTH // 2
INTERSECTION_MARGIN = 6  # Units to stop before intersection
STOP_DISTANCE = 40       # Distance to check for stop line
SAFE_DISTANCE = 50       # Distance to keep from car in front

# Intersection spacing (distance between roads)
INTERSECTION_SPACING = 300  # Distance between parallel roads

# Intersection spacing (distance between roads)
INTERSECTION_SPACING = 300  # Distance between parallel roads

# Colors - Realistic theme
COLOR_GRASS = (34, 139, 34)      # Grass green background
COLOR_ROAD = (60, 60, 65)        # Dark asphalt
COLOR_SIDEWALK = (180, 180, 180) # Light gray
COLOR_LANE_WHITE = (255, 255, 255)
COLOR_LANE_YELLOW = (255, 220, 0)
COLOR_VEHICLE_REG = (70, 130, 255) # Blue
COLOR_VEHICLE_EMG = (255, 50, 50)  # Red
COLOR_TEXT = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 200, 0)
AMBER = (255, 191, 0)


def init_screen_dependent_config(screen_width, screen_height):
    """Initialize configuration that depends on screen dimensions"""
    global WIDTH, HEIGHT, ROADS, STOP_LINES
    
    WIDTH = screen_width
    HEIGHT = screen_height
    
    # Calculate centered road positions
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Road positions centered on screen
    road_left = center_x - INTERSECTION_SPACING // 2
    road_right = center_x + INTERSECTION_SPACING // 2
    road_top = center_y - INTERSECTION_SPACING // 2
    road_bottom = center_y + INTERSECTION_SPACING // 2
    
    # Road Layout - Dynamically centered
    # 0: Top Horiz (L->R), 1: Right Vert (T->B), 2: Bot Horiz (R->L), 3: Left Vert (B->T)
    ROADS = {
        0: {'y': road_top, 'dir': (1, 0),  'start': (-50, road_top), 'name': "Horizontal-Upper"},
        1: {'x': road_right, 'dir': (0, 1),  'start': (road_right, -50), 'name': "Vertical-Right"},
        2: {'y': road_bottom, 'dir': (-1, 0), 'start': (WIDTH + 50, road_bottom), 'name': "Horizontal-Lower"},
        3: {'x': road_left, 'dir': (0, -1), 'start': (road_left, HEIGHT + 50), 'name': "Vertical-Left"}
    }
    
    # Stop lines (coordinates where cars stop for lights)
    STOP_LINES = {
        0: [road_left - ROAD_WIDTH, road_right - ROAD_WIDTH],
        1: [road_top - ROAD_WIDTH, road_bottom - ROAD_WIDTH],
        2: [road_right + ROAD_WIDTH, road_left + ROAD_WIDTH],
        3: [road_bottom + ROAD_WIDTH, road_top + ROAD_WIDTH]
    }

# Spawn Configuration
REGULAR_SPAWN_INTERVAL = 1500  # milliseconds
EMERGENCY_SPAWN_INTERVAL = 5000  # milliseconds
