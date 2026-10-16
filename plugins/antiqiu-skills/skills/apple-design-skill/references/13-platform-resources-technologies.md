# Platform, Resources, and Technologies Extraction

This file combines Apple platform adaptation, Apple Design Resources, and HIG Technologies. Use it when a task mentions a platform, official Apple resource, brand-sensitive capability, or system technology.

The skill is for cross-platform Apple design reference. Apple-only platforms and technologies must be treated as inspiration or compliance targets, not as UI to clone outside their native context.

## 1. Platform adaptation matrix

| Platform reference | Cross-platform value | Use for | Do not use for | Motion posture |
|---|---|---|---|---|
| iOS | High | Phone-first Web/mobile flows, touch targets, nav stacks, tab bars, sheets | Desktop density or keyboard-heavy enterprise apps | short, direct, reach-aware |
| iPadOS | High | Tablet/desktop hybrids, split views, sidebars, toolbars, drag/drop | Phone-only flows or tiny screens | context-preserving |
| macOS | High | Desktop Web apps, admin systems, data tools, sidebars, inspectors | Simple consumer mobile pages | restrained, expert-friendly |
| Apple.com marketing | High for landing pages | Product storytelling, scroll chapters, hero sections | Dense app workflows | cinematic but purposeful |
| watchOS | Low / scenario inspiration | Glanceable widgets, compact status chips, dashboard micro-cards | Full app UI, desktop/mobile page structure | tiny, immediate |
| tvOS | Low / scenario inspiration | TV, kiosk, remote-control, keyboard focus grids | Pointer/touch-first layouts without focus-grid needs | focus parallax only on active item |
| visionOS | Low / scenario inspiration; Apple-only for native visionOS | Spatial/layered demos, depth comfort, material hierarchy | Generic Web pages pretending to be spatial OS | comfortable, depth-aware |
| CarPlay | Low / safety constraint model; Apple-only for CarPlay | Driving/field/kiosk low-distraction constraints | General app navigation or decorative style | minimal, non-distracting |

## 2. Applicability rules

- **High-value cross-platform references**: iOS, iPadOS, macOS, Apple.com marketing. Use them as primary models when the target screen/input/task matches.
- **Scenario inspiration only**: watchOS, tvOS, visionOS, CarPlay. Extract constraints such as glanceability, focus predictability, motion comfort, and low distraction. Do not copy the surface UI unless the target platform actually matches.
- **Apple-only resources/technologies**: SF Symbols, Product Bezels, Apple Fonts, Apple Pay, Sign in with Apple, Wallet, HealthKit, Live Activities, Dynamic Island, Digital Crown, Eyes. Use only with platform support, license compliance, or neutral fallback.
- When in doubt, write down the transferable principle and a cross-platform fallback before implementing the Apple-specific treatment.

## 3. Platform rules

### iOS

- Prefer one clear path per screen.
- Keep primary actions reachable.
- Use tab bars for stable top-level destinations.
- Use sheets for scoped tasks.
- Respect safe areas and dynamic browser chrome.
- Avoid hover-only interactions.

### iPadOS

- Use sidebars and split views when comparing or managing collections.
- Support pointer, keyboard, touch, and drag/drop together.
- Preserve context across pane changes.
- Avoid phone-only modal stacks on wide tablet layouts.

### macOS

- Embrace density when the task is expert or data-heavy.
- Keep commands discoverable through toolbar/menu-like groupings.
- Use inspectors/side panels instead of repeated modal dialogs.
- Preserve keyboard shortcuts and focus order.

### watchOS

- One idea per view.
- Short labels, clear state, minimal choices.
- Good pattern source for compact widgets/status cards, not full desktop UI.
- Cross-platform use is limited to glanceable cards and status summaries; do not mimic watch faces or complications in normal Web/app UI.

### tvOS

- Focus state is the main interaction language.
- Directional movement must be predictable.
- Text is larger and controls are fewer.
- Use focus parallax sparingly and only on active content.
- Cross-platform use is limited to TV, kiosk, remote, gamepad, or keyboard-driven focus grids.

### visionOS

- Depth expresses hierarchy, not spectacle.
- Avoid large z-axis zoom and aggressive parallax.
- Keep glass/material panels readable.
- Reduced motion should flatten depth into clear static layers.
- Cross-platform use is limited to spatial storytelling, layered dashboards, or product demos. Do not fake visionOS windows, system chrome, gaze UI, or immersive OS behavior on ordinary Web pages.

### CarPlay

- Minimize reading and interaction count.
- Use large targets and explicit actions.
- Defer nonessential settings.
- Never use distracting decorative motion.
- Cross-platform use is a safety/low-distraction model for vehicle, field, kiosk, or high-attention environments. Do not use CarPlay as a visual style for general apps.

## 4. Responsive recipe

1. Phone: iOS stack, tab/bottom action, edge sheets.
2. Tablet: iPadOS split/sidebar, larger cards, drag/drop affordance.
3. Desktop: macOS density, toolbar/sidebar/inspector, keyboard shortcuts.
4. TV/kiosk only: tvOS focus grid, large visual targets.
5. Spatial/showcase only: visionOS depth and Liquid Glass with flat fallback.

Default Web / client / mobile products should usually stop at steps 1-3 unless the user explicitly asks for TV/kiosk/spatial behavior.

## 5. Apple Design Resources

| Resource group | Applicability | Use for | Rules |
|---|---|---|---|
| UI Kits | Reference only | Platform measurement and component fidelity | Use to calibrate density/behavior; do not blindly copy into Web |
| Product Bezels | Apple-only asset | README/marketing screenshots | Respect Apple usage terms and avoid misleading support claims |
| Fonts | License-sensitive | SF Pro, SF Compact, SF Mono, New York, language-specific families | Do not redistribute Apple fonts unless license allows; use system stack on Apple devices |
| SF Symbols | Apple-only asset | Symbol style, scale, weight | Use on Apple platforms; use licensed fallback icons elsewhere |
| Icon templates | Platform-specific production | App icon production | Follow export/radius guidance; do not copy Apple app icons |
| Technology templates | Brand-gated | Apple Pay, Wallet, Sign in with Apple, Health, HomeKit, etc. | Use official templates only for supported Apple technologies |

Font policy:

- Apple devices: prefer system fonts and system PingFang SC for Chinese.
- Non-Apple Web: use legal fallback stack; use bundled PingFangSC fallback from [06-fonts.md](06-fonts.md) only for Chinese consistency.
- Do not package SF Pro/SF Symbols as generic Web assets without confirming license.

## 6. Technologies and brand-sensitive features

| Technology | Applicability | Transferable principle | Cross-platform fallback |
|---|---|---|---|
| Apple Pay | Apple-only / brand-gated | Fast, trusted checkout with clear amount/merchant | Neutral payment button, payment-method selector |
| Sign in with Apple | Apple-only / brand-gated | Privacy-preserving sign-in and clear account timing | Neutral SSO/email auth with privacy copy |
| Wallet | Apple-only / analogous pass fallback | Add/save pass with clear confirmation | Download pass/PDF/QR/export flow |
| Live Activities | Apple-only / concept transferable | Glanceable ongoing state | Status chip, toast, persistent task bar |
| Widgets | Concept transferable | One focused job and full-detail destination | Dashboard card, home-screen-like summary |
| App Clips | Apple-only / concept transferable | Lightweight task before full app/account | Guest mode, preview flow, demo task |
| AirPlay | Apple-only / analogous casting fallback | Target selection and connection state | Generic cast/device picker |
| CarPlay | Apple-only / safety model | Low-distraction, glanceable controls | Field/kiosk/vehicle-safe mode, not general UI |
| HealthKit | Apple-only / sensitive-data model | Purposeful permission and data clarity | Health-data module with explicit consent |
| HomeKit | Apple-only / device-control model | Safety-sensitive device state | IoT control panel with clear state/confirmation |
| iCloud | Apple ecosystem / sync model | Sync/offline/conflict clarity | Generic cloud sync state |
| In-app purchase | Platform-specific commerce | Purchase clarity and recovery | Neutral checkout/subscription flow |
| Maps | Transferable with provider rules | Geographic controls and attribution | Provider-compliant map UI |
| Siri / voice | Apple-only / voice model | Clear action names and confirmations | Generic voice/command palette |
| SharePlay | Apple-only / collaboration model | Shared session presence and control | Collaborative session state |
| Game Center | Apple-only / game social model | Achievements, identity, social status | Neutral achievements/profile |
| Generative AI | Transferable | Transparency, user control, correction/undo | AI assistant/generation UI with trust controls |
| Machine learning | Transferable | Personalization clarity and reset/correction | Recommendation/personalization controls |
| Augmented reality | Scenario-specific | Placement feedback, safety boundaries, reset | AR-capable experience only; otherwise static preview |
| Complications / watch faces | Apple-only / micro-status inspiration | Glanceable status in tiny surfaces | Small dashboard tile/status chip |

## 7. Sensitive feature rules

Use this stricter bar for identity, payment, health, home, location, AI, camera/mic, contacts, and sync:

- Ask permission just in time.
- Explain purpose in plain language.
- Offer deny/skip paths where feasible.
- Show sync, sharing, and conflict states clearly.
- Make destructive or irreversible actions explicit.
- Let AI/ML outputs be corrected, undone, or regenerated.
- Do not imply Apple endorsement.

## 8. Official resource links

- Apple Design Resources: https://developer.apple.com/design/resources/
- Apple Fonts: https://developer.apple.com/fonts/
- SF Symbols: https://developer.apple.com/sf-symbols/
- Apple Style Guide: https://support.apple.com/guide/applestyleguide/welcome/web
- AirPlay: https://developer.apple.com/design/human-interface-guidelines/airplay
- Apple Pay: https://developer.apple.com/design/human-interface-guidelines/apple-pay
- App Clips: https://developer.apple.com/design/human-interface-guidelines/app-clips
- Augmented reality: https://developer.apple.com/design/human-interface-guidelines/augmented-reality
- CarPlay: https://developer.apple.com/design/human-interface-guidelines/carplay
- Game Center: https://developer.apple.com/design/human-interface-guidelines/game-center
- Generative AI: https://developer.apple.com/design/human-interface-guidelines/generative-ai
- HealthKit: https://developer.apple.com/design/human-interface-guidelines/healthkit
- HomeKit: https://developer.apple.com/design/human-interface-guidelines/homekit
- iCloud: https://developer.apple.com/design/human-interface-guidelines/icloud
- In-app purchase: https://developer.apple.com/design/human-interface-guidelines/in-app-purchase
- Live Activities: https://developer.apple.com/design/human-interface-guidelines/live-activities
- Machine learning: https://developer.apple.com/design/human-interface-guidelines/machine-learning
- Maps: https://developer.apple.com/design/human-interface-guidelines/maps
- Siri: https://developer.apple.com/design/human-interface-guidelines/siri
- Sign in with Apple: https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple
- SharePlay: https://developer.apple.com/design/human-interface-guidelines/shareplay
- Wallet: https://developer.apple.com/design/human-interface-guidelines/wallet
- Widgets: https://developer.apple.com/design/human-interface-guidelines/widgets
