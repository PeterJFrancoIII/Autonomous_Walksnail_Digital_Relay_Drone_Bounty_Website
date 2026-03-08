# 📦 Bill of Materials — Relay Drone Bounty Challenge

**Budget Cap:** $2,000 USD  
**Target Coverage Area:** 2 Square Miles  
**Target Endurance:** 1 Hour Minimum Hover  
**Key RF Links:** Walksnail Avatar HD (Video) & ExpressLRS (Control)  

---

To achieve the "unlimited practical range" required by this challenge, competitors must optimize primarily for endurance (grams per watt) without exceeding the aggressive $2,000 funding cap.

This document serves as a recommended baseline build demonstrating that hitting the requirements is mathematically possible.

## Airframe & Propulsion

The frame has to lift a heavy dual-band RF payload while remaining incredibly light to allow for massive Li-Ion battery reserves. 

| # | Component | Specific Part | Qty | Unit Cost | Total | Weight (est.) | Notes |
|---|-----------|---------------|-----|-----------|-------|---------------|-------|
| 1 | Frame | Tarot 650 Sport (or custom CF cross) | 1 | $160 | $160 | 550 g | 650mm class, clearance for 15"–17" props |
| 2 | Motors | T-Motor MN501S 360KV | 4 | $50 | $200 | 440 g | Low-KV pancake motors, high hover efficiency |
| 3 | ESCs | 35A BLHeli_32 (or 4-in-1) | 4 | $20 | $80 | 60 g | Dshot600, telemetry capable |
| 4 | Propellers | 16×5.4 Carbon Fiber Folding Props | 2 sets | $50 | $100 | 100 g | Large, slow-spinning = maximum efficiency |

**Propulsion Subtotal: $540 | ~1,150 g**

---

## Flight Controller, Navigation, and Autonomy

Per the challenge parameters, the system must utilize autonomous takeoff/landing and battery voltage monitoring for fail-safes. 

| # | Component | Specific Part | Qty | Unit Cost | Total | Weight (est.) | Notes |
|---|-----------|---------------|-----|-----------|-------|---------------|-------|
| 5 | Flight Controller | Matek H743-WLITE | 1 | $80 | $80 | 36 g | ArduPilot, ample UARTs, integrated BEC |
| 6 | GPS / Compass | Matek M10Q-5883 | 1 | $40 | $40 | 30 g | Matek M10 GNSS + QMC5883L compass |
| 7 | Remote ID Module | FAA-compliant broadcast module | 1 | $40 | $40 | 25 g | Wired to spare 5V pad on FC |

**Avionics Subtotal: $160 | ~91 g**

---

## Power System (The 1-Hour Secret)

For a 60-minute hover, Lithium-ion is non-negotiable. It provides vastly superior Wh/kg over LiPo racing packs.

| # | Component | Specific Part | Qty | Unit Cost | Total | Weight (est.) | Notes |
|---|-----------|---------------|-----|-----------|-------|---------------|-------|
| 8 | Battery Cells | Molicel INR21700-P45B | 30 | $7 | $210 | 2,100 g | 6S5P configuration: 22.2V, 22.5Ah, ~485 Wh |
| 9 | BMS / Balance Board | 6S Li-Ion BMS | 1 | $15 | $15 | 30 g | Cell balancing and protection |
| 10 | Spot Welder Materials | Nickel strip, solder, heatshrink | 1 | $25 | $25 | — | For pack construction |

**Power Subtotal: $250 | ~2,130 g**

---

## RF Payload (Bridging the Links)

This is the core payload that provides the "unlimited" FPV range to the worker drone.

| # | Component | Specific Part | Qty | Unit Cost | Total | Weight (est.) | Notes |
|---|-----------|---------------|-----|-----------|-------|---------------|-------|
| 11 | Video Repeater | Walksnail Avatar modules | 2 | $125 | $250 | 120 g | 5.8 GHz RX (from Worker), 5.2 GHz TX (to Pilot) |
| 12 | Control RX | ELRS 900MHz Receiver | 1 | $25 | $25 | 10 g | Wired to FC UART1 (Pilot uplink) |
| 13 | Control TX | RadioMaster 2.4GHz ELRS Micro TX | 1 | $40 | $40 | 20 g | Wired to FC UART2 (Worker downlink) |
| 14 | Video BEC | Dedicated 9V/12V BEC | 1 | $10 | $10 | 10 g | Isolated power for Walksnail, away from motor noise |

**RF Payload Subtotal: $325 | ~160 g**

---

## Companion Computer ("The Brain")

Needed for the high-level spatial positioning logic, calculating the 3D topographic midpoint from the ELRS MAVlink streams.

| # | Component | Specific Part | Qty | Unit Cost | Total | Weight (est.) | Notes |
|---|-----------|---------------|-----|-----------|-------|---------------|-------|
| 15 | Companion Computer | Orange Pi Zero 3 | 1 | $35 | $35 | 28 g | Full Linux/Python, MAVLink via UART |
| 16 | MicroSD Card | 32 GB Class 10 | 1 | $10 | $10 | 2 g | OS + SRTM elevation data |

**Compute Subtotal: $45 | ~30 g**

---

## Miscellaneous

| # | Component | Details | Qty | Unit Cost | Total | Weight (est.) |
|---|-----------|---------|-----|-----------|-------|---------------|
| 17 | Wiring | Silicone wire (12–18 AWG), XT60 connectors | 1 lot | $30 | $30 | 80 g |
| 18 | 3D Printed Parts | Motor mounts, antenna mounts, covers (PLA/PETG) | 1 lot | $15 | $15 | 60 g |
| 19 | Fasteners & Standoffs | M3 hardware, nylon standoffs, zip ties, heatshrink | 1 lot | $15 | $15 | 30 g |
| 20 | BECs | 5V BEC for FC/Pi, 9V BEC for Walksnail | 2 | $5 | $10 | 10 g |
| 21 | Vibration Dampening | Silicone grommets or foam for Pi & RF modules | 1 lot | $5 | $5 | 5 g |
| 22 | Antenna Pigtails & Adapters | SMA/U.FL pigtails for ELRS & Walksnail | 1 lot | $15 | $15 | 15 g |
| 23 | Heatsinks | Stick-on aluminum heatsinks for ESCs & Pi | 1 lot | $10 | $10 | 15 g |

**Misc Subtotal: $100 | ~215 g**

---

## Grand Total Summary

| Category | Cost | Weight |
|----------|------|--------|
| Airframe & Propulsion | $540 | 1,150 g |
| Avionics (FC, GPS, Remote ID) | $160 | 91 g |
| Power System (6S5P Li-Ion) | $250 | 2,130 g |
| RF Payload | $325 | 160 g |
| Companion Computer | $45 | 30 g |
| Miscellaneous | $100 | 215 g |
| **TOTAL** | **$1,420** | **3,776 g** |

---

### Endurance Estimate Validation

- **AUW (All-Up Weight):** 3.78 kg
- **Hover thrust per motor:** 945 g
- **Estimated Efficiency:** ~12 g/W with 16" props
- **Hover power per motor:** 945 ÷ 12 = ~79 W
- **Total hover power:** 79 × 4 = 316 W
- **Payload power:** ~20 W (Pi + ELRS + Walksnail + GPS + Remote ID)
- **Total system power draw:** ~336 W

- **Battery energy:** 486 Wh (30 x 16.2Wh P45B cells)
- **Gross flight time:** 486 ÷ 336 = 1.45 hrs = ~87 minutes

*With a 15% safety reserve, this reference build provides ~74 minutes of usable hover time, well past the 60-minute requirement, while leaving ~$580 of headroom in the $2,000 project budget.*
