# 🌐 BOUNTY: The Autonomous 1-Hour FPV Relay Challenge

> *"Imagine your FPV drone with truly unlimited practical range—no more dead zones, no more signal loss. We’re creating an autonomous relay drone, and with your support, we’ll unlock the skies. Pilots, help fund it; builders, help design it—so we all fly without limits."*

**Status:** 🟢 OPEN (Pending Crowdfunding Launch)
**License Requirement:** MIT / GPL (100% Open Source)
**Prize Pool:** Crowdfunded via Kickstarter

---

## 🎯 The Mission

When you fly an FPV drone behind a building or a mountain, the signal degrades rapidly or drops completely. But if we position a **Relay Drone** at 400 feet AGL (the maximum FAA limit), the signal degredation issues caused by line of sight object density issue vanishes. There is significantly less interference between you and the open airspace above the obstacle than there is trying to blast a signal *through* the obstacle on the ground level.

The goal of this community-driven bounty is to design, code, and document a **fully autonomous, sub-$2,000 relay drone system** that bridges the video and control link between a ground pilot and a worker FPV drone, effectively granting the worker drone **unlimited practical range** (target: 2 square miles of coverage).

This is a Kickstarter-style effort: Pilots who want this capability fund the prize pool; Builders with the engineering chops compete to solve the problem and claim the prize.

---

## 🛠️ Core Technical Specifications

To claim the prize, your submission must meet the following hardware and software constraints:

1. **The Cost Cap:** The relay drone cannot cost more than **$2,000 USD** to build.
2. **Endurance:** The relay drone must be capable of hovering for a minimum of **1 Hour (60 minutes)**.
3. **The RF Payload:**
   - **Video Relay:** Walksnail Avatar HD Digital System.
   - **Control Link:** ExpressLRS (ELRS).
4. **Autonomous Functions:**
   - Fully autonomous takeoff.
   - Fully autonomous landing.
   - Autonomous battery monitoring (to trigger Auto-RTH/Landing).
5. **Manual Override:** The pilot must be able to manually take over the relay drone and guide it back home if the autonomous systems fail.
6. **Geospatial & Topographical Logic (The "Brain"):**
   - The relay drone must constantly calculate and position itself in the optimal 3D location between the Pilot and the Worker drone.
   - It requires topographical awareness (3D mapping data) to understand where it is based on GPS, and where it must go to avoid predefined obstacles.
   - *(Bonus/Optional)*: Real-time Computer Vision for active obstacle avoidance.
7. **100% Open Source:** All source code, CAD files, schematics, and configuration files must be public and easily replicable by the community.

---

## 🏆 The Prize Tiers & Judging Criteria

This bounty is judged by an administrative panel. The total prize pool scales with the crowdfunding effort.

**Minimum Funding Goal:** $20,000 USD. This target guarantees that even the 3rd Place winner recoups their entire $2,000 hardware budget.

* **🥇 1st Place:** The Grand Prize for the highest-scoring overall system. (60%)
* **🥈 2nd Place:** Runner-up prize for high innovation or excellent subsystems. (20%)
* **🥉 3rd Place:** Bronze tier reward. (10%)
* **🌟 VIP Contributors:** "Thank you for entering" prizes distributed to teams documenting the best individual mods, fixes, or community support efforts. (5%)
* **🛡️ Administrative Award:** Covers the costs and efforts of the judging panel and event organizers. (5%)

### The Scoring Matrix

The judging panel will evaluate all completed submissions based on the following 9 metrics:

**Quantitative Metrics:**

1. **Flight Time:** Did it hit or exceed the 1-hour requirement?
2. **Cost:** How far under the $2,000 budget is the final BOM?
3. **Weight:** Is the system footprint elegant and optimized?
4. **Range Extension:** What is the maximum demonstrated range increase compared to testing the FPV drone locally with standard ground equipment?

**Qualitative Metrics:**
5. **Design Quality:** Engineering elegance and hardware integration.
6. **Documentation Completeness:** How thorough are the build guides and wiring diagrams?
7. **Ease of Replication:** How easily can a standard FPV hobbyist source parts and replicate your build?
8. **Real-World Reliability:** How stable is the RF link and autonomous logic in varied field conditions?
9. **User Experience:** How intuitive and polished does the final system feel to operate for the end-user?

---

## 🚀 How to Participate

### For Pilots (The Backers)

Wait for the Kickstarter campaign link to go live. Your contributions directly fund the prize pool and incentivize the world's best open-source builders to solve this problem for the entire community.

### For Builders (The Competitors)

1. Fork this repository.
2. Read the [HINTS_AND_TIPS.md](docs/HINTS_AND_TIPS.md) and [BOM.md](docs/BOM.md) to understand the endurance and RF challenges.
3. Begin prototyping. Keep your testing logs, schematics, and source code strictly documented on GitHub.
4. Final submission procedures will be announced alongside the crowdfunding launch.

---

### Project Architecture & Links

*(Links to be populated as the repository grows)*

- [Technical Specifications &amp; Rules](docs/SPECIFICATIONS.md)
- [Judging Rubric Details](docs/JUDGING_RUBRIC.md)
- [Recommended Hardware / BOM](docs/BOM.md)
- [Relay Brain Source Code](src/)
