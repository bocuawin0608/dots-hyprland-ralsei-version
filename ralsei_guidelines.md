# RALSEI OS — RALSEI DESIGN IDENTITY OVERRIDE

This project is NOT a generic Linux rice.

This project is a **Ralsei-themed personal desktop environment**.

The identity of the entire system must be built around **Ralsei from Deltarune**.

Do NOT treat Ralsei as a wallpaper pasted onto an otherwise generic desktop.

Ralsei is the **visual, emotional, and interaction design inspiration** for the entire system.

---

# 1. CORE IDENTITY

The final desktop should immediately communicate:

```text
Ralsei
+
Dark fantasy
+
Soft magical atmosphere
+
Green magic
+
Cozy darkness
+
Gentle personality
+
Clean modern UI
+
Deltarune-inspired visual language
```

The system should feel like:

> a modern Linux desktop designed inside Ralsei's world.

NOT:

```text
generic dotfiles
+
green accent
+
Ralsei wallpaper
```

That is insufficient.

---

# 2. RALSEI DESIGN LANGUAGE

The design language should draw inspiration from:

```text
Ralsei's green scarf
Ralsei's hat
Ralsei's dark robe
soft green magic
Dark World atmosphere
Deltarune UI
pixel-art influence
storybook fantasy
cozy interiors
magical interfaces
```

Translate those concepts into a modern desktop UI.

Do not blindly reproduce game UI.

The result should be an **original desktop interface inspired by Ralsei**.

---

# 3. COLOR IDENTITY

The primary visual identity should be based around Ralsei's characteristic palette.

Conceptually:

```text
Dark Forest
Deep Green
Soft Emerald
Mint
Warm Cream
Dark Purple
Black
Muted Gray
```

However:

## IMPORTANT

The wallpaper-driven Material 3 system remains authoritative.

The Ralsei identity should influence the **palette generation strategy**, while Matugen dynamically adapts the actual colors to the wallpaper.

Conceptually:

```text
RALSEI BASE IDENTITY
        +
WALLPAPER
        ↓
MATUGEN
        ↓
MATERIAL 3 PALETTE
        ↓
RALSEI OS THEME
```

Therefore:

* dark wallpapers should produce deep magical themes
* green wallpapers should produce stronger Ralsei-like palettes
* purple wallpapers should produce Dark World-like palettes
* bright wallpapers should still maintain readable dark surfaces
* random wallpapers must not destroy the Ralsei identity

The theme must remain recognizably Ralsei-inspired even when the wallpaper changes.

---

# 4. SEMANTIC THEME TOKENS

Do NOT hardcode Ralsei colors into individual components.

Create semantic tokens.

For example:

```text
ralseiBackground
ralseiSurface
ralseiSurfaceElevated
ralseiPrimary
ralseiSecondary
ralseiAccent
ralseiMagic
ralseiCream
ralseiOutline
ralseiText
ralseiTextMuted
ralseiSuccess
ralseiWarning
ralseiError
```

Use the project's existing theme architecture where possible.

Do not blindly create these exact names if the existing repository has a better naming convention.

The principle is:

```text
centralized semantic theme
```

not:

```text
Ralsei green #XXYYZZ
```

copied into 70 files.

---

# 5. VISUAL MATERIALS

The UI should use layered surfaces inspired by:

```text
dark cloth
soft magical glass
polished stone
paper
storybook panels
```

Translate these into:

```text
Material 3 surfaces
controlled transparency
soft blur
subtle borders
soft shadows
depth layers
```

Avoid excessive glassmorphism.

The desktop should feel:

```text
soft
warm
magical
dark
cozy
```

rather than:

```text
cyberpunk
neon
aggressive
corporate
```

---

# 6. RALSEI MAGIC EFFECT

Introduce a subtle visual concept called the:

```text
MAGIC LAYER
```

This is the visual language for active/important UI states.

Examples:

```text
focused window
selected workspace
active button
AI interaction
media playback
subtitle mode
notification
system activity
```

The Magic Layer may use:

```text
soft green glow
subtle particles
gradient
blur
light bloom
animated accent
```

Do NOT use particles everywhere.

Magic should be **rare and meaningful**.

---

# 7. WORKSPACE DESIGN

Workspaces should have a Ralsei-inspired identity.

Possible visual language:

```text
green magical indicators
soft glowing selection
storybook-like workspace cards
dark surfaces
subtle scarf/cloth-inspired curves
```

The active workspace should feel like:

```text
"this is where Ralsei currently is"
```

rather than a generic numbered workspace indicator.

Workspace indicators must remain functional and readable.

---

# 8. TOP BAR

The top bar should resemble a magical status ribbon.

Visual characteristics:

```text
dark surface
soft green accent
subtle glow
rounded geometry
clean typography
small magical details
```

Possible sections:

```text
Ralsei OS identity
workspace
active window
system status
clock
notifications
AI
```

Do not overload it.

---

# 9. BOTTOM BAR

The bottom bar should feel like Ralsei's magical control panel.

Possible components:

```text
launcher
workspace controls
media
system controls
AI
applications
```

Use a visually coherent surface.

Avoid making it look like a Windows taskbar clone.

---

# 10. OVERVIEW

The Overview should be one of the strongest expressions of the theme.

When entering Overview:

```text
desktop
 ↓
dark magical transition
 ↓
workspace/window overview
```

Use:

```text
soft depth
subtle green glow
smooth zoom
dark surfaces
window cards
```

Window cards should feel like magical panels.

Active/focused windows may receive a subtle Magic Layer.

---

# 11. LAUNCHER

The launcher should feel like a magical spellbook/search interface.

Concept:

```text
             ┌─────────────────────┐
             │  What shall we do?  │
             ├─────────────────────┤
             │ Firefox             │
             │ Terminal            │
             │ Code                │
             │ Settings            │
             └─────────────────────┘
```

Do not literally force fantasy text everywhere.

The interface should remain practical.

Use Ralsei-inspired visual styling rather than turning every label into roleplay.

---

# 12. AI PANEL

The AI panel should feel like a magical assistant.

Visual identity:

```text
dark magical surface
green accent
soft glow
storybook-like conversation bubbles
```

Gemini and Ollama should be represented as providers.

Do not invent fake Ralsei AI responses.

The UI is Ralsei-themed.

The underlying AI providers remain real.

---

# 13. WALLPAPER

The wallpaper system should prioritize Ralsei-themed wallpapers.

Support:

```text
Ralsei artwork
Dark World environments
green magical scenes
dark fantasy landscapes
cozy fantasy environments
```

The wallpaper selector should have a dedicated:

```text
RALSEI
```

category.

But do NOT hardcode internet URLs.

Use local assets or user-provided wallpaper directories.

---

# 14. WALLPAPER SELECTION EXPERIENCE

When selecting a wallpaper:

```text
preview
 ↓
apply
 ↓
Matugen
 ↓
theme transition
```

The UI should animate the palette transition.

Avoid abruptly changing 50 colors at once.

The theme should transition smoothly.

---

# 15. CAVA

Cava should visually represent:

```text
Ralsei's magic
```

rather than looking like a generic audio visualizer.

Use:

```text
green
mint
cream
dynamic wallpaper-derived colors
```

with the central theme system.

Possible animation:

```text
soft magical bars
```

rather than aggressive neon equalizer styling.

---

# 16. SUBTITLE SYSTEM

The YouTube subtitle overlay should use a Ralsei-inspired visual treatment.

Example visual language:

```text
soft cream text
dark translucent magical panel
green accent
subtle glow
rounded corners
```

The subtitle should remain highly readable.

Do NOT sacrifice readability for aesthetics.

---

# 17. MUSIC-REACTIVE SUBTITLE MODE

When:

```text
Ctrl + Shift + Y
```

is activated on an empty workspace:

```text
subtitle mode
```

should become a special Ralsei-themed visual mode.

The subtitle animation can react to music using:

```text
scale
glow
vertical movement
soft wave
opacity
particle-like accents
```

The animation should resemble:

```text
magic responding to music
```

rather than a generic audio spectrum.

Keep the actual subtitle readable.

---

# 18. RALSEI MAGIC STATES

Create consistent visual states.

### Idle

```text
quiet
soft
dark
minimal
```

### Hover

```text
small green glow
subtle elevation
```

### Focus

```text
stronger magical accent
```

### Active

```text
green/mint illumination
```

### Loading

```text
soft magical pulse
```

### Error

Do NOT use bright aggressive red everywhere.

Prefer:

```text
dark surface
warm red accent
controlled glow
```

### Success

```text
soft green/mint glow
```

---

# 19. RALSEI ICONOGRAPHY

Prefer iconography that feels:

```text
soft
rounded
friendly
magical
simple
```

Avoid:

```text
aggressive
military
cyberpunk
sharp futuristic
```

Use a consistent icon family.

Do not mix random icon packs.

---

# 20. TYPOGRAPHY

Typography should balance:

```text
modern UI
+
storybook/fantasy atmosphere
```

Primary UI text must remain extremely readable.

Use decorative typography only for:

```text
branding
large headings
special overlays
```

Do NOT use decorative fonts for:

```text
system status
terminal
configuration
dense information
```

---

# 21. RALSEI BRANDING

The desktop may contain subtle branding such as:

```text
RALSEI OS
Ralsei
magic
```

But branding must remain subtle.

Do not put:

```text
RALSEI
```

in every corner of the screen.

The theme should communicate the identity without constantly announcing it.

---

# 22. RALSEI CHARACTER ART

Character artwork should be treated as an asset layer.

Recommended structure:

```text
assets/
└── ralsei/
    ├── wallpapers/
    ├── icons/
    ├── overlays/
    ├── illustrations/
    └── security/
```

Do not embed huge images directly inside QML.

Use optimized assets.

Prefer WebP/AVIF/appropriately compressed formats where supported.

---

# 23. CHARACTER ART PERFORMANCE

Never continuously render giant high-resolution character artwork.

Use:

```text
lazy loading
appropriate resolution
texture reuse
asset caching
```

If the image is not visible:

```text
do not keep expensive rendering active unnecessarily
```

---

# 24. SECURITY DETERRENT

The failed-password deterrent should fit the Ralsei theme.

After three failed authentication attempts:

```text
authentication failure
 ↓
Ralsei-themed security screen
 ↓
configured furry/femboy image
 ↓
desktop remains locked
 ↓
5-minute cooldown
```

The visual should be surprising/funny but must remain technically safe.

Do NOT replace real authentication.

Do NOT store passwords.

Do NOT weaken PAM.

---

# 25. ANTI-FLASHBANG RALSEI MODE

The anti-flashbang system should preserve the dark magical atmosphere.

When an extremely bright application appears:

```text
bright window detected
 ↓
soft transition
 ↓
controlled visual mitigation
```

Avoid suddenly displaying a full-screen black overlay.

Use subtle compositor/UI behavior where technically possible.

---

# 26. DARK WORLD ATMOSPHERE

The default desktop should feel like a calm Dark World environment.

Visual hierarchy:

```text
dark background
 ↓
deep surface
 ↓
soft elevated surface
 ↓
green magical accent
 ↓
cream readable text
```

This should be the default visual hierarchy.

---

# 27. COZY MODE

Provide an optional visual state:

```text
COZY MODE
```

This may reduce:

```text
brightness
animation intensity
visual noise
```

while increasing:

```text
warmth
softness
ambient glow
```

Do not add the mode unless it integrates naturally with the existing architecture.

---

# 28. RALSEI PERSONALITY WITHOUT ROLEPLAY

The UI can communicate personality through:

```text
friendly microcopy
soft visual feedback
gentle animations
cozy design
```

But do NOT turn every system message into roleplay.

Bad:

```text
"Ralsei is casting the volume spell!"
```

Good:

```text
Volume
```

The theme should come from design, not forced dialogue.

---

# 29. RALSEI + MATERIAL 3

The design must combine:

```text
Material Design 3
+
Ralsei visual identity
+
dynamic wallpaper palette
```

Do not choose one and ignore the others.

The final hierarchy:

```text
Material 3
    ↓
Design system
    ↓
Ralsei identity
    ↓
Wallpaper adaptation
    ↓
Component styling
```

---

# 30. RALSEI + PERFORMANCE

The Ralsei identity must NOT justify poor performance.

Never use:

```text
"it's Ralsei-themed, therefore it needs 15 layers of blur"
```

Instead:

```text
Ralsei atmosphere
+
efficient rendering
```

Use:

```text
GPU-accelerated rendering
cached effects
limited blur layers
controlled animations
lazy loading
```

The desktop must feel magical without turning the GPU into a space heater.

---

# 31. RALSEI DESIGN CONSISTENCY TEST

After implementation, inspect the entire desktop.

Ask:

```text
Does this look like Ralsei OS?

Does the palette feel coherent?

Does the UI feel magical?

Does it remain readable?

Does the wallpaper influence the UI?

Does Cava belong to the same world?

Does the subtitle overlay belong to the same world?

Does the AI panel belong to the same world?

Do the bars belong to the same world?

Does Overview belong to the same world?

Does the launcher belong to the same world?

Do animations belong to the same world?
```

If a component looks like it came from a completely different dotfile:

```text
redesign it.
```

---

# 32. FINAL VISUAL OBJECTIVE

The finished system should evoke:

```text
Ralsei
Dark World
Green Magic
Cozy Fantasy
Material You
Modern Linux
```

simultaneously.

The target is:

```text
                 RALSEI
                    │
             ┌──────┴──────┐
             │             │
          MAGIC         COZY
             │             │
             └──────┬──────┘
                    │
               MATERIAL 3
                    │
               QUICKSHELL
                    │
                HYPRLAND
```

The desktop should feel like a **single authored product**, not a pile of independent features.

---

# FINAL RULE

If a design decision conflicts between:

```text
generic modern UI
```

and:

```text
Ralsei-inspired UI
```

prefer the Ralsei-inspired direction **provided that functionality, readability, performance, accessibility, and maintainability remain intact**.

Do not make the UI childish merely because it is Ralsei-themed.

Do not make it neon merely because it is fantasy-themed.

Do not make it visually noisy merely because it has many effects.

Make it:

```text
soft
dark
magical
green
cozy
elegant
responsive
modern
```

The user should be able to look at the desktop for one second and know:

> **This is Ralsei OS.**
