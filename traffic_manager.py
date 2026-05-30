"""
Traffic Manager module for Traffic Simulation
Manages traffic light states and adaptive timing
"""

import config


class TrafficManager:
    """Manages traffic light states with adaptive timing and emergency overrides"""
    
    def __init__(self):
        # Traffic light states: 0 = Red, 1 = Green
        self.lights = [0, 0, 0, 0] 
        self.current_phase = 0  # Starts with Horizontal Upper
        
        # Timing (in frames)
        self.base_timer = 60
        self.timer = self.base_timer
        self.timer_counter = 0
        
        # Emergency handling
        self.emergency_active = False
        self.emergency_lane = -1
        self.emergency_override_duration = 0

    def update(self, vehicles):
        """Update traffic light states based on current traffic conditions"""
        
        # --- Emergency Logic ---
        # Detect emergency vehicles
        emg_vehicle = None
        for v in vehicles:
            if v.is_emergency:
                emg_vehicle = v
                break
        
        if emg_vehicle:
            self.emergency_active = True
            self.emergency_lane = emg_vehicle.lane_id
            # All lights red except emergency lane
            for i in range(4):
                self.lights[i] = 1 if i == self.emergency_lane else 0
            return  # Skip normal adaptive logic
        else:
            self.emergency_active = False

        # --- Adaptive Traffic Light Logic ---
        # Count waiting vehicles in each lane
        waiting_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        for v in vehicles:
            if v.stopped:
                waiting_counts[v.lane_id] += 1
        
        current_lane_load = waiting_counts[self.current_phase]
        other_lane_load = sum(waiting_counts.values()) - current_lane_load

        # Adaptive timer adjustments
        current_max_time = self.base_timer
        if current_lane_load > 3:
            current_max_time = 100  # Extend if many cars waiting
        elif other_lane_load > 5:
            current_max_time = 40   # Shorten if other lanes busy

        # Cycle State Machine
        self.timer_counter += 1
        
        # Set lights based on current phase
        for i in range(4):
            if i == self.current_phase:
                self.lights[i] = 1  # Green
            else:
                self.lights[i] = 0  # Red

        # Move to next phase when timer expires
        if self.timer_counter >= current_max_time:
            self.timer_counter = 0
            self.current_phase = (self.current_phase + 1) % 4
