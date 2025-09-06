import os, io

class Node:
    __slots__ = ('v', 'prev', 'next', 'blk')
class Block:
    __slots__ = ('head', 'tail', 'size', 'sum', 'label', 'prev', 'next')

def solve():
    data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
    it = 0
    Q = int(data[it]); it += 1

    # block tuning
    B = int((Q + 1) ** 0.5) + 5
    MAXB = B * 2
    STEP = 1 << 30  # wide gaps for labels

    # ---- helpers on the block list ----
    def relabel():
        """Give consecutive labels with wide gaps."""
        nonlocal blk_head
        cur = blk_head
        lab = 0
        while cur:
            cur.label = lab
            lab += STEP
            cur = cur.next

    def split_block(b: Block):
        """Split a too-large block in half, relabel afterwards."""
        if b.size <= MAXB:
            return
        keep = b.size // 2
        cur = b.head
        for _ in range(keep - 1):
            cur = cur.next
        right = cur.next
        if right is None:
            return  # shouldn't happen
        # create new block after b
        nb = Block()
        nb.prev = b
        nb.next = b.next
        if b.next: b.next.prev = nb
        b.next = nb
        # temporary label; we will relabel all blocks after linking/moving
        nb.label = 0
        nb.head = right
        nb.tail = b.tail
        nb.size = 0
        nb.sum = 0
        # move nodes [right .. old_tail] into nb
        t = right
        while True:
            t.blk = nb
            nb.size += 1
            nb.sum += t.v
            if t is nb.tail: break
            t = t.next
        # adjust left block
        b.tail = cur
        b.size -= nb.size
        b.sum -= nb.sum
        # assign consistent labels
        relabel()

    def is_before(nx: Node, ny: Node) -> bool:
        """Return True if nx appears before ny in the list."""
        bx, by = nx.blk, ny.blk
        if bx is by:
            # same block: walk forward inside the block (≤ block size)
            t = nx
            while t and t.blk is bx:
                if t is ny:
                    return True
                t = t.next
            return False
        return bx.label < by.label

    # ---- initial state ----
    blk_head = Block()
    blk_head.prev = blk_head.next = None
    blk_head.label = 0
    blk_head.size = 1
    blk_head.sum = 0
    n0 = Node()
    n0.v = 0
    n0.prev = n0.next = None
    n0.blk = blk_head
    blk_head.head = blk_head.tail = n0

    pos = {0: n0}
    out = []

    # ---- main loop ----
    for i in range(1, Q + 1):
        t = data[it]; it += 1
        if t == b'1':
            x = int(data[it]); it += 1
            nx = pos[x]
            nn = Node()
            nn.v = i
            nn.blk = nx.blk
            # link in the global list
            nxt = nx.next
            nn.prev = nx
            nn.next = nxt
            nx.next = nn
            if nxt: nxt.prev = nn
            # update block stats
            b = nx.blk
            if b.tail is nx: b.tail = nn
            b.size += 1
            b.sum += i
            pos[i] = nn
            split_block(b)
        else:
            x = int(data[it]); y = int(data[it+1]); it += 2
            nx = pos[x]; ny = pos[y]
            if nx is ny:
                out.append('0'); continue
            if is_before(nx, ny):
                start, end = nx.next, ny
            else:
                start, end = ny.next, nx
            if start is None or start is end:
                out.append('0'); continue
            # remove [start, end)
            s = 0
            cur = start
            while cur is not end:
                s += cur.v
                pos.pop(cur.v, None)
                b = cur.blk
                b.size -= 1
                b.sum -= cur.v
                pv = cur.prev
                nxn = cur.next
                if pv: pv.next = nxn
                if nxn: nxn.prev = pv
                if b.head is cur:
                    b.head = nxn if (nxn and nxn.blk is b) else None
                if b.tail is cur:
                    b.tail = pv if (pv and pv.blk is b) else None
                if b.size == 0:
                    if b.prev: b.prev.next = b.next
                    else: blk_head = b.next
                    if b.next: b.next.prev = b.prev
                cur = nxn
            out.append(str(s))

    os.write(1, ("\n".join(out)).encode())

if __name__ == "__main__":
    solve()
