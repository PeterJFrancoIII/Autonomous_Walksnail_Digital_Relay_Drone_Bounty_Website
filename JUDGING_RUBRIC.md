# ⚖️ Judging Rubric: Relay Drone Bounty

Every submission will be evaluated by the administrative panel across 9 core metrics. These metrics are a combination of hard quantitative data and qualitative design assessment.

## 📊 Quantitative Metrics (Hard Data)

| Metric                       | Goal                                                                                                                                                                                           | Description                                                                                                                                                                                                            | Max Points |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **1. Flight Time**     | ≥ 60 Minutes                                                                                                                                                                                  | The system must demonstrate a continuous hover under payload for at least one hour. Log files (voltage/current draw over time) must be submitted as proof.                                                             | 20         |
| **2. Cost**            | ≤ $2,000 USD | Total Bill of Materials (BOM) for the airborne relay module. Does not include pilot ground gear or the secondary worker drone. The further below $2,000, the higher the score. | 15                                                                                                                                                                                                                     |            |
| **3. Weight**          | Minimum Possible                                                                                                                                                                               | All-up weight (AUW) of the relay drone. Highly optimized (lightweight) builds that still hit the 1-hour margin will score highest.                                                                                     | 10         |
| **4. Range Extension** | 2 Sq Miles @ ≤15ft AGL                                                                                                                                                                        | The delta between the standard operational range (Pilot ↔ Worker) and the new relay range (Pilot ↔ Relay ↔ Worker). Video evidence must show a 2-square-mile coverage capability or equivalent penetration testing. | 15         |

---

## 🎨 Qualitative Metrics (Design & Execution)

| Metric                       | Description                                                                                                                                                        | Max Points |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| **5. Design Quality**  | Engineering elegance, clean wiring, thermal management of the RF payload, and structural integrity.                                                                | 10         |
| **6. Documentation**   | Completeness of the GitHub repository. Are the build guides clear? Are the schematics readable?                                                                    | 10         |
| **7. Replicability**   | How easily could a standard FPV hobbyist build this? Are the parts easily sourced or highly custom/exotic? Open-source 3D prints and common hardware score higher. | 10         |
| **8. Reliability**     | Field test stability. Does the Walksnail/ELRS link suffer from self-interference? Does the autonomous terrain logic correctly avoid obstacles?                     | 5          |
| **9. User Experience** | How intuitive is the final system to deploy? Does the companion computer boot cleanly? Is the manual override seamless?                                            | 5          |

---

## 🏆 Prize Distribution

The final score (out of 100) will determine the placement tiers. The actual cash value of the tiers scales dynamically with the Kickstarter crowdfunding pool.

**Minimum Funding Goal:** $20,000 USD. This target guarantees that even the 3rd Place winner recoups their entire $2,000 hardware budget.

1. **First Place (Grand Prize):** Highest overall score. (60% of Pool)
2. **Second Place (Innovator):** Runner-up. (20% of Pool)
3. **Third Place (Bronze):** Third highest score. (10% of Pool)
4. **VIP Contributors:** Awarded at the admin panel's discretion for exceptional individual contributions (e.g., a specific ELRS backpack mod, a computer vision script, or exceptional community help). (5% of Pool)
5. **Administrative Award:** Covers the costs and efforts of the judging panel and event organizers. (5% of Pool)
