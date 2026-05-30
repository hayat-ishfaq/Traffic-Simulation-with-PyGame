# Traffic Simulation with PyGame

An adaptive traffic simulation system featuring realistic vehicle behavior, emergency vehicle priority, and intelligent traffic light management.

## Features

### Core Components
- **Road Layout**: 2 vertical + 2 horizontal roads creating 4 intersections
- **Regular Vehicles**: Blue cars following traffic rules
- **Emergency Vehicles**: White ambulances with priority (spawn every 5s)
- **Adaptive Traffic Lights**: 4 intelligent traffic lights with dynamic timing

### Traffic Light Logic
- **Sequence**: Horizontal-Upper → Vertical-Right → Horizontal-Lower → Vertical-Left
- **Base Timer**: 60 ticks (~1 second)
- **Adaptive Timing**:
  - Extends to 100 ticks if >3 cars waiting in current lane
  - Shortens to 40 ticks if >5 cars waiting in other lanes
- **Emergency Override**: All lights turn red except for emergency vehicle's direction

### Vehicle Behavior
- **Regular Speed**: 0.5 units/frame
- **Emergency Speed**: 0.8 units/frame
- Stop at red lights within 40 pixels of intersection
- Collision avoidance with 50-pixel safe distance
- Can clear intersection if already inside

### Visual Design
- Realistic grass background with gray sidewalks
- Asphalt roads with proper lane markings (yellow dashed center, white solid edges)
- Crosswalks at all intersections
- Detailed vehicle sprites (cars with windows, wheels, lights)
- Realistic 3-light traffic signals (red, yellow, green)
- Semi-transparent UI panel with real-time statistics

## Project Structure

```
python/
├── config.py           # Configuration and constants
├── vehicle.py          # Vehicle class with car and ambulance sprites
├── traffic_manager.py  # Traffic light management and adaptive logic
├── renderer.py         # Drawing functions for roads, lights, and UI
├── main.py            # Main game loop and entry point
├── road_network.py    # Legacy monolithic file (can be removed)
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Installation

1. **Install Python 3.7+**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulation:
```bash
python main.py
```

**Controls**:
- Press `ESC` or close the window to exit

## Configuration

Edit `config.py` to customize:
- Window dimensions (`WIDTH`, `HEIGHT`)
- Frame rate (`FPS`)
- Road layout and dimensions
- Vehicle spawn intervals
- Colors and visual settings

## UI Information

The top-left panel displays:
- **Cars**: Number of regular vehicles
- **Ambulances**: Number of emergency vehicles
- **Avg Wait**: Average waiting time in seconds
- **Current Phase**: Active traffic light phase or emergency status

## Technical Details

- **Framework**: PyGame 2.6+
- **FPS**: 60 frames per second
- **Collision Detection**: Sprite-based collision checking
- **Adaptive Algorithm**: Real-time traffic density analysis
- **Emergency Protocol**: Instant light override for priority vehicles

## Author

Traffic Simulation System - 2025
