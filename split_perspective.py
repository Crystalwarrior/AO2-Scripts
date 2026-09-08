#!/usr/bin/env python3
"""
Perspective Splitter for Attorney Online demo log files.

Takes a big demo log (where every player's perspective is merged) and produces a
new demo log that only follows one character's point of view.

How it decides what to keep (per-character, chosen in the prompts):
  * MS  (in-character) : keep the target's own messages, plus messages from any
        other character currently in the same area as the target. Any MS without
        an area marker (e.g. GM video broadcasts) is treated as global and kept.
  * CT  (out-of-character): keep messages that are area-tagged to the target's
        current area, plus any global (area-less) CT messages.
  * CT movement ("X moves from A to B"): always tracked for state; only kept if
        it involves the target's current area (someone entering/leaving), or if
        it is the target's own movement.
  * All auxiliary packets (wait, BN, HP, TI, TT, ...) are preserved so the
        output still replays correctly.

The character can be chosen either by its FOLDER (e.g. "DRIO/Kazuo Tengan") or
by its showname (e.g. "Short old man").

Usage:
    python split_perspective.py input.demo output.demo --folder "DRIO/Kazuo Tengan"
    python split_perspective.py input.demo output.demo --showname "Varrick Albertson"
"""

import re
import argparse
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def split_ms(line: str) -> Optional[Tuple[str, str, Optional[int]]]:
    """
    Parse a single-line MS packet.

    Returns (folder, showname, area) or None if this is not a usable MS packet.
    """
    if not line.startswith('MS#') or '%' not in line:
        return None
    parts = line.split('#')
    if len(parts) < 17:
        return None
    folder = parts[3]
    message = parts[5]
    showname = parts[16]
    area = None
    # The area is embedded in the message as:  }}}[26] {{{
    m = re.search(r'\]?\}\}\}\[(\d+)\] \{\{\{', message)
    if m:
        area = int(m.group(1))
    return folder, showname, area


def parse_ct_block(block: List[str]) -> dict:
    """
    Parse an accumulated CT message block (one or more physical lines that form
    a single logical CT packet).

    Returns a dict describing the packet.
    """
    joined = '\n'.join(block)
    info = {
        'joined': joined,
        'area': None,          # int area if area-tagged (CT#[N]<dollar>#...)
        'area_str': None,      # original text of the area tag ("[N]" or None=global)
        'showname': None,      # the sender showname, if derivable
        'client_id': None,     # the sender client id, if derivable
        'kind': 'generic',     # one of: generic, movement, disconnect, action,
                               #         evidence, peek, listing
        'from_area': None,
        'to_area': None,
    }

    # For "CT#GA|REAS|EA#message#1#%", the part between "CT#" and the following
    # "#" can be:
    #   "[N]<dollar>"   -> area-tagged OOC
    #   "<dollar>"      -> global OOC
    #   "showname"      -> old-style CT with a sender showname (no area)
    m = re.match(r'^CT#(.*?)#(.*)$', joined, flags=re.DOTALL)
    if not m:
        return info
    tag, content = m.group(1), m.group(2)

    area_m = re.fullmatch(r'\[(\d+)\]<dollar>', tag)
    if area_m:
        info['area'] = int(area_m.group(1))
        info['area_str'] = f'[{info["area"]}]'
    elif tag == '<dollar>':
        info['area_str'] = None          # global
    else:
        # Two possibilities:
        #   "CT#[N]<showname>#..."  -> area-tagged OOC chat (area [N]).
        #   "CT#[showname]#..."     -> old-style chat, no area.
        area_name_m = re.fullmatch(r'\[(\d+)\]<(.+)>', tag)
        area_plain_m = re.fullmatch(r'\[(\d+)\](.+)', tag)
        if area_name_m:
            info['area'] = int(area_name_m.group(1))
            info['area_str'] = f'[{info["area"]}]'
            info['showname'] = area_name_m.group(2)
        elif area_plain_m:
            # "[N]Name" style (non <dollar> form) still carries an area.
            info['area'] = int(area_plain_m.group(1))
            info['area_str'] = f'[{info["area"]}]'
            info['showname'] = area_plain_m.group(2)
        else:
            # Old style "CT#showname#..."
            info['showname'] = tag

    # Specify the area a showname is acting in (used for generic/action CT).
    info['area_of'] = info['area']

    # --- movement --------------------------------------------------------
    mv = re.search(
        r'\[(\d+)\] (.+?) moves from \[(\d+)\] (.+?) to \[(\d+)\]',
        content)
    if mv:
        info['kind'] = 'movement'
        info['client_id'] = int(mv.group(1))
        info['showname'] = mv.group(2).strip()
        info['from_area'] = int(mv.group(3))
        info['to_area'] = int(mv.group(5))
        info['area_of'] = info['to_area']
        return info

    # --- area listing ("Changed to area: [N] ...") ------------------------
    if 'Changed to area:' in content:
        lm = re.search(r'Changed to area: \[(\d+)\]', content)
        info['kind'] = 'listing'
        info['area'] = int(lm.group(1)) if lm else None
        info['area_str'] = 'listing'
        info['listing_area'] = info['area']
        # collect bullet lines
        bullets = []
        for ln in block:
            s = ln.strip().lstrip('◾◽')
            s = s.strip()
            if s.startswith('['):
                bullets.append(s)
        info['bullets'] = bullets
        return info

    # --- disconnect -------------------------------------------------------
    dc = re.search(r'\[(\d+)\] (.+?) has disconnected\.', content)
    if dc:
        info['kind'] = 'disconnect'
        info['client_id'] = int(dc.group(1))
        info['showname'] = dc.group(2).strip()
        info['area_of'] = info['area']
        return info

    # --- action -----------------------------------------------------------
    ac = re.search(r'\[❗\] \[(\d+)\] (.+?) action:', content)
    if ac:
        info['kind'] = 'action'
        info['client_id'] = int(ac.group(1))
        info['showname'] = ac.group(2).strip()
        info['area_of'] = info['area']
        return info

    # --- presented evidence ----------------------------------------------
    ev = re.search(r'\[(\d+)\] (.+?) has presented evidence:', content)
    if ev:
        info['kind'] = 'evidence'
        info['client_id'] = int(ev.group(1))
        info['showname'] = ev.group(2).strip()
        info['area_of'] = info['area']
        return info

    # --- peeks into -------------------------------------------------------
    pk = re.search(r'\[(\d+)\] (.+?) peeks into', content)
    if pk:
        info['kind'] = 'peek'
        info['client_id'] = int(pk.group(1))
        info['showname'] = pk.group(2).strip()
        info['area_of'] = info['area']
        return info

    return info


def is_aux_line(line: str) -> bool:
    return bool(re.match(
        r'^(wait#|BN#|HP#|ST#|TI#|JD#|LE#|PV#|MC#|MM#|SC#|CU#|SP#|TT#|SH#|'
        r'ML#|RC#|AC#|CO#|RT#|CB#|TF#|TIN#|MS<|CT<|SC<|BN<)', line))


def strip_area_markers(line: str) -> str:
    """
    Remove area markers from a single output line.

    For MS packets, the area is embedded in the message field as
    '}}}[N] {{{...  '. This is removed so only the message text remains.

    For area-tagged OOC chat lines of the form 'CT#[N]<dollar>#...',
    'CT#[N]showname#...' or 'CT#[N]<showname>#...', the '[N]' area tag is
    removed (leaving the global/old-style form).
    """
    if line.startswith('MS#') and '%' in line:
        parts = line.split('#')
        # The message is field index 5 (same layout as split_ms() relies on).
        if len(parts) >= 6:
            parts[5] = re.sub(r'^\s*\]?\}\}\}\[\d+\]\s*\{\{\{', '', parts[5])
            line = '#'.join(parts)
    elif line.startswith('CT#'):
        m = re.match(r'^(CT#)\[(\d+)\](<[^>]*>|.*?)(#.*)$', line, flags=re.DOTALL)
        if m:
            # Rebuild without the [N] area tag in the sender/area slot.
            line = m.group(1) + m.group(3) + m.group(4)
    return line


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def parse_client_bullet(text: str) -> Optional[Tuple[int, Optional[str], Optional[str]]]:
    """
    Parse one client listing bullet like:
        ◾ [12] "Arthur" (DRIO/Wolfgang Akire) <full>: Chew
    Returns (client_id, showname, folder).
    """
    text = text.strip().lstrip('◾◽').strip()
    if not text.startswith('['):
        return None
    idm = re.match(r'\[(\d+)\]', text)
    if not idm:
        return None
    cid = int(idm.group(1))

    showname = None
    folder = None

    q = re.search(r'"([^"]*)"\s*\(([^)]*)\)', text)
    if q:
        showname = q.group(1) if q.group(1) != '' else None
        folder = q.group(2)
    else:
        # No quoted showname, e.g. "DRIO/GM <full>" or "Spectator <full>"
        fm = re.search(r'\(([^)]*)\)', text)
        if fm:
            folder = fm.group(1)
        rest = re.sub(r'^\[\d+\]\s*', '', text)
        rest = re.split(r'\s*<', rest)[0]
        # If rest looks like a folder (contains '/') use it as both, else showname.
        if '/' in rest:
            if not folder:
                folder = rest
        else:
            showname = rest.strip('"')
    return cid, showname, folder


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_blocks(path: str) -> List[dict]:
    """
    Read the file and split it into logical blocks.

    Each block is a dict:
        {'lines': [...], 'type': 'MS'|'CT'|'AUX'|'RAW'}
    Multi-line CT packets are grouped into a single block.
    """
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.readlines()

    blocks = []
    i = 0
    n = len(raw)
    while i < n:
        line = raw[i].rstrip('\n')
        if line.startswith('CT#') or line.startswith('CT<'):
            j = i
            block_lines = []

            while j < n:
                block_lines.append(raw[j].rstrip('\n'))
                if raw[j].rstrip('\n').endswith('#%'):
                    break
                # Defensive: a 'wait#N#%' should never be part of a CT block.
                if raw[j].startswith('wait#') or raw[j].startswith('BN#'):
                    break
                j += 1
            blocks.append({'type': 'CT', 'lines': block_lines})
            i = j + 1
        elif line.startswith('MS#') or line.startswith('MS<'):
            blocks.append({'type': 'MS', 'lines': [raw[i].rstrip('\n')]})
            i += 1
        elif line.startswith('SC#') or line.startswith('BN#') or \
                line.startswith('HP#') or line.startswith('wait#') or \
                is_aux_line(line):
            blocks.append({'type': 'AUX', 'lines': [raw[i].rstrip('\n')]})
            i += 1
        else:
            # Any other line: keep it as-is (part of surrounding structure).
            blocks.append({'type': 'RAW', 'lines': [raw[i].rstrip('\n')]})
            i += 1
    return blocks


def main():
    ap = argparse.ArgumentParser(
        description="Extract a single character's perspective from an AO demo log.")
    ap.add_argument('input_file')
    ap.add_argument('output_file')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--folder', help="Character folder, e.g. 'DRIO/Kazuo Tengan'")
    g.add_argument('--showname', help="Character showname, e.g. 'Short old man'")
    ap.add_argument('--strip-area-markers', action='store_true',
                    help="Remove the area marker (e.g. '}}}[26] {{{') from MS "
                         "messages and the area tag (e.g. '[35]') from "
                         "area-tagged OOC chat lines.")
    args = ap.parse_args()

    blocks = load_blocks(args.input_file)

    # ------------------------------------------------------------------
    # Client / showname / folder mapping
    # ------------------------------------------------------------------
    client_folder: Dict[int, Optional[str]] = {}
    client_showname: Dict[int, Optional[str]] = {}
    showname_folder: Dict[str, str] = {}
    folder_shownames: Dict[str, Set[str]] = {}
    area_names: Dict[int, str] = {}

    def note_showname_folder(showname: Optional[str], folder: Optional[str]):
        if showname and folder and showname not in showname_folder:
            showname_folder[showname] = folder
        if folder:
            folder_shownames.setdefault(folder, set())
            if showname:
                folder_shownames[folder].add(showname)

    def note_client(cid: int, showname: Optional[str], folder: Optional[str]):
        if showname is not None:
            client_showname[cid] = showname
        if folder is not None:
            client_folder[cid] = folder
        note_showname_folder(showname, folder)

    for blk in blocks:
        if blk['type'] == 'MS':
            parsed = split_ms(blk['lines'][0])
            if parsed:
                folder, showname, _area = parsed
                area_names if False else None
                note_showname_folder(showname or None, folder)
                if folder:
                    folder_shownames.setdefault(folder, set())
                    if showname:
                        folder_shownames[folder].add(showname)
        elif blk['type'] == 'CT':
            info = parse_ct_block(blk['lines'])
            if info['kind'] == 'listing':
                name_m = re.search(r'Changed to area: \[(\d+)\]\s*([^\n(]*)', info['joined'])
                if name_m:
                    area_names[int(name_m.group(1))] = name_m.group(2).strip()
                for bullet in info.get('bullets', []):
                    parsed = parse_client_bullet(bullet)
                    if parsed:
                        cid, sh, fo = parsed
                        note_client(cid, sh, fo)
            elif info['kind'] in ('movement', 'evidence', 'peek'):
                if info['client_id'] is not None and info['client_id'] in client_folder:
                    note_showname_folder(info['showname'], client_folder[info['client_id']])
                    # associate this showname's client with folder too
                    client_showname[info['client_id']] = info['showname']
            elif info['kind'] == 'action':
                if info['client_id'] is not None and info['client_id'] in client_folder:
                    note_showname_folder(info['showname'], client_folder[info['client_id']])
                    client_showname[info['client_id']] = info['showname']

    # Resolve the target
    target_folder = args.folder
    target_showname = args.showname
    if target_folder:
        # folder -> possible shownames
        pass
    else:
        target_showname = args.showname
        target_folder = showname_folder.get(target_showname)

    def showname_is_target(sh: Optional[str]) -> bool:
        if not sh:
            return False
        if target_showname and sh == target_showname:
            return True
        if target_folder and showname_folder.get(sh) == target_folder:
            return True
        return False

    def folder_is_target(folder: Optional[str]) -> bool:
        return bool(folder and target_folder and folder == target_folder)

    print(f"Target folder: {target_folder}")
    print(f"Target showname: {target_showname}")

    # ------------------------------------------------------------------
    # Simulation pass
    # ------------------------------------------------------------------
    # Track the current area of every showname, and the target's current area.
    showname_area: Dict[str, Optional[int]] = {}
    # client id -> area (freed on disconnect, re-set on reconnect to 0)
    client_area: Dict[int, Optional[int]] = {}

    current_area: Optional[int] = None

    def fmt_area(area: Optional[int]) -> str:
        if area is None:
            return '?'
        name = area_names.get(area)
        return f'[{area} {name}]' if name else f'[{area}]'

    output_blocks = []

    for blk in blocks:
        keep = False

        if blk['type'] == 'MS':
            parsed = split_ms(blk['lines'][0])
            if not parsed:
                # keep malformed MS for safety
                output_blocks.append(blk)
                continue
            folder, showname, area = parsed

            if showname and area is not None:
                showname_area[showname] = area

            if area is None:
                # Global (e.g. video / GM broadcast): show as-is.
                keep = True
            elif folder_is_target(folder) or showname_is_target(showname):
                keep = True
                current_area = area
            elif area == current_area:
                keep = True
                if showname:
                    showname_area[showname] = area

        elif blk['type'] == 'CT':
            info = parse_ct_block(blk['lines'])

            if info['kind'] == 'listing':
                # Everyone listed is now in that area.
                la = info.get('listing_area')
                for bullet in info.get('bullets', []):
                    parsed = parse_client_bullet(bullet)
                    if parsed:
                        cid, sh, _fo = parsed
                        if sh:
                            showname_area[sh] = la
                        client_area[cid] = la
                # If the target appears in this listing, adopt that area.
                for bullet in info.get('bullets', []):
                    parsed = parse_client_bullet(bullet)
                    if parsed:
                        cid, sh, _fo = parsed
                        if showname_is_target(sh) or \
                           (target_folder and sh and showname_folder.get(sh) == target_folder):
                            if la is not None:
                                current_area = la
                # Global CT -> keep.
                keep = True

            elif info['kind'] == 'movement':
                sh = info['showname']
                fa, ta = info['from_area'], info['to_area']
                cid = info['client_id']

                # Movement always updates state.
                if sh:
                    showname_area[sh] = ta
                if cid is not None:
                    client_area[cid] = ta
                is_target = showname_is_target(sh)
                if is_target:
                    current_area = ta

                # "Same area only": keep if it involves the target's area, or it
                # is the target's own movement.
                if is_target:
                    keep = True
                elif current_area is not None and (fa == current_area or ta == current_area):
                    keep = True

            elif info['kind'] == 'disconnect':
                sh = info['showname']
                cid = info['client_id']
                da = info['area']  # area-tag if present
                # Free the client / remove from area.
                if cid is not None:
                    client_area.pop(cid, None)
                if sh:
                    showname_area.pop(sh, None)
                is_target = showname_is_target(sh)
                # Keep if global, in the target's current area, or it's the target.
                if da is None or da == current_area or is_target:
                    keep = True

            else:
                # generic / action / evidence / peek
                sh = info['showname']
                act_area = info['area']  # None => global
                # Optionally keep the acting showname's tracked area in sync.
                if act_area is not None and sh:
                    showname_area[sh] = act_area
                is_target = showname_is_target(sh)
                # "Same area + global"
                if act_area is None:
                    keep = True
                elif is_target:
                    keep = True
                elif act_area == current_area:
                    keep = True

        elif blk['type'] in ('AUX', 'RAW'):
            # Timing / background / misc lines: always preserved.
            keep = True

        if keep:
            output_blocks.append(blk)

    # Write output
    with open(args.output_file, 'w', encoding='utf-8', newline='\n') as f:
        for blk in output_blocks:
            for line in blk['lines']:
                if args.strip_area_markers:
                    line = strip_area_markers(line)
                f.write(line + '\n')

    print(f"Wrote perspective log to {args.output_file}")
    print(f"Input lines: {sum(len(b['lines']) for b in blocks)}")
    print(f"Output lines: {sum(len(b['lines']) for b in output_blocks)}")


if __name__ == '__main__':
    main()
