# 📝 Submission Guidelines & Verification Schema

All competitors must formally register and submit their final builds via GitHub. This ensures the 100% open-source nature of the bounty.

---

## 1. Applicant Registration Schema

Before submitting a final build, teams must declare their intent to compete by opening a `Registration Issue` on this repository with the following schema:

```markdown
**Team / Builder Name:** [e.g., Team Stratos]
**Base Frame/Chassis:** [e.g., Custom 3D Printed, Tarot 650]
**Control Link (Worker):** [e.g., ELRS 2.4GHz]
**Video Link:** [e.g., Walksnail Avatar HD]
**Companion Computer:** [e.g., Orange Pi Zero 3]

**Brief Approach Summary (2-3 sentences):**
[Explain how you plan to tackle the 1-hour hover and the cross-band interference.]
```

---

## 2. Verification Methodology (The Burden of Proof)

The judging panel will **not** evaluate your build conceptually. You must prove it works in the real world. 

### Proof of 1-Hour Hover
To score points for the 60-minute endurance requirement, you must provide:
1. **Uncut DVR Footage:** Showing the drone taking off, hovering for 60+ minutes, and landing. (Can be sped up in a YouTube video, but the full raw file must be linked).
2. **ArduPilot `.bin` Dataflash Logo:** The log must show the `BAT.Volt` and `BAT.Curr` dropping over a continuous 60-minute arming sequence. 

### Proof of Range Extension / Autonomy
To score points for the 2-Square-Mile coverage and topographical brain logic, you must provide:
1. **GPS Overlay DVR:** Walksnail DVR footage from the Worker Drone showing a clear video feed while the pilot is physically located behind a massive, signal-blocking obstacle. 
2. **Companion Computer Logs:** Terminal logs from your Python script proving the system issued dynamic `SET_POSITION_TARGET_GLOBAL_INT` commands to avoid terrain intersections based on SRTM data.

### Proof of Budget (The $2,000 Cap)
You must submit a fully itemized Bill of Materials with live URLs to the retail sites where you purchased the parts, proving the total cost of the airborne relay unit is under $2,000 USD. 

---

## 3. Final Submission GitHub Issue Template

When your build is flying and verified, open a `Final Submission Issue` using this exact template.

```markdown
# Final Submission: [Team Name]

## 1. Core Metrics
- **Flight Time Achieved:** [X] Minutes
- **Final BOM Cost:** $[X] USD
- **System Weight (AUW):** [X] Grams
- **Demonstrated Range:** [X] Miles

## 2. Link to Open-Source Repository
[Insert URL to YOUR fork containing all source code, CAD files, and STLs]

## 3. Proof of Flight (Video)
[Insert YouTube / Google Drive Links]
- Link 1: 60-Minute Hover Verification (Uncut)
- Link 2: Range Extension & Terrain Avoidance Demonstration

## 4. Hardware Verification
- [Link to your itemized BOM with pricing]
- [Link to your ArduPilot .bin Dataflash Log]

## 5. System Architecture Breakdown
*Provide a 2-paragraph summary explaining your power distribution, how you solved RF self-interference, and how your topographical Python brain functions.*
```
