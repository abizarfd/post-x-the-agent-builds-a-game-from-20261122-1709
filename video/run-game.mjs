// Headless runner for Ghost Catcher (index.html).
// Runs the REAL game code from index.html in Node with a recording canvas,
// drives it with a simple AI player (glide the ghost under the lowest star),
// and dumps one draw-op list per frame to video/game-frames.json.
// The video's gameplay frames are rendered from these real game states.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const FPS = 30;
const SECONDS = 10;
const FRAMES = FPS * SECONDS;

const html = readFileSync(join(ROOT, "repo", "index.html"), "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error("no <script> found in index.html"); process.exit(1); }
const code = m[1];

// --- recording canvas -------------------------------------------------------
function makeCtx() {
  const ops = [];
  let path = [];
  const ctx = {
    fillStyle: "#000000",
    font: "10px monospace",
    textAlign: "left",
    textBaseline: "alphabetic",
    _ops: ops,
    fillRect(x, y, w, h) {
      ops.push({ t: "rect", x, y, w, h, c: this.fillStyle });
    },
    beginPath() { path = []; },
    moveTo(x, y) { path.push(["M", x, y]); },
    lineTo(x, y) { path.push(["L", x, y]); },
    closePath() { path.push(["Z"]); },
    arc(x, y, r, a0, a1) { path.push(["A", x, y, r, a0, a1]); },
    fill() {
      if (path.length) {
        ops.push({ t: "fill", items: path, c: this.fillStyle });
        path = [];
      }
    },
    fillText(text, x, y) {
      ops.push({ t: "text", text, x, y, font: this.font,
                 c: this.fillStyle, align: this.textAlign,
                 baseline: this.textBaseline });
    },
  };
  return ctx;
}

const canvas = {
  width: 1280, height: 720,
  getContext: () => recordingCtx,
  addEventListener() {},
  getBoundingClientRect: () => ({ left: 0, width: 1280 }),
};
const recordingCtx = makeCtx();

const sandbox = {
  window: { __HEADLESS__: true, addEventListener() {} },
  document: { getElementById: () => canvas },
  requestAnimationFrame() {},
  console,
};
sandbox.window.window = sandbox.window;
vm.createContext(sandbox);
vm.runInContext(code, sandbox);
const game = sandbox.window.__game;
if (!game) { console.error("__game handle missing"); process.exit(1); }

console.log(`game: loaded index.html (${code.split("\n").length} lines of game code)`);
console.log(`game: canvas ${game.W}x${game.H}, round ${60}s, 3 lives`);

// --- drive 10 seconds with the AI player ------------------------------------
const frames = [];
let overAt = -1;
let committed = null; // stick with one star until it is caught or gone
for (let f = 0; f < FRAMES; f++) {
  const s = game.state();
  if (!s.over) {
    // Commit to the star that will reach the ghost line soonest AND that the
    // ghost can still reach in time; stay with it until it is caught or gone.
    if (committed && !s.stars.includes(committed)) committed = null;
    if (!committed) {
      let bestT = Infinity;
      for (const st of s.stars) {
        const tImpact = (590 - st.y) / st.vy;
        const tReach = Math.abs(st.x - s.ghostX) / 620;
        if (tReach > tImpact + 0.15) continue; // cannot get there in time
        if (tImpact < bestT) { bestT = tImpact; committed = st; }
      }
      if (!committed) { // nothing reachable: take the most urgent anyway
        for (const st of s.stars) {
          const tImpact = (590 - st.y) / st.vy;
          if (tImpact < bestT) { bestT = tImpact; committed = st; }
        }
      }
    }
    if (committed) {
      const dx = committed.x - s.ghostX;
      game.setDir(Math.abs(dx) < 14 ? 0 : Math.sign(dx));
    } else {
      game.setDir(0);
    }
    game.step(1 / FPS);
  } else if (overAt < 0) {
    overAt = f;
  }
  recordingCtx._ops.length = 0;
  game.draw(recordingCtx);
  frames.push(recordingCtx._ops.slice());
}

const s = game.state();
console.log(`game: simulated ${FRAMES} frames (${SECONDS}s at ${FPS}fps)`);
console.log(`game: final score ${s.score} — caught ${s.caught} stars, missed ${s.missed}, lives left ${s.lives}${s.over ? " (round over)" : ""}`);
if (overAt >= 0) console.log(`game: round ended at frame ${overAt} (${(overAt / FPS).toFixed(1)}s)`);

mkdirSync(join(HERE, "frames"), { recursive: true });
writeFileSync(join(HERE, "frames", "game-frames.json"), JSON.stringify(frames));
console.log(`game: wrote ${frames.length} frames to video/frames/game-frames.json`);
