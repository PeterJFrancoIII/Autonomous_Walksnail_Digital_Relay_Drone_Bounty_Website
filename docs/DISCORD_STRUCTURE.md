# 💬 Discord Community Layout: The Overwatch Network

Because this relies on crowdsourcing the brightest hardware hackers in the world, the community Discord Server is the most critical piece of infrastructure outside of the GitHub repo itself.

The server is designed to foster **open-source collaboration**. Teams will compete, but they will also share solutions to the hardest physics problems. 

*(5% of the total Prize Pool is allocated explicitly to reward individuals who provide the best fixes, mods, and support in this server).*

---

## 🔒 Roles Structure

- **@Admin / Judge:** Organizers and final evaluators.
- **@Builder:** Users who have submitted a formal `Registration Issue` on GitHub.
- **@Backer:** Users who helped fund the Kickstarter (synced via Discord integration).
- **@Spectator:** General FPV enthusiasts hanging out.

---

## 📁 Channel Categories & Layout

### 📢 INFORMATION
- `#welcome` — Rules and onboarding.
- `#announcements` — Official updates from the judges.
- `#bounty-rules` — Links to the live GitHub README, Rubric, and Constraints.
- `#live-funding-tracker` — A read-only channel where a bot posts real-time updates from our Django backend whenever a new donation clears.

### 🛠️ COMPETITOR WORKSHOPS (The Meat of the Server)
This is where the engineering happens.

- `#general-hardware` — General discussion on frames, motors, and props.
- `#energy-and-batteries` — 1-hour hover math, Molicel P45B spot-welding advice, and BMS discussion.
- `#rf-interference-hell` — The hardest part of the bounty. Discussing how to mount ELRS 900MHz, ELRS 2.4GHz, Walksnail 5.8RX, and Walksnail 5.2TX on the same rig without blocking GPS.
- `#python-and-math` — Companion computer discussion. Passing MAVLink telemetry, Ray-tracing, and SRTM elevation logic.
- `#ardupilot-tuning` — PID tuning a massive 16-inch rig to hover perfectly steady.

### 🧪 FLIGHT TESTING & VERIFICATION
- `#test-flights` — Builders posting their DVR footage and log files for community review.
- `#crashes-and-carnage` — It happens. Post the charred ESCs here.

### 💰 CROWDFUNDING & SUPPORT
- `#backer-chat` — A place for the pilots funding the bounty to chat with the engineers building it.
- `#vip-nominations` — See someone drop an incredible 3D printed Walksnail mount? Nominate them here for a cut of the 5% VIP Prize Pool.

---

## 🤖 Required Discord Bots

1. **GitHub Notifier Bot:** Pushes a notification to an `#updates` channel whenever a new PR is merged or a new `Registration Issue` is opened.
2. **Kickstarter/Stripe Bot:** Reads the `/api/bounty/live-stats/` endpoint from our Django server to update the #live-funding-tracker channel dynamically.
3. **Role Management Bot:** Manages the `@Backer` tag for users who verify their Kickstarter email.
