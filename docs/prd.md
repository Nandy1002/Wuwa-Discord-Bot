# PRD — Shorekeeper Inspired Wuthering Waves Build Guide Discord Bot

## Project Name

**Shorelia** *(working title)*

---

# Overview

A stylish Discord bot focused on providing high-quality Wuthering Waves character build guides, Echo recommendations, team compositions, and optimization help inside Discord.

The bot should feel:

* elegant
* responsive
* anime/WuWa themed
* visually polished
* easy to use

The goal is NOT to become a bloated wiki bot.

The goal is:

> Fast, beautiful, practical build guidance.

---

# Core Concept

Users can instantly retrieve optimized character builds using:

```bash id="3b1s8l"
!build <character_name>
```

Example:

```bash id="8sn4zi"
!build hiyuki
```

The bot returns:

* Character image/banner
* Echo recommendations
* Main stats
* Substats priority
* Weapon rankings
* Skill priority
* Team compositions
* Styled embed UI

---

# Primary Features

## 1. Character Build Command

### Command

```bash id="5ukjlwm"
!build <character>
```

### Example

```bash id="0hw3b7"
!build hiyuki
```

### Output

A highly styled Discord embed containing:

---

## Embed Structure

### Header

* Character Name
* Element Icon
* Weapon Type
* Character Splash Art

Example:

```txt id="cpxndg"
❄️ Hiyuki — Glacio | Broadblade
```

---

## Echo Section

### Best Set

```txt id="z4e7mr"
Wishes of Quiet Snowfall (5pc)
```

### Recommended Layout

```txt id="1c12va"
4 Cost:
Reminiscence: Threnodian - Voidborne Construct
(Crit Rate / Crit DMG)

3 Cost:
Glacio DMG / ATK%

3 Cost:
Glacio DMG / ATK%

1 Cost:
ATK%

1 Cost:
ATK%
```

### Alternate Set

```txt id="q5vjlwm"
Freezing Frost (5pc)
```

---

## Substats Priority

Use visual ranking style:

```txt id="d6k0gq"
💠 Crit Rate / Crit DMG
💠 Energy Regen
💠 Resonance Liberation DMG
💠 ATK%
💠 Flat ATK
```

---

## Weapons Section

### Best Weapons

```txt id="7e9qv9"
🥇 Frostburn
🥈 Emerald of Genesis
🥉 Red Spring
```

### F2P Weapons

```txt id="w1ef8q"
⭐ Somnoire Anchor
⭐ Feather Edge
⭐ Fables of Wisdom
⭐ Commando of Conviction
```

---

## Forte Priority

Visual style:

```txt id="9o2vkj"
★★★★★ Normal Attack
★★★★★ Resonance Liberation
★★★★☆ Forte Circuit
★★★☆☆ Resonance Skill
★★☆☆☆ Intro Skill
```

---

## Team Compositions

```txt id="mpgrtb"
🏆 Hiyuki • Lynae • Chisa
(Best Team)

🆓 Hiyuki • Jianxin • Baizhi
(F2P Team)

⚡ Hiyuki • Zhizhi • Shorekeeper
(Second Best Team)
```

---

# Visual Design Goals

The bot should NOT feel like plain text.

## Use:

* Rich embeds
* Character thumbnails
* Accent colors by element
* Emojis/icons
* Section dividers
* Clean spacing
* Optional buttons/dropdowns later

---

# Embed Theme Colors

| Element | Color    |
| ------- | -------- |
| Glacio  | Ice Blue |
| Fusion  | Crimson  |
| Aero    | Green    |
| Electro | Purple   |
| Havoc   | Dark Red |
| Spectro | Gold     |

---

# Data Structure

Initially use JSON files.

---

## Example Structure

```bash id="o9y8ra"
data/
└── characters/
    ├── hiyuki.json
    ├── jinhsi.json
    ├── changli.json
```

---

## Example JSON Format

```json id="3u2rvj"
{
  "name": "Hiyuki",
  "element": "Glacio",
  "weapon_type": "Broadblade",
  "color": 5814783,

  "best_set": {
    "name": "Wishes of Quiet Snowfall",
    "pieces": [
      "4 - Crit Rate/Crit DMG",
      "3 - Glacio DMG/ATK%",
      "3 - Glacio DMG/ATK%",
      "1 - ATK%",
      "1 - ATK%"
    ]
  },

  "substats": [
    "Crit Rate/Crit DMG",
    "Energy Regen",
    "Resonance Liberation DMG",
    "ATK%",
    "Flat ATK"
  ],

  "weapons": {
    "best": [
      "Frostburn",
      "Emerald Of Genesis",
      "Red Spring"
    ],
    "f2p": [
      "Somnoire Anchor",
      "Feather Edge",
      "Fables of Wisdom"
    ]
  },

  "forte_priority": [
    "★★★★★ Normal Attack",
    "★★★★★ Resonance Liberation",
    "★★★★☆ Forte Circuit"
  ],

  "teams": [
    {
      "type": "Best Team",
      "members": "Hiyuki - Lynae - Chisa"
    }
  ]
}
```

---

# Recommended Tech Stack

| Purpose         | Technology          |
| --------------- | ------------------- |
| Bot Framework   | Python + discord.py |
| Data Storage    | JSON                |
| Future Database | SQLite              |
| Hosting         | Railway / Render    |
| Image Assets    | Local assets folder |

---

# Folder Structure

```bash id="l7zy0m"
shorelia/
│
├── assets/
│   ├── characters/
│   ├── icons/
│
├── data/
│   ├── characters/
│
├── cogs/
│   ├── build.py
│
├── utils/
│
├── .env
└── main.py
```

---

# Future Features

## Phase 2

* Slash commands
* Autocomplete
* Buttons/dropdowns
* Pagination

---

## Phase 3

* Echo scoring system
* Damage calculators
* Team recommendation AI
* OCR screenshot scanning

---

## Phase 4

* Website integration
* User profiles
* Build sharing
* Meta ranking system

---

# Success Criteria

The bot should:

* feel premium
* load fast
* look visually clean
* give practical information
* avoid clutter
* scale easily with new characters

---

# Main Differentiator

Most WuWa bots:

* dump walls of text
* have poor UI
* feel outdated

This bot should feel:

> like an in-game assistant character.
