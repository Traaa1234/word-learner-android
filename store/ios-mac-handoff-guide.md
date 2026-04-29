# iOS Build & App Store Submission — Mac Handoff Guide

Everything you need to do **on your Mac** to build the iOS version of Word Learner and submit it to the App Store. The repo is already iOS-ready — what's left is the parts that physically require macOS + Xcode.

---

## Part 1 — One-time Mac setup (~45 min, mostly downloads)

You only do this once per Mac.

### 1.1 Install Xcode

Open the **Mac App Store** → search "Xcode" → **Install** (it's a ~12 GB download, the biggest item on the list).

After install, **launch Xcode once** so it accepts its license and downloads additional components (this prompts for your Mac password the first time).

```bash
# Verify it's installed
xcode-select -p
# Expected: /Applications/Xcode.app/Contents/Developer

# Accept the license non-interactively if needed
sudo xcodebuild -license accept
```

### 1.2 Install Command Line Tools (usually auto-installed with Xcode)

```bash
xcode-select --install
```

If it says "already installed," you're good.

### 1.3 Install Node.js

If you don't have it on the Mac:

```bash
# Recommended: install via Homebrew
brew install node
# OR download from https://nodejs.org
```

You need Node 18+ (we used Node 24 on Windows; either works).

### 1.4 Confirm your Apple Developer account is active

Go to https://developer.apple.com/account → sign in → confirm your membership shows **"Active"**. If it's still pending verification, wait until it clears before continuing — signing won't work without it.

---

## Part 2 — Get the project onto your Mac

```bash
# Clone the repo (you already pushed it from Windows)
cd ~
git clone https://github.com/Traaa1234/word-learner-android.git
cd word-learner-android

# Install dependencies — same command as Windows, just runs on Mac
npm install

# Sync iOS to make sure web assets and plugins are up to date
npx cap sync ios
```

> **Note**: Capacitor 8 uses Swift Package Manager for plugins, **not CocoaPods**. So you do *not* need to run `pod install` like older Capacitor tutorials suggest. Xcode resolves Swift packages automatically.

### Open the project in Xcode

```bash
npx cap open ios
# or directly:
open ios/App/App.xcworkspace
```

⚠️ **Open `App.xcworkspace`, NOT `App.xcodeproj`.** The workspace is the right entry point.

---

## Part 3 — Configure code signing in Xcode (~10 min)

1. In Xcode's left sidebar, click the blue **App** project icon at the top
2. Select the **App** target (under TARGETS)
3. Click the **Signing & Capabilities** tab
4. Tick **Automatically manage signing** (recommended for Capacitor projects)
5. **Team** dropdown → select your Apple Developer team
   - If it's blank, click **Add an Account…** → sign in with your Apple ID associated with your Developer Program enrollment
6. **Bundle Identifier**: should already say `app.wordlearner.kids` — if not, set it
7. Xcode will provision automatically. You may see a "Failed to register bundle identifier" message the first time — usually it self-resolves on retry, or you may need to register it manually at https://developer.apple.com/account/resources/identifiers/

---

## Part 4 — Run on the iPhone Simulator (free, no device needed)

1. In the toolbar at the top of Xcode, click the device dropdown (currently shows your Mac or "Any iOS Device")
2. Pick a simulator — e.g. **iPhone 15 Pro**
3. Click the **▶ Run** button (or press ⌘R)
4. The Simulator app launches and your app should boot up
5. Tap a 🔊 button to confirm speech works on iOS too

**Expected**: speech works out of the box on iOS. iOS's text-to-speech is more reliable than Android's — fewer device-specific quirks.

---

## Part 5 — Run on your actual iPhone (free with Apple Developer account)

This is where you'll catch bugs the simulator misses.

1. **Connect iPhone via USB** to the Mac
2. On the iPhone, you'll see a "Trust this computer?" prompt → tap **Trust**, enter your passcode
3. In Xcode's device dropdown, select your iPhone (its name will appear)
4. Click ▶ Run
5. The first time, Xcode signs the app with your Apple Developer team and pushes it to the phone
6. **On the iPhone first time**: Settings → General → VPN & Device Management → tap your developer profile → **Trust**
7. Open the app from the home screen — same launcher icon as on Android

> **Free Personal Team alternative**: even without a paid Apple Developer membership, you can sideload to your own iPhone for 7 days at a time using a free "Personal Team". After 7 days the app stops working until you re-sign and reinstall. Useful for early testing only.

---

## Part 6 — TestFlight beta testing (Apple's "closed testing")

Unlike Google Play's 12-tester / 14-day requirement, Apple has **no minimum tester count or duration**. TestFlight is much faster.

### Two TestFlight tracks:

| Track | Tester limit | Apple review needed | Best for |
|---|---|---|---|
| **Internal** | 100 (must be on your team) | No (instant) | You + a few close friends with Apple IDs you can add as App Store Connect users |
| **External** | 10,000 | Yes (~24 hr review for first build, then automatic) | Wider beta with friends, family, online testers |

### To set up TestFlight:

1. Go to https://appstoreconnect.apple.com/ (separate from developer.apple.com — your same Apple ID logs into both)
2. **My Apps → + → New App**
   - Platforms: **iOS**
   - Name: `Word Learner`
   - Primary language: English (U.S.)
   - Bundle ID: select `app.wordlearner.kids` from the dropdown (shows up after first archive upload, or you register it at developer.apple.com first)
   - SKU: any unique string, e.g. `word-learner-1`
   - User Access: Full Access
3. **Create**

### Upload your first build to App Store Connect:

In Xcode:

1. Top menu: **Product → Scheme → Edit Scheme** → set Build Configuration to **Release**
2. Top menu: **Product → Archive** (must have "Any iOS Device" selected in the device dropdown, not a simulator)
3. After ~2 min, the **Organizer** window opens with your archive
4. Click **Distribute App** → **App Store Connect** → **Upload** → follow prompts
5. Xcode signs and uploads. Wait ~5–15 min for App Store Connect to process the build (you'll see "Processing" status, then it'll appear in TestFlight)
6. In App Store Connect → your app → TestFlight → invite testers via email or share a public link

---

## Part 7 — App Store submission (production release)

After you're happy with TestFlight feedback:

1. App Store Connect → your app → **App Store** tab → **+ Version** (start your 1.0 production listing)
2. Fill in:
   - **App name**: Word Learner
   - **Subtitle** (30 chars): something like "Top 200 sight words for kids"
   - **Promotional text** (170 chars, can update without re-submission): elevator pitch
   - **Description** (4000 chars): paste from `store/listing-copy.md` § "Full description"
   - **Keywords** (100 chars, comma-separated): `phonics,sight words,reading,kids,esl,flashcards,early reader,kindergarten,preschool,letters`
   - **Support URL**: your privacy policy GitHub Pages URL is fine, or a `mailto:lw_jen@yahoo.com` link
   - **Marketing URL**: optional
3. **App Store Icon** (1024×1024): upload `store/icon-only.png` (NOT the 512 version — App Store wants 1024 for iOS)
4. **Screenshots**: required for at least one device size. Apple wants iPhone 6.7" screenshots (1290 × 2796) — bigger than what we generated for Play. Two paths:
   - **Easy**: Run the app on iPhone 15 Pro Simulator (6.7"), take screenshots with `Device → Screenshot` (⌘S), upload those
   - **Reuse**: Upload the existing `screenshots/*.png` (1080×1920) — Apple may resize/letterbox
5. **Age Rating**: complete the questionnaire → answer "no" to everything → **4+** rating
6. **Pricing**: Free
7. **App Privacy**: Same answers as Play Store — declare "no data collected"
8. **Build**: select the build you uploaded via Xcode in Part 6
9. **App Review Information**: 
   - Contact name, email, phone (Apple will use this if reviewers have questions)
   - Demo account: leave blank (no login required)
   - Review notes: short note, e.g. "Children's flashcard app. No login. No data collection. All speech happens on-device."
10. **Submit for Review**

App Store review typically takes **24–48 hours** for a first submission, sometimes longer during holidays. If approved, you can release immediately or schedule.

---

## Part 8 — When to ping me back

- **Any Xcode error** during signing or archive — paste the error message, I'll diagnose
- **Apple rejects the app** — they send a specific reason; some are easy (description tweak) some are deep (functionality change). Most TTS-related rejections are around describing data collection accurately, which we've already nailed
- **Once it's approved and live** — celebrate! 🎉 Then we sync iOS feature parity going forward

---

## Quick reference: useful Xcode shortcuts

| Action | Shortcut |
|---|---|
| Run on selected device | ⌘R |
| Stop running app | ⌘. |
| Take simulator screenshot | ⌘S (saves to Desktop) |
| Build (without running) | ⌘B |
| Clean build folder | ⇧⌘K |
| Archive for distribution | (no shortcut) Product menu → Archive |
| Show/hide left sidebar | ⌘0 |
| Show/hide right sidebar | ⌥⌘0 |
