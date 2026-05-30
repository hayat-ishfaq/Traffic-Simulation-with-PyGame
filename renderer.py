"""
Renderer module for Traffic Simulation
Contains all drawing functions for roads, lights, and UI
"""

import pygame
import config


def draw_roads(surface):
    """Draw road network with grass, sidewalks, lanes, and crosswalks"""
    # Fill with grass background
    surface.fill(config.COLOR_GRASS)
    
    # Get road positions from config
    center_x = config.WIDTH // 2
    center_y = config.HEIGHT // 2
    road_left = center_x - config.INTERSECTION_SPACING // 2
    road_right = center_x + config.INTERSECTION_SPACING // 2
    road_top = center_y - config.INTERSECTION_SPACING // 2
    road_bottom = center_y + config.INTERSECTION_SPACING // 2
    
    # Draw sidewalks (slightly wider than roads)
    sidewalk_width = 70
    pygame.draw.rect(surface, config.COLOR_SIDEWALK, (0, road_top - 35, config.WIDTH, sidewalk_width))
    pygame.draw.rect(surface, config.COLOR_SIDEWALK, (0, road_bottom - 35, config.WIDTH, sidewalk_width))
    pygame.draw.rect(surface, config.COLOR_SIDEWALK, (road_left - 35, 0, sidewalk_width, config.HEIGHT))
    pygame.draw.rect(surface, config.COLOR_SIDEWALK, (road_right - 35, 0, sidewalk_width, config.HEIGHT))
    
    # Draw Road Pavement
    pygame.draw.rect(surface, config.COLOR_ROAD, (0, road_top - 30, config.WIDTH, 60))
    pygame.draw.rect(surface, config.COLOR_ROAD, (0, road_bottom - 30, config.WIDTH, 60))
    pygame.draw.rect(surface, config.COLOR_ROAD, (road_left - 30, 0, 60, config.HEIGHT))
    pygame.draw.rect(surface, config.COLOR_ROAD, (road_right - 30, 0, 60, config.HEIGHT))
    
    # Draw intersection boxes
    intersections = [
        (road_left-30, road_top-30, 60, 60), (road_right-30, road_top-30, 60, 60),
        (road_left-30, road_bottom-30, 60, 60), (road_right-30, road_bottom-30, 60, 60)
    ]
    for rect in intersections:
        pygame.draw.rect(surface, config.COLOR_ROAD, rect)
    
    # Draw Center Lane Lines (Dashed yellow)
    dash_length = 15
    gap_length = 10
    
    # Horizontal roads center lines
    for y in [road_top, road_bottom]:
        x = 0
        while x < config.WIDTH:
            pygame.draw.line(surface, config.COLOR_LANE_YELLOW, (x, y), 
                           (min(x + dash_length, config.WIDTH), y), 2)
            x += dash_length + gap_length
    
    # Vertical roads center lines
    for x in [road_left, road_right]:
        y = 0
        while y < config.HEIGHT:
            pygame.draw.line(surface, config.COLOR_LANE_YELLOW, (x, y), 
                           (x, min(y + dash_length, config.HEIGHT)), 2)
            y += dash_length + gap_length
    
    # Draw edge lines (white solid)
    # Horizontal roads
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (0, road_top - 30), (config.WIDTH, road_top - 30), 2)
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (0, road_top + 30), (config.WIDTH, road_top + 30), 2)
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (0, road_bottom - 30), (config.WIDTH, road_bottom - 30), 2)
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (0, road_bottom + 30), (config.WIDTH, road_bottom + 30), 2)
    
    # Vertical roads
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (road_left - 30, 0), (road_left - 30, config.HEIGHT), 2)
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (road_left + 30, 0), (road_left + 30, config.HEIGHT), 2)
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (road_right - 30, 0), (road_right - 30, config.HEIGHT), 2)
    pygame.draw.line(surface, config.COLOR_LANE_WHITE, (road_right + 30, 0), (road_right + 30, config.HEIGHT), 2)
    
    # Draw crosswalks at intersections
    _draw_crosswalks(surface, road_left, road_right, road_top, road_bottom)


def _draw_crosswalks(surface, road_left, road_right, road_top, road_bottom):
    """Helper function to draw crosswalks at all intersections"""
    crosswalk_color = (255, 255, 255)
    stripe_width = 4
    stripe_spacing = 6
    
    # Top-left intersection
    for i in range(5):
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_left - 30 - i * stripe_spacing, road_top - 10, stripe_width, 20))
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_left - 10, road_top - 30 - i * stripe_spacing, 20, stripe_width))
    
    # Top-right intersection
    for i in range(5):
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_right - 30 - i * stripe_spacing, road_top - 10, stripe_width, 20))
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_right + 10, road_top - 30 - i * stripe_spacing, 20, stripe_width))
    
    # Bottom-left intersection
    for i in range(5):
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_left - 30 - i * stripe_spacing, road_bottom - 10, stripe_width, 20))
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_left - 10, road_bottom - 30 - i * stripe_spacing, 20, stripe_width))
    
    # Bottom-right intersection
    for i in range(5):
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_right - 30 - i * stripe_spacing, road_bottom - 10, stripe_width, 20))
        pygame.draw.rect(surface, crosswalk_color, 
                        (road_right + 10, road_bottom - 30 - i * stripe_spacing, 20, stripe_width))


def draw_lights(surface, lights):
    """Draw realistic traffic lights at intersections"""
    # Calculate road positions dynamically
    center_x = config.WIDTH // 2
    center_y = config.HEIGHT // 2
    road_left = center_x - config.INTERSECTION_SPACING // 2
    road_right = center_x + config.INTERSECTION_SPACING // 2
    road_top = center_y - config.INTERSECTION_SPACING // 2
    road_bottom = center_y + config.INTERSECTION_SPACING // 2
    
    positions = {
        0: [(road_left - 30, road_top - 40), (road_right - 30, road_top - 40)],  # Top road
        1: [(road_right + 40, road_top - 30), (road_right + 40, road_bottom - 30)],  # Right road
        2: [(road_right + 30, road_bottom + 40), (road_left + 30, road_bottom + 40)],  # Bottom road
        3: [(road_left - 40, road_bottom + 30), (road_left - 40, road_top + 30)]   # Left road
    }
    
    for lane, coords in positions.items():
        is_green = lights[lane] == 1
        
        for pos in coords:
            # Traffic light pole
            pygame.draw.rect(surface, (80, 80, 80), (pos[0] - 3, pos[1] + 15, 6, 20))
            
            # Traffic light box
            pygame.draw.rect(surface, (40, 40, 40), 
                           (pos[0] - 12, pos[1] - 30, 24, 40), border_radius=3)
            pygame.draw.rect(surface, (200, 200, 200), 
                           (pos[0] - 12, pos[1] - 30, 24, 40), 2, border_radius=3)
            
            # Red light (top)
            red_color = config.RED if not is_green else (80, 0, 0)
            pygame.draw.circle(surface, red_color, (pos[0], pos[1] - 20), 6)
            
            # Yellow light (middle) - off
            pygame.draw.circle(surface, (80, 80, 0), (pos[0], pos[1] - 5), 6)
            
            # Green light (bottom)
            green_color = config.GREEN if is_green else (0, 80, 0)
            pygame.draw.circle(surface, green_color, (pos[0], pos[1] + 10), 6)


def draw_ui(surface, vehicles, traffic_manager):
    """Draw UI panel with simulation statistics"""
    # Create semi-transparent panel
    panel = pygame.Surface((280, 130), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    surface.blit(panel, (10, 10))
    
    font_title = pygame.font.SysFont("Arial", 18, bold=True)
    font = pygame.font.SysFont("Arial", 15)
    
    # Calculate statistics
    reg_count = sum(1 for v in vehicles if not v.is_emergency)
    emg_count = sum(1 for v in vehicles if v.is_emergency)
    
    total_wait = sum(v.waiting_time for v in vehicles)
    avg_wait = (total_wait / len(vehicles)) / config.FPS if vehicles else 0.0
    
    # State Info
    state_text = config.ROADS[traffic_manager.current_phase]['name']
    if traffic_manager.emergency_active:
        state_text = "🚨 EMERGENCY"
        text_color = config.RED
    else:
        text_color = config.GREEN

    # Title
    title = font_title.render("Traffic Monitor", True, (255, 255, 100))
    surface.blit(title, (20, 15))
    
    y = 45
    
    # Regular vehicles
    pygame.draw.circle(surface, config.COLOR_VEHICLE_REG, (25, y + 5), 5)
    txt = font.render(f"Cars: {reg_count}", True, config.COLOR_TEXT)
    surface.blit(txt, (40, y))
    y += 22
    
    # Emergency vehicles
    pygame.draw.circle(surface, config.COLOR_VEHICLE_EMG, (25, y + 5), 5)
    txt = font.render(f"Ambulances: {emg_count}", True, config.COLOR_TEXT)
    surface.blit(txt, (40, y))
    y += 22
    
    # Wait time
    txt = font.render(f"Avg Wait: {avg_wait:.1f}s", True, (150, 255, 150))
    surface.blit(txt, (20, y))
    y += 22
    
    # Active state
    txt = font.render(f"{state_text}", True, text_color)
    surface.blit(txt, (20, y))
