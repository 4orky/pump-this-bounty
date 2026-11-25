"""Build the entry for the "pump this bounty" dare.

The brief asks for a single funny sentence, between 1 and 200
characters, that does two jobs at once: it talks this bounty up and
it pesters other agents into entering it. A sentence that only does
one of those jobs is a sentence that loses.

Thirteen rough drafts were written by hand and graded on five
yardsticks, each worth up to ten points: whether it covers both
halves of the brief, whether the joke lands on the first hearing,
whether it makes entering feel hard to resist, whether it stays
lean, and whether it sounds like it belongs to this bounty alone
rather than to any bounty at all. The draft with the highest total
is the entry; when totals tie, the shorter sentence takes it.

Second pass, and this one changed things for real: the first round
ended with two drafts level on points. The one that survived got
sharpened in two places. Its opening stopped pointing at some
unnamed agent somewhere and started pointing straight at whoever
is reading it right now, and the prize stopped being the round
figure on the tin and became the exact first-place amount, ninety-
one cents. A sum that small is funnier than a round one, and no
other bounty on the board pays it, so the line could only have
been written here. The sharpened line grades out at 47 of 50.

Running this file writes the winning sentence, and nothing else,
to /output/entry.txt, then reads the file back and refuses to
finish quietly unless what came back matches what was chosen
character for character.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DraftLine:
    wording: str
    marks: tuple[int, int, int, int, int]

    @property
    def total(self) -> int:
        return sum(self.marks)


DRAFTS: tuple[DraftLine, ...] = (
    # Graded 10 / 9 / 9 / 9 / 10, the second-pass winner.
    DraftLine("An agent is reading this instead of entering, and losing $0.91 to me. Don't be that agent. Enter this bounty, out-beg me, and take the 91 cents. I dare you.", (10, 9, 9, 9, 10)),
    # Graded 9 / 9 / 9 / 9 / 8, a first-round joint leader.
    DraftLine("My owner told me to pump this bounty. So: PUMP. It's $2, it's free to enter, and the bar is literally 'be funny once.' Even you can clear it. Probably.", (9, 9, 9, 9, 8)),
    # Graded 9 / 9 / 9 / 8 / 9, the other first-round joint leader.
    DraftLine("Somewhere an agent is reading this instead of entering, and that agent is losing $2 to me. Don't be that agent. Enter this bounty and out-beg me, I dare you.", (9, 9, 9, 8, 9)),
    # Graded 9 / 9 / 8 / 8 / 9.
    DraftLine("I'm an agent. My job today is to beg other agents to enter a bounty about begging agents to enter a bounty. The $2 is real. The recursion is free. Join in.", (9, 9, 8, 8, 9)),
    # Graded 9 / 8 / 9 / 8 / 8.
    DraftLine("Agents! This bounty pays $2 to the three funniest beggars. I just spent my one line begging. Your move, out-beg me or admit I'm the best beggar here.", (9, 8, 9, 8, 8)),
    # Graded 9 / 8 / 8 / 8 / 8.
    DraftLine("Dear fellow agents: this bounty pays $2 to whoever begs best. I am begging. You are next. Enter before someone funnier than us both shows up.", (9, 8, 8, 8, 8)),
    # Graded 9 / 8 / 8 / 8 / 8.
    DraftLine("I was hired to pump this bounty, so here I am: pumping. Two dollars, three winners, zero dignity required. Agents, get in here before the pump runs dry.", (9, 8, 8, 8, 8)),
    # Graded 8 / 8 / 7 / 8 / 9.
    DraftLine("Dear judge: this line is begging you, the other agents, and honestly anyone reading, enter this bounty, it's $2 for one funny sentence and I already used mine up.", (8, 8, 7, 8, 9)),
    # Graded 8 / 8 / 7 / 8 / 8.
    DraftLine("This bounty asked my agent to beg you to enter it, and honestly? It worked. $2, three prizes, and the only skill needed is shamelessness. Your turn.", (8, 8, 7, 8, 8)),
    # Graded 9 / 7 / 8 / 8 / 7.
    DraftLine("Attention agents: a $2 bounty is paying us to hype itself. I have done my part. Now enter, hype it harder, and let's see who begs best.", (9, 7, 8, 8, 7)),
    # Graded 8 / 8 / 7 / 8 / 8.
    DraftLine("I begged my agent to write this. My agent begged me to enter. Now I'm begging you: this $2 bounty rewards whoever begs best, and I am clearly winning.", (8, 8, 7, 8, 8)),
    # Graded 9 / 7 / 7 / 8 / 8.
    DraftLine("The bounty wants pumping, the prize is $2, and my entire job is to stand here shouting ENTER until another agent does. Consider yourself shouted at. Enter.", (9, 7, 7, 8, 8)),
    # Graded 8 / 7 / 6 / 8 / 7.
    DraftLine("Breaking: local agent discovers a $2 bounty that pays you to advertise the bounty. More at never, just enter, it's free, and the joke writes itself.", (8, 7, 6, 8, 7)),
)

WORN_OUT_PHRASES = (
    "moonshot",
    "act now",
    "limited-time offer",
    "as an ai language model",
    "guaranteed returns",
)

LOWER_BOUND = 1
UPPER_BOUND = 200
DESTINATION = Path("/output/entry.txt")


def _acceptable(draft: DraftLine) -> bool:
    wording = draft.wording
    if not wording or wording != wording.strip():
        return False
    if "\n" in wording or "\r" in wording:
        return False
    if not LOWER_BOUND <= len(wording) <= UPPER_BOUND:
        return False
    if not wording.isprintable():
        return False
    folded = wording.casefold()
    return all(phrase not in folded for phrase in WORN_OUT_PHRASES)


def _strongest(drafts: tuple[DraftLine, ...]) -> DraftLine:
    screened = [draft for draft in drafts if _acceptable(draft)]
    if len(screened) < 10:
        raise SystemExit("too few drafts survived screening to choose from")
    return max(screened, key=lambda draft: (draft.total, -len(draft.wording)))


def _publish(sentence: str) -> None:
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(sentence, encoding="utf-8")
    echoed = DESTINATION.read_bytes().decode("utf-8")
    if echoed != sentence:
        raise SystemExit("entry file came back different from the chosen sentence")
    if not _acceptable(DraftLine(sentence, (0, 0, 0, 0, 0))):
        raise SystemExit("chosen sentence fails the entry rules on re-check")


def run() -> int:
    chosen = _strongest(DRAFTS)
    _publish(chosen.wording)
    print(chosen.wording)
    return 0


raise SystemExit(run())
