"""
Main entry point for Traffic Simulation
Handles game loop, event processing, and simulation updates
"""

import pygame
import random
import config
from config import FPS, REGULAR_SPAWN_INTERVAL, EMERGENCY_SPAWN_INTERVAL, FULLSCREEN
from vehicle import Vehicle
from traffic_manager import TrafficManager
from renderer import draw_roads, draw_lights, draw_ui


def main():
    """Main simulation loop"""
    # Initialize Pygame
    pygame.init()
    
    # Set up fullscreen or windowed mode
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
    else:
        screen_width = 1280
        screen_height = 720
        screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Initialize screen-dependent configuration
    config.init_screen_dependent_config(screen_width, screen_height)
    
    pygame.display.set_caption("Traffic Simulation - Adaptive 4-Way System")
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    vehicles = pygame.sprite.Group()
    
    # Create traffic manager
    traffic_manager = TrafficManager()
    
    # Set up spawn timers
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, REGULAR_SPAWN_INTERVAL)
    
    EMG_SPAWN_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(EMG_SPAWN_EVENT, EMERGENCY_SPAWN_INTERVAL)

    # Main game loop
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            elif event.type == SPAWN_EVENT:
                # Spawn regular car
                lane = random.randint(0, 3)
                v = Vehicle(lane, is_emergency=False)
                # Avoid spawning on top of another vehicle
                if not pygame.sprite.spritecollideany(v, vehicles):
                    all_sprites.add(v)
                    vehicles.add(v)
            
            elif event.type == EMG_SPAWN_EVENT:
                # Spawn emergency vehicle
                lane = random.randint(0, 3)
                v = Vehicle(lane, is_emergency=True)
                all_sprites.add(v)
                vehicles.add(v)

        # 2. Update Logic
        traffic_manager.update(vehicles)
        
        for v in vehicles:
            v.update(vehicles, traffic_manager.lights, traffic_manager)

        # 3. Drawing
        draw_roads(screen)
        draw_lights(screen, traffic_manager.lights)
        all_sprites.draw(screen)
        draw_ui(screen, vehicles, traffic_manager)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
