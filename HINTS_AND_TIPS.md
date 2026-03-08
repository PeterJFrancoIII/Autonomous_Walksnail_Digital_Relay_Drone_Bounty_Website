# 💡 Engineering Hints & Tips

This document provides technical guidance for solving the core challenges of the Relay Drone Bounty: a 60-minute hover, a sub-$2k budget, and cross-band RF payload integration.

---

## 1. The 1-Hour Energy Physics

To hit 60 minutes, you must maximize **Watt-hours per gram**. 

* **Use Lithium-Ion (21700 cells), not LiPo.** A 6S5P pack of Molicel P45B cells provides ~485 Wh of energy at ~2.1 kg. LiPo equivalent would weigh nearly 3.5 kg.
* **Large, Slow Props.** 15" to 17" propellers paired with low KV (300-400 KV) pancake motors are the absolute sweet spot for hover efficiency. You should target ~12 grams of thrust per watt (g/W).

## 2. RF Self-Interference

You are mounting three to four active radios on the same airframe:
1. Walksnail Avatar Receiver (5.8 GHz)
2. Walksnail Avatar Transmitter (5.2 GHz)
3. ExpressLRS Receiver (900 MHz)
4. ExpressLRS Transmitter (2.4 GHz)

* **Physical Separation:** Place the 900 MHz RX antenna on one arm, and the 2.4 GHz TX antenna on the opposite arm.
* **Orientation:** Point directional RF antennas straight down towards the ground (where the Pilot and Worker drone exist).
* **GPS Placement:** Keep the GPS/Compass stalk as high and as far away from the video transmitters as possible to avoid GPS lock failure.

## 3. The Cross-Band Control Loop

ArduPilot on the Flight Controller (e.g., Matek H743) must sit in the middle of the control loop.

```
Pilot Radio (900 MHz TX) --> Relay Drone (900 MHz RX on UART1) --> ArduPilot (Pass-through) --> Relay Drone (2.4 GHz TX on UART2) --> Worker Drone (2.4 GHz RX)
```

ArduPilot must strip the MAVlink telemetry data coming back from the Worker Drone and pass it to the Companion Computer ("The Brain").

## 4. Topographical Logic (The Brain)

Relying on simple line-of-sight math isn't enough. If a mountain is between the Pilot and the Worker drone, the relay drone must know to fly *higher* or laterally to maintain LOS over the obstacle, while remaining under the 400ft FAA hard deck.

* Use a lightweight companion computer like the **Orange Pi Zero 3** running Linux.
* Pre-load an **SRTM (Shuttle Radar Topography Mission) digital elevation map** of the test area onto the Pi's MicroSD card.
* Write a Python script that calculates the 3D ray-trace between Pilot GPS and Worker GPS. If the ray intersects an SRTM elevation point, issue a `SET_POSITION_TARGET_GLOBAL_INT` command to move the Relay drone.
