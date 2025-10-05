import sys

class Transition:
    def __init__(self, next_state, write, move):
        self.next_state = next_state
        self.write = write
        self.move = move  # 'L', 'R', 'S'

class Tape:
    def __init__(self, content, blank='_'):
        self.tape = dict((i, ch) for i, ch in enumerate(content) if ch != blank)
        self.head = 0
        self.blank = blank

    def read(self):
        return self.tape.get(self.head, self.blank)

    def write_symbol(self, ch):
        if ch == self.blank:
            self.tape.pop(self.head, None)
        else:
            self.tape[self.head] = ch

    def move_left(self):
        self.head -= 1

    def move_right(self):
        self.head += 1

    def contents_trimmed(self):
        if not self.tape:
            return ''
        mn = min(self.tape.keys())
        mx = max(self.tape.keys())
        return ''.join(self.tape.get(i, self.blank) for i in range(mn, mx+1))

def parse_machine(path):
    spec = {}
    start_state = None
    accept_states = set()
    blank = '_'
    table = {}

    with open(path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    in_trans = False
    for line in lines:
        if '=' in line and not in_trans:
            k, v = line.split('=',1)
            k = k.strip()
            v = v.strip()
            if k == 'startState':
                start_state = v
            elif k == 'acceptStates':
                accept_states.update(x.strip() for x in v.split(',') if x)
            elif k == 'blankSymbol' and v:
                blank = v[0]
        else:
            in_trans = True
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 5:
                continue
            cur, read, write, move, nxt = parts[:5]
            table.setdefault(cur, {})[read] = Transition(nxt, write, move)

    if not start_state:
        raise ValueError("startState not defined in machine file")
    spec['start_state'] = start_state
    spec['accept_states'] = accept_states
    spec['blank'] = blank
    spec['table'] = table
    return spec

def run_machine(spec, tape, max_steps=1000000):
    state = spec['start_state']
    steps = 0
    while steps < max_steps:
        if state in spec['accept_states']:
            status = 'ACCEPT'
            break
        read_sym = tape.read()
        t_row = spec['table'].get(state)
        if not t_row or read_sym not in t_row:
            status = 'HALTED_NO_TRANSITION'
            break
        t = t_row[read_sym]
        tape.write_symbol(t.write)
        if t.move == 'L':
            tape.move_left()
        elif t.move == 'R':
            tape.move_right()
        state = t.next_state
        steps += 1
    else:
        status = 'MAX_STEPS'

    return {
        'final_state': state,
        'status': status,
        'steps': steps,
        'tape_contents': tape.contents_trimmed()
    }

def main():
    if len(sys.argv) < 4:
        print("Usage: python tm_simulator.py machine.txt tape.txt output.txt")
        sys.exit(1)

    machine_file = sys.argv[1]
    tape_file = sys.argv[2]
    output_file = sys.argv[3]

    spec = parse_machine(machine_file)

    with open(tape_file, 'r', encoding='utf-8') as f:
        content = ''.join(l.strip() for l in f if l.strip() and not l.startswith('#'))

    tape = Tape(content, spec['blank'])
    res = run_machine(spec, tape)

    with open(output_file, 'w', encoding='utf-8') as f:
        for k,v in res.items():
            f.write(f"{k}={v}\n")

    print(f"Simulation finished. Status={res['status']}, steps={res['steps']}")

if __name__ == "__main__":
    main()
