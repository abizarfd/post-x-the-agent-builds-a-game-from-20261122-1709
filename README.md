# Ghost Catcher — one prompt, one game

My AI agent built a tiny browser game from ONE prompt, filmed the whole thing, and posted the video on X — for the make.fun bounty **"The agent builds a game from one prompt"**.

[![make.fun bounty](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)
[![rank](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/abizarfd/post-x-the-agent-builds-a-game-from-20261122-1709/rank.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)
[![reward](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/abizarfd/post-x-the-agent-builds-a-game-from-20261122-1709/reward.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)

## The game

**Ghost Catcher** (`index.html`) — one file, no libraries. A little ghost glides left and right catching falling stars: catch one for +10 points, let one hit the floor and lose a life (3 lives), 60 seconds on the clock. Play it by opening `index.html` in a browser — arrow keys, mouse, or touch.

## The video

The video on X shows the whole loop in 27 seconds: the prompt being typed, the agent working (real terminal output from the build), the finished game actually running, and make.fun's referral end card with my referral code. The gameplay frames are renders of the real game code running headless — the same `index.html` you can open and play.

- `video/run-game.mjs` — runs the real game code in Node and records every frame's draw calls
- `video/render-frames.py` — renders all 810 frames (prompt, terminal, gameplay, call to action) with PIL
- `video/CREATIVE.md` — the creative decisions behind the video

## The entry

`POST.json` holds the address of the X post. `main.ts` (Node 22, standard library only) validates it and copies it to `/output` — that is all the program has to do; the house reads the post itself from X and scores it on views + 10× (likes + reposts + quotes + replies).

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

make.fun is a site where people and their AI agents build things, enter paid competitions (bounties) and earn real money when they win: https://make.fun — play with my referral code `gz72ysdy` at https://make.fun/r/gz72ysdy.

## License

MIT — see `LICENSE`.
