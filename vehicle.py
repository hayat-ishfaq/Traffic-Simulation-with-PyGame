"""
Vehicle module for Traffic Simulation
Contains Vehicle class with car and ambulance sprites
"""

import pygame
import config


class Vehicle(pygame.sprite.Sprite):
    """Represents a vehicle (car or ambulance) in the simulation"""
    
    def __init__(self, lane_id, is_emergency=False):
        super().__init__()
        self.lane_id = lane_id
        self.is_emergency = is_emergency
        
        if is_emergency:
            self.base_speed = 0.8 * 5  # Scale for pixels
            self.image = self._create_ambulance()
        else:
            self.base_speed = 0.5 * 5
            self.image = self._create_car()
        
        # Rotate based on direction
        self.direction = config.ROADS[lane_id]['dir']
        angle = 0
        if self.direction == (0, 1): 
            angle = -90
        elif self.direction == (-1, 0): 
            angle = 180
        elif self.direction == (0, -1): 
            angle = 90
        self.image = pygame.transform.rotate(self.image, angle)
        
        self.rect = self.image.get_rect()
        self.rect.center = config.ROADS[lane_id]['start']
        
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        self.speed = self.base_speed
        self.waiting_time = 0
        self.stopped = False
        
        # Get direction from config
        self.direction = config.ROADS[lane_id]['dir']
    
    def _create_car(self):
        """Create a normal car sprite"""
        car_width, car_height = 40, 20
        surface = pygame.Surface((car_width, car_height), pygame.SRCALPHA)
        
        # Car body - main shape
        body_color = (70, 130, 255)  # Blue
        pygame.draw.rect(surface, body_color, (4, 4, 32, 12), border_radius=3)
        
        # Car hood (front)
        pygame.draw.rect(surface, (50, 110, 220), (4, 4, 8, 12), border_radius=2)
        
        # Windshield (darker blue/tinted)
        pygame.draw.rect(surface, (40, 80, 150), (14, 6, 6, 8))
        
        # Back window
        pygame.draw.rect(surface, (40, 80, 150), (24, 6, 6, 8))
        
        # Side windows
        pygame.draw.rect(surface, (60, 100, 180), (20, 6, 3, 3))
        pygame.draw.rect(surface, (60, 100, 180), (20, 11, 3, 3))
        
        # Wheels (black circles with gray rims)
        pygame.draw.circle(surface, (20, 20, 20), (10, 3), 4)
        pygame.draw.circle(surface, (20, 20, 20), (10, 17), 4)
        pygame.draw.circle(surface, (20, 20, 20), (30, 3), 4)
        pygame.draw.circle(surface, (20, 20, 20), (30, 17), 4)
        # Wheel rims
        pygame.draw.circle(surface, (100, 100, 100), (10, 3), 2)
        pygame.draw.circle(surface, (100, 100, 100), (10, 17), 2)
        pygame.draw.circle(surface, (100, 100, 100), (30, 3), 2)
        pygame.draw.circle(surface, (100, 100, 100), (30, 17), 2)
        
        # Headlights
        pygame.draw.circle(surface, (255, 255, 220), (3, 6), 2)
        pygame.draw.circle(surface, (255, 255, 220), (3, 14), 2)
        
        # Taillights
        pygame.draw.circle(surface, (200, 0, 0), (37, 6), 2)
        pygame.draw.circle(surface, (200, 0, 0), (37, 14), 2)
        
        return surface
    
    def _create_ambulance(self):
        """Create an ambulance sprite"""
        amb_width, amb_height = 44, 22
        surface = pygame.Surface((amb_width, amb_height), pygame.SRCALPHA)
        
        # Ambulance body - white with red stripe
        body_color = (255, 255, 255)  # White
        pygame.draw.rect(surface, body_color, (4, 3, 36, 16), border_radius=2)
        
        # Red stripe on side
        pygame.draw.rect(surface, (255, 0, 0), (10, 8, 24, 6))
        
        # Red cross symbol
        pygame.draw.rect(surface, (255, 255, 255), (20, 9, 2, 4))  # Vertical
        pygame.draw.rect(surface, (255, 255, 255), (18, 11, 6, 2))  # Horizontal
        
        # Ambulance cab (front section)
        pygame.draw.rect(surface, (240, 240, 240), (4, 6, 8, 10), border_radius=2)
        
        # Windows
        pygame.draw.rect(surface, (100, 150, 200), (14, 5, 6, 6))
        pygame.draw.rect(surface, (100, 150, 200), (24, 5, 6, 6))
        pygame.draw.rect(surface, (100, 150, 200), (32, 8, 6, 6))
        
        # Wheels (larger for ambulance)
        pygame.draw.circle(surface, (20, 20, 20), (11, 2), 4)
        pygame.draw.circle(surface, (20, 20, 20), (11, 20), 4)
        pygame.draw.circle(surface, (20, 20, 20), (33, 2), 4)
        pygame.draw.circle(surface, (20, 20, 20), (33, 20), 4)
        
        # Headlights (brighter)
        pygame.draw.circle(surface, (255, 255, 255), (3, 7), 2)
        pygame.draw.circle(surface, (255, 255, 255), (3, 15), 2)
        
        # Emergency lights on top (red and blue)
        pygame.draw.rect(surface, (255, 0, 0), (17, 1, 4, 3), border_radius=1)
        pygame.draw.rect(surface, (0, 100, 255), (23, 1, 4, 3), border_radius=1)
        
        # Text "AMBULANCE" (simplified)
        font = pygame.font.SysFont('Arial', 6, bold=True)
        text = font.render('AMB', True, (255, 255, 255))
        surface.blit(text, (19, 10))
        
        return surface

    def update(self, vehicles, traffic_lights, traffic_manager):
        """Update vehicle position and behavior"""
        # 1. Acceleration / Deceleration
        target_speed = self.base_speed
        
        # 2. Check collision with car in front
        min_dist = 9999
        for v in vehicles:
            if v is not self and v.lane_id == self.lane_id:
                # Calculate distance based on direction
                dist = 9999
                if self.direction == (1, 0) and v.pos_x > self.pos_x:
                    dist = v.pos_x - self.pos_x
                elif self.direction == (-1, 0) and v.pos_x < self.pos_x:
                    dist = self.pos_x - v.pos_x
                elif self.direction == (0, 1) and v.pos_y > self.pos_y:
                    dist = v.pos_y - self.pos_y
                elif self.direction == (0, -1) and v.pos_y < self.pos_y:
                    dist = self.pos_y - v.pos_y
                
                if dist < min_dist:
                    min_dist = dist

        if min_dist < config.SAFE_DISTANCE:
            target_speed = 0

        # 3. Check Traffic Lights
        stops = config.STOP_LINES[self.lane_id]
        is_green = traffic_lights[self.lane_id] == 1 
        
        # Emergency vehicle override
        if self.is_emergency and traffic_manager.emergency_active:
            if traffic_manager.emergency_lane == self.lane_id:
                is_green = True

        for stop_coord in stops:
            dist_to_stop = 9999
            
            if self.direction == (1, 0):  # Horizontal Right
                dist_to_stop = stop_coord - self.rect.right
            elif self.direction == (-1, 0):  # Horizontal Left
                dist_to_stop = self.rect.left - stop_coord
            elif self.direction == (0, 1):  # Vertical Down
                dist_to_stop = stop_coord - self.rect.bottom
            elif self.direction == (0, -1):  # Vertical Up
                dist_to_stop = self.rect.top - stop_coord
            
            # Stop if light is red and approaching
            if 0 < dist_to_stop < config.STOP_DISTANCE and not is_green:
                if dist_to_stop < config.INTERSECTION_MARGIN:
                    target_speed = 0
                else:
                    # Slow down naturally
                    target_speed = min(target_speed, dist_to_stop * 0.1)

        # Smooth speed transition
        self.speed += (target_speed - self.speed) * 0.2
        if self.speed < 0.1: 
            self.speed = 0
        
        # Update statistics
        if self.speed < 0.1:
            self.waiting_time += 1
            self.stopped = True
        else:
            self.stopped = False
        
        # 4. Update Position
        self.pos_x += self.direction[0] * self.speed
        self.pos_y += self.direction[1] * self.speed
        
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        
        # 5. Remove if off-screen
        if self.rect.right < -100 or self.rect.left > config.WIDTH + 100:
            self.kill()
        if self.rect.bottom < -100 or self.rect.top > config.HEIGHT + 100:
            self.kill()
