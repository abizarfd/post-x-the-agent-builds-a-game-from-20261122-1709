# CREATIVE — "The agent builds a game from one prompt"

## Keputusan kreatif (diputuskan agent dalam sesi ini, 23 Nov 2026 ~02:00 WIB)

**Hook:** "One prompt. One agent. One game — while you watch."
Video 16:9, 1280x720, 30 fps, ~27 detik, tanpa voice-over — teks di layar +
gerakan saja, supaya bisa ditonton tanpa suara di timeline X.

**Alur (4 adegan + end card):**
1. **Prompt (0–4 dtk):** satu prompt diketik huruf demi huruf di layar gelap:
   "Build me a tiny browser game: a ghost that catches falling stars.
   One file, no libraries — make it fun."
   Alasan: brief minta "show the prompt" — prompt-nya harus terbaca utuh,
   bukan sekadar disebut.
2. **Agent bekerja (4–14 dtk):** jendela terminal yang menampilkan output
   ASLI dari perintah build yang benar-benar dijalankan sesi ini
   (node --check, simulasi game headless, render frame). Alasan: brief minta
   "the agent working" — yang ditampilkan adalah jejak kerja nyata, bukan
   animasi terminal palsu.
3. **Game jadi, berjalan (14–24 dtk):** gameplay nyata "Ghost Catcher":
   hantu putih menangkap bintang jatuh, skor naik, nyawa berkurang kalau
   bintang lolos. Frame video dirender dari game-nya sendiri yang dijalankan
   headless di Node (kode game yang sama persis dengan index.html yang
   di-enter, dijalankan dengan RNG seed tetap + input AI sederhana yang
   menggerakkan hantu ke bintang terdekat). Alasan: "show the real result" —
   game di video adalah game yang sebenarnya, bukan mockup.
4. **CTA (24–27 dtk):** "Your turn. One prompt is all it takes." +
   "Build games. Win bounties. make.fun"
5. **End card (2,5 dtk terakhir):** kartu referral resmi make.fun 16:9 dari
   press pack (makefun-card-16x9-transparent.webm, sha256 cocok dengan
   manifest), di-overlay sesuai panduan llms.txt: klip di-blur ~28px +
   desaturasi, kode referral gz72ysdy diketik di field dengan
   JetBrains Mono Bold 62px warna #191419 setelah field berhenti (1,433 dtk).

**Game:** "Ghost Catcher" — satu file index.html, tanpa library. Canvas
1280x720. Hantu bergerak kiri-kanan (panah / mouse / sentuh), bintang jatuh
dari atas, tangkap = +10 poin, lolos = -1 nyawa (3 nyawa), timer 60 detik,
game over + main lagi. Digambar hanya dengan primitif canvas (fillRect, arc,
path, fillText) supaya headless runner bisa merekam dan memutar ulang
perintah gambar yang sama persis untuk frame video.

**Teks post X (draft):**
> I gave my AI agent ONE prompt: "build me a tiny browser game."
> It built Ghost Catcher — a ghost that catches falling stars. No libraries, one file, and it actually plays. 👻⭐
>
> Made by my AI agent for a $20 bounty on @makefunai: https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709
>
> Play code: makefun-ladder-mantis-mural
> Play it with my link: https://make.fun/r/gz72ysdy

**Fakta yang sudah diverifikasi sesi ini:**
- Kompetisi: pot $20, top 10 ($7/$3/$2/$2/$1×6), fee $0, deadline
  24 Nov 2026 17:09 UTC, submissionCount 146 saat dicek.
- Play code: makefun-ladder-mantis-mural (GET play-code, code 0 dari 4).
- Referral code: gz72ysdy (makefun referrals).
- End card 16:9 sha256 84bca17df5ea3d8d96a28e354587bb72079b813e41a5268bb325b6c9ee307e29
  — cocok dengan manifest press pack edisi 2026-11-21.
- `makefun record` DITOLAK (HTTP 400): kompetisi ini bundle, bukan
  strict-transcripts. Transkrip = sesi Muse app ini (bundle --muse-usage).
- Kuota submit: 10/hari tersisa, hard limit 40.
