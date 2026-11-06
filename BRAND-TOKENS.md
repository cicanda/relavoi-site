# Brand tokens

Every colour used by relavoi.com, the dashboard, the operator console and the
docs, derived from the six colours in the brand guidelines. Nothing here is
invented: each value is one of the six, or a mix of two of them.

    Ink         #0E1B2C   dark grounds and primary text
    Relay Teal  #0B7A6B   the brand: buttons, links, accents, teal on light
    Pulse Teal  #2CC5AE   accents on dark grounds ONLY
    Proxy Amber #F5A524   the proxy moment only
    Mist        #EEF3F2   light grounds
    Slate       #5B6B7A   secondary text

How the derived values are made:

- **Light tints** (`-100`, `-200`, `-50`) are mixed toward white in **linear
  light**, not on the gamma-encoded values. A plain hex mix of `#0B7A6B` with
  white reads muddy and uneven; in linear light the ramp is even, which matters
  because these sit behind text.
- **Dark steps** (`ink-600/700/800`) mix Ink toward **Slate**, not toward Mist.
  Mixing toward Mist desaturated them into greys that were lighter than Slate
  itself, which broke the ordering of the scale.
- **Marks and dark-ground text** (`-300`, `-dark`) are lightened in **HSL**,
  keeping hue and saturation. A linear mix to white pulls the chroma out and
  leaves a grey, which is right for a 5% tint and useless for a mark.

Two rules that are enforced by the token names rather than by discipline:

- **Pulse Teal is never text on white.** It is 2.16:1 there. It is 8.01:1 on
  Ink, which is where it belongs.
- **Proxy Amber is never a warning.** Every amber utility in these apps was a
  caution (cooldown, at-limit, pool utilisation, KYB pending), so those names
  now carry the **warning** scale, and Proxy Amber lives under `proxy-*` where
  nothing can reach it by accident.

Contrast is against white and against Ink. 4.5 is the AA floor for body text,
3.0 for large text and for user-interface parts.

| token | value | on white | on Ink |
|---|---|---|---|
| `amber-100` | `#FEF5EF` | 1.08 | 16.11 |
| `amber-200` | `#FCE9DB` | 1.18 | 14.70 |
| `amber-500` | `#F5A524` | 2.04 | 8.49 |
| `amber-700` | `#C6851B` | 3.10 | 5.59 |
| `amber-800` | `#976412` | 5.06 | 3.42 |
| `chart-a-to-b` | `#0B7A6B` | 5.24 | 3.31 |
| `chart-answered` | `#35A866` | 3.02 | 5.73 |
| `chart-axis` | `#5B6B7A` | 5.48 | 3.16 |
| `chart-b-to-a` | `#1F5FA6` | 6.47 | 2.68 |
| `chart-failed` | `#8E1E17` | 8.94 | 1.94 |
| `chart-grid` | `#ECEDEE` | 1.17 | 14.78 |
| `chart-missed` | `#B9651C` | 4.25 | 4.08 |
| `danger-100` | `#F6EFEF` | 1.13 | 15.28 |
| `danger-300` | `#CA463F` | 4.71 | 3.68 |
| `danger-500` | `#B3261E` | 6.54 | 2.65 |
| `danger-700` | `#A4221B` | 7.44 | 2.33 |
| `danger-dark` | `#D68985` | 2.70 | 6.42 |
| `info-100` | `#EFF1F5` | 1.13 | 15.32 |
| `info-300` | `#4181C8` | 4.04 | 4.29 |
| `info-500` | `#1F5FA6` | 6.47 | 2.68 |
| `info-700` | `#1B5698` | 7.42 | 2.34 |
| `info-dark` | `#86ABD5` | 2.39 | 7.26 |
| `ink-100` | `#EEF3F2` | 1.12 | 15.46 |
| `ink-200` | `#ECEDEE` | 1.17 | 14.78 |
| `ink-300` | `#D4D6D9` | 1.46 | 11.90 |
| `ink-400` | `#88919A` | 3.20 | 5.42 |
| `ink-50` | `#F8FAF9` | 1.05 | 16.53 |
| `ink-500` | `#5B6B7A` | 5.48 | 3.16 |
| `ink-600` | `#3E4B59` | 8.92 | 1.94 |
| `ink-700` | `#313D4A` | 11.07 | 1.57 |
| `ink-800` | `#25303E` | 13.37 | 1.30 |
| `ink-900` | `#0E1B2C` | 17.33 | 1.00 |
| `ink-950` | `#091321` | 18.64 | 1.08 |
| `paper` | `#FFFFFF` | 1.00 | 17.33 |
| `pulse-300` | `#1F8B7D` | 4.16 | 4.17 |
| `pulse-500` | `#2CC5AE` | 2.16 | 8.01 |
| `pulse-600` | `#28B8A3` | 2.48 | 6.99 |
| `relay-100` | `#EFF2F1` | 1.13 | 15.38 |
| `relay-200` | `#DDE4E2` | 1.29 | 13.43 |
| `relay-300` | `#33D6C0` | 1.82 | 9.51 |
| `relay-50` | `#F7F9F8` | 1.06 | 16.39 |
| `relay-500` | `#0B7A6B` | 5.24 | 3.31 |
| `relay-600` | `#0A7466` | 5.67 | 3.06 |
| `relay-700` | `#096E60` | 6.16 | 2.81 |
| `relay-800` | `#076458` | 7.06 | 2.45 |
| `relay-dark` | `#2CC5AE` | 2.16 | 8.01 |
| `success-100` | `#EFF2F0` | 1.13 | 15.37 |
| `success-300` | `#4ABF78` | 2.33 | 7.44 |
| `success-500` | `#1F7A43` | 5.35 | 3.24 |
| `success-700` | `#1B6F3D` | 6.20 | 2.80 |
| `success-dark` | `#8BCFA6` | 1.81 | 9.55 |
| `warning-100` | `#F4F0EF` | 1.13 | 15.31 |
| `warning-300` | `#D37D36` | 3.11 | 5.58 |
| `warning-500` | `#9A4F11` | 6.00 | 2.89 |
| `warning-700` | `#8D480F` | 6.85 | 2.53 |
| `warning-dark` | `#DBA980` | 2.10 | 8.25 |
