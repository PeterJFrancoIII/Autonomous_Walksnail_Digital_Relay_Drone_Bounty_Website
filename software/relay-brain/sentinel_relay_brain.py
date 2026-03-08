#!/usr/bin/env python3
"""
MODULE: sentinel_relay_brain.py
PROJECT: Project Sentinel — Autonomous 1-Hour FPV Relay Challenge
LICENSE: MIT

DESCRIPTION:
    Core autonomous positioning module for the Relay Drone. Interfaces with the
    ArduPilot flight controller via PyMAVLink to intercept telemetry data, calculate
    the optimal Line-of-Sight (LOS) position between the Pilot and the Worker Drone,
    and issue dynamic Guided Mode movement commands.

EFFECT ON PROGRAM:
    When executed on the Companion Computer (Orange Pi Zero 3 / Raspberry Pi Zero 2 W),
    this script takes over the positional authority of the Relay Drone. It continuously
    polls for the Worker Drone's GPS (embedded in the ELRS MAVLink stream), calculates
    the spatial midpoint, and commands the FC to move to that coordinate while respecting
    the 400ft AGL hard-deck.

HARDWARE CONTEXT:
    - Flight Controller: Matek H743-WLITE running ArduPilot
    - ELRS 900MHz RX on UART1 (Pilot uplink)
    - RadioMaster 2.4GHz Micro TX on UART2 (Worker downlink)
    - ArduPilot handles ELRS pass-through and strips telemetry for this brain

USAGE:
    pip install pymavlink
    python3 sentinel_relay_brain.py
"""

import time
import math
from pymavlink import mavutil

# ==============================================================================
# CONFIGURATION CONSTANTS
# ==============================================================================

# Connection string to the ArduPilot Flight Controller (UART/Serial)
FC_CONNECTION_STRING = '/dev/ttyAMA0'
FC_BAUD_RATE = 115200

# FAA Hard-deck limit (in meters, approx 400ft)
MAX_ALTITUDE_AGL = 120.0
# The minimum altitude the relay drone will descend to (in meters)
MIN_ALTITUDE_AGL = 50.0

# Pre-defined Pilot (Ground Station) Coordinates [Latitude, Longitude, Altitude MSL]
# In a fully dynamic system, this could also be updated via MAVLink from a
# ground-station telemetry radio or a second ELRS backpack.
PILOT_LOCATION = {
    'lat': 40.0000000,
    'lon': -75.0000000,
    'alt': 100.0  # meters MSL
}

# Update rate for the positioning loop (Hz)
LOOP_RATE_HZ = 1

# Altitude buffer above the highest endpoint (meters)
# Ensures the Relay has geometric clearance for LOS
ALTITUDE_BUFFER_M = 30.0


# ==============================================================================
# MAVLINK CONNECTION
# ==============================================================================

def connect_to_fc():
    """
    Establishes the MAVLink connection to the Flight Controller.
    Waits for the heartbeat to ensure the connection is active.

    Returns:
        mavutil.mavlink_connection: Active MAVLink connection object.
    """
    print(f"[SENTINEL] Connecting to Flight Controller on {FC_CONNECTION_STRING}...")
    master = mavutil.mavlink_connection(FC_CONNECTION_STRING, baud=FC_BAUD_RATE)
    master.wait_heartbeat()
    print(f"[SENTINEL] Heartbeat detected (system {master.target_system}, "
          f"component {master.target_component}). Connection established.")
    return master


# ==============================================================================
# TELEMETRY PARSING
# ==============================================================================

def get_worker_drone_gps(master):
    """
    Parses the incoming MAVLink stream to extract the Worker Drone's GPS position.

    In the cross-band ELRS setup, the Worker Drone's telemetry is received on the
    900MHz RX (UART1) and forwarded by ArduPilot to the companion computer's
    MAVLink stream.

    Args:
        master: Active MAVLink connection.

    Returns:
        dict or None: {'lat': float, 'lon': float, 'alt': float} in degrees and
                      meters MSL, or None if no fresh position data is available.
    """
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
    if msg:
        # MAVLink sends Lat/Lon as integers (degrees * 1E7)
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        # Altitude is in millimeters, convert to meters
        alt = msg.alt / 1000.0
        return {'lat': lat, 'lon': lon, 'alt': alt}
    return None


def get_relay_drone_position(master):
    """
    Gets the Relay Drone's own current GPS position from its flight controller.

    Returns:
        dict or None: {'lat': float, 'lon': float, 'alt': float, 'relative_alt': float}
    """
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
    if msg and msg.get_srcSystem() == master.target_system:
        return {
            'lat': msg.lat / 1e7,
            'lon': msg.lon / 1e7,
            'alt': msg.alt / 1000.0,
            'relative_alt': msg.relative_alt / 1000.0
        }
    return None


# ==============================================================================
# SPATIAL LOGIC (POSITIONING ENGINE)
# ==============================================================================

def haversine_distance(loc1, loc2):
    """
    Calculates the great-circle distance between two GPS coordinates in meters.

    Args:
        loc1, loc2: dicts with 'lat' and 'lon' keys (degrees).

    Returns:
        float: Distance in meters.
    """
    R = 6371000  # Earth's radius in meters
    lat1, lat2 = math.radians(loc1['lat']), math.radians(loc2['lat'])
    dlat = math.radians(loc2['lat'] - loc1['lat'])
    dlon = math.radians(loc2['lon'] - loc1['lon'])

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_optimal_relay_position(pilot_loc, worker_loc):
    """
    Calculates the optimal 3D spatial position for the Relay Drone between
    the Pilot and the Worker drone.

    CURRENT IMPLEMENTATION:
        Pure geometric midpoint with altitude clamping for LOS and FAA compliance.

    ADVANCED IMPLEMENTATION (Rule #6 — Terrain-Aware Logic):
        This is where the SRTM / Topographical database query would occur.
        You would:
        1. Load a localized SRTM .hgt tile covering the operational area.
        2. Sample elevation along the 3D vector from pilot_loc to worker_loc.
        3. If terrain intersects the LOS vector, calculate a vertical or lateral
           offset to restore pure Line-of-Sight.
        4. Ensure the adjusted position never exceeds MAX_ALTITUDE_AGL.

    Args:
        pilot_loc: dict with 'lat', 'lon', 'alt' (degrees, meters MSL).
        worker_loc: dict with 'lat', 'lon', 'alt' (degrees, meters MSL).

    Returns:
        dict: {'lat': float, 'lon': float, 'alt': float} — target position.
    """
    # Pure geographic midpoint
    target_lat = (pilot_loc['lat'] + worker_loc['lat']) / 2.0
    target_lon = (pilot_loc['lon'] + worker_loc['lon']) / 2.0

    # Calculate target altitude:
    #   - Start with the higher of the two endpoints + a buffer for clearance
    #   - Clamp to the FAA 400ft (120m) AGL hard-deck
    #   - Enforce minimum altitude for signal geometry
    target_alt = max(pilot_loc['alt'], worker_loc['alt']) + ALTITUDE_BUFFER_M
    target_alt = min(target_alt, pilot_loc['alt'] + MAX_ALTITUDE_AGL)
    target_alt = max(target_alt, pilot_loc['alt'] + MIN_ALTITUDE_AGL)

    return {'lat': target_lat, 'lon': target_lon, 'alt': target_alt}


# ==============================================================================
# FLIGHT COMMANDS
# ==============================================================================

def send_movement_command(master, target_loc):
    """
    Constructs and sends a SET_POSITION_TARGET_GLOBAL_INT MAVLink command.
    This tells ArduPilot (in Guided Mode) to autonomously fly to the calculated
    target coordinates.

    The type_mask is set to use ONLY position (lat/lon/alt), ignoring velocity
    and acceleration fields.

    Args:
        master: Active MAVLink connection.
        target_loc: dict with 'lat', 'lon', 'alt' keys.
    """
    master.mav.set_position_target_global_int_send(
        time_boot_ms=0,
        target_system=master.target_system,
        target_component=master.target_component,
        coordinate_frame=mavutil.mavlink.MAV_FRAME_GLOBAL_INT,
        type_mask=0b0000111111111000,  # Use position only; ignore vel/accel/yaw
        lat_int=int(target_loc['lat'] * 1e7),
        lon_int=int(target_loc['lon'] * 1e7),
        alt=target_loc['alt'],
        vx=0, vy=0, vz=0,
        afx=0, afy=0, afz=0,
        yaw=0, yaw_rate=0
    )
    print(f"[SENTINEL] CMD -> Lat: {target_loc['lat']:.7f}, "
          f"Lon: {target_loc['lon']:.7f}, Alt: {target_loc['alt']:.1f}m")


# ==============================================================================
# MAIN LOOP
# ==============================================================================

def main():
    """
    The main execution loop.

    Flow:
        1. Connect to the ArduPilot FC via MAVLink.
        2. Poll for the Worker Drone's GPS from the telemetry stream.
        3. Calculate the optimal relay position (midpoint with altitude logic).
        4. Send SET_POSITION_TARGET to fly the Relay Drone to that position.
        5. Repeat at LOOP_RATE_HZ (default 1 Hz) to avoid saturating the FC serial link.

    Exit:
        Ctrl+C triggers a clean shutdown.
    """
    master = connect_to_fc()

    print(f"[SENTINEL] Pilot station: Lat {PILOT_LOCATION['lat']:.7f}, "
          f"Lon {PILOT_LOCATION['lon']:.7f}, Alt {PILOT_LOCATION['alt']:.0f}m")
    print(f"[SENTINEL] Altitude limits: {MIN_ALTITUDE_AGL}m – {MAX_ALTITUDE_AGL}m AGL")
    print(f"[SENTINEL] Loop rate: {LOOP_RATE_HZ} Hz")
    print(f"[SENTINEL] Entering autonomous positioning loop...\n")

    loop_count = 0

    try:
        while True:
            worker_loc = get_worker_drone_gps(master)

            if worker_loc:
                loop_count += 1
                distance = haversine_distance(PILOT_LOCATION, worker_loc)

                print(f"[SENTINEL] [#{loop_count}] Worker at: "
                      f"Lat {worker_loc['lat']:.7f}, "
                      f"Lon {worker_loc['lon']:.7f}, "
                      f"Alt {worker_loc['alt']:.0f}m | "
                      f"Range: {distance:.0f}m")

                # Calculate the geographic logic
                optimal_target = calculate_optimal_relay_position(
                    PILOT_LOCATION, worker_loc
                )

                # Issue the command to ArduPilot
                send_movement_command(master, optimal_target)
            else:
                print("[SENTINEL] Waiting for Worker Drone telemetry...")

            # Loop runs at configured rate to prevent overwhelming the FC
            time.sleep(1.0 / LOOP_RATE_HZ)

    except KeyboardInterrupt:
        print("\n[SENTINEL] Manual override triggered. "
              "Terminating positioning logic. Relay Drone will hold last position.")


if __name__ == '__main__':
    main()
