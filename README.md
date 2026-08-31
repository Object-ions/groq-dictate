# groq-dictate

**Hold a key, talk, and your words get typed wherever your cursor is.**

groq-dictate is a tiny push-to-talk dictation tool for the Mac. You hold down a
key (the **` / ~** key by default — a quick tap still types the character), speak
a sentence, and let go. Your speech is
sent to [Groq](https://groq.com)'s super-fast Whisper service, turned into text,
and typed straight into whatever field you're focused on — a browser search box,
an email, a chat message, a code editor, anywhere you can type.

It works in **English, Hebrew, and 90+ other languages**, and it can even
auto-detect the language as you go, so you can switch between them without
changing any settings.

> No machine-learning knowledge needed. No coding needed. If you can copy and
> paste a line of text, you can set this up. This guide assumes you have
> **nothing** installed yet — not even the developer tools — and walks you
> through every single step.

---

## What you'll need

- **A Mac** (Apple Silicon — M1/M2/M3/M4 — or an older Intel Mac; both work).
- **About 10 minutes.**
- **A free Groq account** (we'll create it together in Step 4 — no credit card).

That's it. We will install **everything else** together, one step at a time. You
do **not** need to already have Python, Homebrew, git, or any developer tools —
the steps below install them for you.

---

## Table of contents

1. [Step 1 — Open Terminal](#step-1--open-terminal)
2. [Step 2 — Install Homebrew](#step-2--install-homebrew)
3. [Step 3 — Install uv and git](#step-3--install-uv-and-git)
4. [Step 4 — Get a free Groq API key](#step-4--get-a-free-groq-api-key)
5. [Step 5 — Save your key](#step-5--save-your-key)
6. [Step 6 — Download this project](#step-6--download-this-project)
7. [Step 7 — Run it](#step-7--run-it)
8. [Step 8 — Grant macOS permissions](#step-8--grant-macos-permissions-the-important-one)
9. [Step 9 — Use it](#step-9--use-it)
10. [Make it one word to launch](#make-it-one-word-to-launch)
11. [Settings you can change](#settings-you-can-change)
12. [Run automatically in the background (advanced, optional)](#run-automatically-in-the-background-advanced-optional)
13. [Troubleshooting](#troubleshooting)
14. [Privacy](#privacy)
15. [License](#license)

---

## Step 1 — Open Terminal

**Terminal** is a plain little app where you type commands and press Enter to run
them. It comes built into every Mac. Throughout this guide, whenever you see a
gray box with a command in it, you'll **copy that line, paste it into Terminal,
and press Enter** to run it.

To open Terminal:

1. Press **Cmd + Space** (hold the Command key and tap the spacebar). A little
   search bar appears in the middle of the screen.
2. Type **Terminal**.
3. Press **Enter**.

(If you prefer, you can also find it at **Applications → Utilities → Terminal**.)

A window with a blinking cursor opens. That's it — leave it open; you'll use it
for the next several steps.

> **How to "run a command":** click inside the Terminal window, paste the line
> (Cmd + V), and press **Enter**. The command runs, prints some output, and the
> blinking cursor comes back when it's done. Then you're ready for the next one.

---

## Step 2 — Install Homebrew

**Homebrew** is a free, trusted tool that installs *other* tools for you. We use
it to install the two small programs this project needs. You install Homebrew
once and never think about it again.

Copy this entire line, paste it into Terminal, and press **Enter**:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

A few things will happen — all normal:

- **It may ask for your Mac login password.** This is the password you use to log
  into your Mac. **Important:** as you type your password, **nothing appears on
  screen** — no dots, no stars, nothing. That's a security feature, not a bug.
  Just type your password and press **Enter**.
- **It may first install "Command Line Tools."** This is a one-time download from
  Apple that can take **several minutes**. Let it finish. You might see a separate
  Apple installer window pop up — click through it and wait.

### Very important: the "Next steps" at the end

When Homebrew finishes, it prints a section titled **`==> Next steps:`** with
**two commands** you need to run so your Mac knows where Homebrew lives. **Don't
skip these.**

**On an Apple Silicon Mac (M1/M2/M3/M4 — most Macs from 2020 onward),** run these
three lines, one at a time:

```bash
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**On an older Intel Mac,** Homebrew installs to `/usr/local` instead, and it's
usually already set up on your PATH — so you typically don't need to run those
lines. If Homebrew's own "Next steps" output shows commands, run exactly what it
shows you.

> **Not sure which Mac you have?** Click the  **Apple menu → About This Mac**. If
> it says "Apple M1/M2/M3/M4" you have Apple Silicon. If it says "Intel" you have
> an Intel Mac.

**Check that it worked.** Run:

```bash
brew --version
```

If you see something like `Homebrew 4.x.x`, you're good. If you get
`command not found`, you missed the "Next steps" lines above — go back and run
them, then try again.

---

## Step 3 — Install uv and git

Now use Homebrew to install the two tools we need. Run:

```bash
brew install uv git
```

- **uv** is a modern Python runner. Here's the great part: **uv automatically
  downloads the correct version of Python for you and installs the project's
  dependencies the first time you run it.** That means **you do not have to
  install Python yourself** — uv handles it.
- **git** is the tool used to download (and update) this project.

**Check that it worked.** Run:

```bash
uv --version
```

If you see a version number like `uv 0.x.x`, you're ready.

---

## Step 4 — Get a free Groq API key

An **API key** is a secret password that lets the tool talk to Groq's
transcription service on your behalf. Groq has a free tier — no credit card
needed.

1. Open this page in your browser: **https://console.groq.com/keys**
2. **Sign up** (you can use Google, GitHub, or an email address).
3. Click **Create API Key**, give it any name (e.g. "dictation"), and create it.
4. **Copy the key immediately.** It starts with **`gsk_`** and is shown **only
   once** — once you close that window, you can't see it again (you'd just make a
   new one). Copy it now and keep it on your clipboard for the next step.

---

## Step 5 — Save your key

Now we'll save your key so the tool can find it automatically every time. In the
command below, **replace `gsk_PASTE_YOUR_KEY_HERE` with your real key** (the one
you just copied). Keep the quotes.

```bash
echo 'export GROQ_API_KEY="gsk_PASTE_YOUR_KEY_HERE"' >> ~/.zshrc
source ~/.zshrc
```

The first line saves your key into your shell's settings file (`~/.zshrc`). The
second line loads it into the current Terminal so you don't have to reopen
anything.

**Check that it worked.** Run:

```bash
[ -n "$GROQ_API_KEY" ] && echo "key is set" || echo "not set"
```

If it prints **`key is set`**, you're good. If it prints `not set`, re-do this
step and make sure you pasted your real key between the quotes.

---

## Step 6 — Download this project

This downloads the project onto your Desktop. Just copy the commands below as-is.

```bash
cd ~/Desktop
git clone https://github.com/object-ions/groq-dictate.git
cd groq-dictate
```

- `cd ~/Desktop` moves you into your Desktop folder.
- `git clone …` downloads the project into a new folder called `groq-dictate`.
- `cd groq-dictate` moves you inside that new folder, where the tool lives.

---

## Step 7 — Run it

From inside the `groq-dictate` folder, run:

```bash
uv run groq_dictate.py
```

**The first time you run this, it will take about a minute.** uv is quietly
downloading the right version of Python and all the dependencies (the libraries
that record audio and talk to Groq). This only happens once — future runs start
instantly.

When it's ready, you'll see this line:

```
Ready. Long-press the ` / ~ key to record, release to transcribe. A quick tap types the character as usual. Ctrl-C to quit.
```

That means it's listening. **Leave this Terminal window open while you use the
tool** — closing it or pressing **Ctrl + C** stops the tool.

> If instead you see **`No Groq API key found`**, your key didn't save — go back
> to [Step 5](#step-5--save-your-key).

---

## Step 8 — Grant macOS permissions (the important one!)

⚠️ **This is the step people get stuck on. Read it slowly.** Because this tool
listens for a key, records your microphone, and types text for you, macOS — quite
rightly — requires you to grant permission first. You must add your **Terminal**
app to **three** different lists.

Open **System Settings** (Apple menu  → System Settings), then click
**Privacy & Security** in the sidebar. Inside there you'll find each of these
lists. For each one: click it, then either flip the switch next to **Terminal**
to ON, or click the **+** button and add the Terminal app (from
Applications → Utilities → Terminal).

| Permission | Where to find it | What it's for | Symptom if it's missing |
|---|---|---|---|
| **Input Monitoring** | Privacy & Security → **Input Monitoring** | Lets the tool notice when you press and hold the record key | Holding the key does **nothing** |
| **Microphone** | Privacy & Security → **Microphone** | Lets the tool record your voice | You get **`(no audio captured)`** or empty text |
| **Accessibility** | Privacy & Security → **Accessibility** | Lets the tool auto-type the text into your field | Text appears in **Terminal** but not in your field |

> **Using a different terminal app?** If you run commands in **iTerm**, **Warp**,
> **Ghostty**, or **VS Code's** built-in terminal instead of Apple's Terminal,
> add *that* app to the three lists instead of Terminal.

### Then quit and reopen Terminal

macOS only reads these permissions **when an app launches**. So after granting
them you must fully restart Terminal:

1. With Terminal focused, press **Cmd + Q** to **fully quit** it. (Just closing
   the window with the red dot is **not** enough — it must be Cmd + Q.)
2. Open Terminal again ([Step 1](#step-1--open-terminal)).
3. Go back into the project and run it again:

   ```bash
   cd ~/Desktop/groq-dictate
   uv run groq_dictate.py
   ```

The **first time you record**, macOS shows a one-time popup asking to allow
microphone access — click **Allow** / **OK**.

---

## Step 9 — Use it

1. Click into any text field — a browser address bar, an email, a notes app,
   anywhere you can type.
2. **Press and hold the ` / ~ key** (top-left, below Esc). You'll see
   `● recording…` in the Terminal.
3. **Speak your sentence.**
4. **Let go** of the key. After a moment your words appear right where your
   cursor is. 🎉

> **Pro tip:** hold the key for a brief moment **before** you start talking, so
> the microphone has time to open. If you start speaking the instant you press
> the key, the very start can get cut off — or you'll get
> `(no audio captured)` if the whole clip was too short.

To stop the tool entirely, click the Terminal window and press **Ctrl + C**.

---

## Make it one word to launch

Typing `uv run …` every time is a chore. Let's make a shortcut so you can just
type **`dictate`** from anywhere. Run these two lines once:

```bash
echo "alias dictate='uv run ~/Desktop/groq-dictate/groq_dictate.py'" >> ~/.zshrc
source ~/.zshrc
```

From now on, in any new Terminal window, just type:

```bash
dictate
```

…and the tool starts. (Remember: the Terminal window must stay open while you use
it, and Terminal still needs the three permissions from
[Step 8](#step-8--grant-macos-permissions-the-important-one).)

---

## Settings you can change

You can tweak how the tool behaves by editing the **CONFIG** block near the top of
`groq_dictate.py`. Open it in any text editor (or run
`open -e ~/Desktop/groq-dictate/groq_dictate.py` to open it in TextEdit). You'll
see these settings:

| Setting | What it does |
|---|---|
| **`RECORD_KEYCODE`** | The push-to-talk key you long-press to record, as a macOS keycode. Default is `50` (the **` / ~** key). To use a different key, see the [Troubleshooting](#troubleshooting) tip about `keyprobe.py`. |
| **`LONG_PRESS_SECS`** | How long you must hold the key before it counts as recording instead of typing. Default `0.35` seconds. |
| **`MODEL`** | Which Groq Whisper model to use. Default `whisper-large-v3-turbo` is fast and multilingual. Switch to `whisper-large-v3` for slightly higher accuracy (a bit slower). |
| **`LANGUAGE`** | Leave as `None` to **auto-detect** the language (great if you switch between, say, English and Hebrew). Or pin it to a code like `"en"` (English) or `"he"` (Hebrew) for a little more accuracy and speed. |
| **`AUTO_PASTE`** | `True` = the tool types the text into your field for you (needs the Accessibility permission). `False` = it only copies the text to your clipboard, and you paste it yourself with **Cmd + V**. |

Save the file after editing, then stop the tool (Ctrl + C) and start it again for
the change to take effect.

---

## Run automatically in the background (advanced, optional)

The repo includes `install_agent.sh`, which sets up the tool as a **background
service** that starts automatically when you log in, so you don't have to keep a
Terminal window open. You'd run it from inside the project folder with
`bash install_agent.sh`.

⚠️ **Beginners should skip this and use the [`dictate` alias](#make-it-one-word-to-launch)
instead.** Here's the catch: macOS ties permissions to a *specific program*. The
permissions you granted to **Terminal** in Step 8 do **not** carry over to the
background Python binary — you'd have to grant **Input Monitoring**,
**Microphone**, and **Accessibility** all over again, this time to a Python
binary buried inside a hidden folder. The installer prints the exact path and
instructions when it finishes, but it's fiddly. Only go down this road if you're
comfortable with it.

**The good news: you only do it once.** The installer sets up a private Python
just for this tool (a *uv-managed* Python, copied — not symlinked — into
`~/.groq-dictate/venv`). Because that binary never changes, your permission
grants survive Homebrew upgrades, `uv` upgrades, and system package updates.
(Earlier versions of this installer pointed at Homebrew's Python, and every
`brew upgrade` silently revoked the permissions — that's fixed.) Re-running
`bash install_agent.sh` later, e.g. after pulling an updated script, keeps the
binary and your grants intact and only refreshes the script and dependencies.

---

## Troubleshooting

**"…is not trusted" message, or holding the key does nothing at all.**
The tool isn't allowed to watch your keyboard. Grant **Input Monitoring** to your
terminal app (Step 8), then **Cmd + Q** to fully quit Terminal and reopen it.

**Holding the ` / ~ key does nothing (but permissions are granted).**
Your keyboard might report the key differently (non-US layouts put ` / ~
elsewhere). Find your key's code: from the project folder, run

```bash
uv run keyprobe.py
```

Press the key you want to use; it prints something like `keycode 50`. Press
**Esc** to quit. Then open `groq_dictate.py` and set `RECORD_KEYCODE` to that
number. Save, then restart the tool.

**The text appears in the Terminal window but not in my actual field.**
The tool transcribed you fine, but it's not allowed to type for you. Grant
**Accessibility** to your terminal app (Step 8), then Cmd + Q and reopen. (Or set
`AUTO_PASTE = False` and paste manually with Cmd + V — the text is already on your
clipboard.)

**The background agent stopped working out of nowhere (worked fine before).**
If you installed the background agent with an older version of
`install_agent.sh`, it used Homebrew's Python — and every `brew upgrade`
replaced that binary, which makes macOS silently revoke the permissions.
Fix it for good: pull the latest repo, run `bash install_agent.sh` again
(it now installs a private, never-changing Python), then remove the old
`python` entries in **Input Monitoring** and **Accessibility** and re-add
`~/.groq-dictate/venv/bin/python` as the installer instructs.

**It says `(no audio captured)`.**
The recording was too short or the mic wasn't allowed. Hold the key a moment
**longer**, and start holding it slightly **before** you talk. If it keeps
happening, grant **Microphone** to your terminal app (Step 8), quit with Cmd + Q,
reopen, and click **Allow** on the one-time mic popup.

**It says `No Groq API key found`.**
Your key isn't set. Redo [Step 5](#step-5--save-your-key), making sure you pasted
your real `gsk_…` key between the quotes. Check it with:

```bash
[ -n "$GROQ_API_KEY" ] && echo "key is set" || echo "not set"
```

---

## Privacy

When you dictate, your recorded audio is sent over the internet to **Groq's
cloud** to be transcribed, and the text comes back. This is perfectly fine for
everyday use — search boxes, emails, notes, messages.

**Don't use it for sensitive or regulated content** (medical, legal, financial
records, secrets) that isn't allowed to leave your machine, since the audio
leaves your computer to be processed.

Your **API key stays on your own computer** — it's saved only in your personal
shell settings (`~/.zshrc`), it is listed in `.gitignore`, and it must **never**
be committed to GitHub or shared with anyone.

---

## License

MIT — see [LICENSE](LICENSE). Copyright © 2026 Moses Atia.
