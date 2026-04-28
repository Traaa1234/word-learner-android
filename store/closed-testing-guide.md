# Closed Testing — Recruit & Onboard 12 Testers

Google requires new personal developer accounts to run a **closed test with 12+ testers for 14+ consecutive days** before approving the app for production. This guide covers everything from your Play Console setup to the messages you send testers.

---

## Part 1 — Set up the closed test in Play Console

*(Wait until your account verification email comes through, then:)*

1. **Create the app**
   Play Console → "Create app"
   - App name: `Word Learner`
   - Default language: English (United States)
   - App or game: **App**
   - Free or paid: **Free**
   - Tick the developer-program-policy and US-export-laws boxes
   - Click **Create app**

2. **Fill out the policy/eligibility forms** (left sidebar shows tasks)
   - **App access**: "All functionality is available without restrictions"
   - **Ads**: No ads
   - **Content rating**: complete the questionnaire — answer "no" to every sensitive content question; you'll get an **Everyone** rating
   - **Target audience**: tick **5–8** and **9–12**, opt in to **Designed for Families**
   - **News app**: No
   - **COVID-19 contact tracing**: No
   - **Data safety**: declare "No data collected" and "No data shared"
   - **Government app**: No
   - **Financial features**: No
   - **Health**: No
   - **Privacy policy**: paste your hosted GitHub Pages URL

3. **Main store listing**
   Open the relevant fields and paste from `store/listing-copy.md`:
   - App name → "Word Learner"
   - Short description → from `listing-copy.md`
   - Full description → from `listing-copy.md`
   - App icon → uses the AAB's embedded icon (no separate upload)
   - Feature graphic → upload `store/feature-graphic.png`
   - Phone screenshots → upload all 4 from `screenshots/`
   - Tablet screenshots → optional, can skip
   - Save

4. **Set up Closed testing**
   Sidebar → **Testing → Closed testing** → "Create track"
   - Track name: `closed-test-1` (or anything)
   - Choose **Email list** for testers (vs. Google Group)
   - Click **Create email list** → paste the 12+ tester emails (comma-separated), name it "Initial 12"
   - Save

5. **Upload the AAB**
   In the same Closed testing track:
   - Click **Create new release**
   - Upload `android/app/build/outputs/bundle/release/app-release.aab`
   - Play Console will offer to **enroll in Play App Signing** — accept (Google manages the production signing key, you keep your upload key)
   - Release name: `1.0.0` (auto-suggested)
   - Release notes: "Initial closed test."
   - Save → **Review release** → **Start rollout to closed testing**

6. **Wait for review** (typically a few hours, sometimes 1–2 days)
   You'll get an email when it's approved.

7. **Get the opt-in URL**
   After approval, on the Closed testing page → "How testers join your test" section → copy the **opt-in URL** that looks like
   `https://play.google.com/apps/testing/app.wordlearner.kids`

8. **Send the URL to your testers** using the messages in Part 3 below.

---

## Part 2 — Tester requirements (so you recruit the right people)

Each tester must:
- Have an Android phone or tablet (any model, any version supported by Play)
- Be signed in to Android with a Google account
- Give you the email of that Google account so you can add them to the tester list
- Tap the opt-in URL once and tap "Become a tester"
- Install the app from the link you'll provide
- **Keep the app installed for at least 14 days** (they don't have to use it daily — just not uninstall it)

You only need 12 unique testers, but recruit 15–18 to be safe in case someone forgets or uninstalls.

---

## Part 3 — Recruitment messages (copy / paste / personalize)

### Long version (email / Messenger / WhatsApp)

```
Hi [Name]!

I'm publishing a kids' app called "Word Learner" on the Google Play Store, and Google requires me to run a closed test with 12 friendly testers for 2 weeks before they'll let me launch publicly. Would you help me out?

It's a colorful flashcard app that teaches the 200 most common English words, with audio, fill-in-the-blank, and a friendly fox mascot. Free, no ads, no tracking.

What I'd need from you:
• An Android phone or tablet
• The email of the Google account you sign into Android with — I add it to the tester list
• Once approved, I'll send you a link. Tap it, tap "Become a tester", install the app
• Keep it installed for 14 days (you don't actually have to use it!)

Total time: about 2 minutes. If you spot any bugs or weird behavior, even better — let me know.

Reply with your Google email if you're in, or "no thanks" if not — totally fine either way.

Thanks 🦊
```

### Short version (SMS / iMessage)

```
Hey [Name] — I'm putting a kids' app on Google Play and need 12 testers before they'll let me launch. Would you help? Just need to install on Android, keep it 14 days (don't have to use it). Reply with your Google email if yes!
```

### Tiny version (Twitter DM / Slack one-liner)

```
Hey, putting a kids' app on Play Store — need 12 testers (Android, 14 days, ~2 min of your time). In? DM me your Google email.
```

---

## Part 4 — Onboarding message to send AFTER you have the opt-in URL

Once approved and you have the URL from Part 1 step 7:

```
Thanks for helping test Word Learner! 🦊

Two quick steps:

1. On your Android phone, tap this link:
   https://play.google.com/apps/testing/app.wordlearner.kids
   Sign in if asked, then tap "Become a tester"

2. Wait ~5 minutes (Play needs to register you), then install from:
   https://play.google.com/store/apps/details?id=app.wordlearner.kids

That's it! Please keep the app installed for the next 14 days. You don't need to actually use it — Google just checks that real installs exist.

If anything looks broken or weird, screenshot it and send me a note.

Thank you so much!
```

---

## Part 5 — Where to find 12 testers if you're stuck

- **Family group chats** — ask once, you'll usually get 4–6 yeses
- **Friends with kids** — they're the most natural fit and may actually use it
- **Coworkers** — most have Android phones and don't mind tapping a link
- **Online communities** for app testing:
  - r/TestMyApp (Reddit)
  - r/AndroidAppTesters (Reddit)
  - Closed Beta Testers Facebook group
  - Discord servers like "App Testers Hub"

If you go the online route, be polite and offer to help test someone's app in return — it's the norm.

---

## Part 6 — During the 14-day test

You don't have to do anything daily. Things to watch for:

- **Play Console → Testing → Closed testing** shows you the active tester count. Make sure it stays ≥ 12.
- If a tester uninstalls, the count drops — recruit a backup.
- Send a friendly check-in around day 7: "How's it going? Any feedback?"
- On day 14+, you can apply for **Production access** in Play Console. This is a second review (1–7 days) and unlocks the ability to publish publicly.

---

## Part 7 — After production access is granted

1. **Promote your closed test release to production** (Play Console → Production → Create release → "Use existing release")
2. Set rollout percentage (start at 10–20%, can ramp to 100% later)
3. Submit → wait for the production review (1–3 days)
4. App goes live on the Play Store 🎉

Total timeline from today: **roughly 3–4 weeks**, mostly waiting.
