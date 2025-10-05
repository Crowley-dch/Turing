import os
import random
import sys

def template_invert(blank='_'):
    return f"""startState=q0
acceptStates=q_accept
blankSymbol={blank}

q0,0,1,R,q0
q0,1,0,R,q0
q0,{blank},{blank},S,q_accept
"""

def template_erase(blank='_'):
    return f"""startState=q0
acceptStates=q_accept
blankSymbol={blank}

q0,0,{blank},R,q0
q0,1,{blank},R,q0
q0,{blank},{blank},S,q_accept
"""

def template_binary_increment(blank='_'):
    return f"""startState=q0
acceptStates=q_accept
blankSymbol={blank}

q0,0,0,R,q0
q0,1,1,R,q0
q0,{blank},{blank},L,q_add

q_add,0,1,S,q_accept
q_add,1,0,L,q_carry
q_add,{blank},{blank},S,q_accept

q_carry,1,0,L,q_carry
q_carry,0,1,S,q_accept
q_carry,{blank},1,S,q_accept
"""

def random_tape(length, symbols='01', seed=None):
    rnd = random.Random(seed)
    return ''.join(rnd.choice(symbols) for _ in range(length))

def main():
    if len(sys.argv) < 4:
        print("Usage: python tm_generator.py <template> <outdir> <length>")
        sys.exit(1)
    template = sys.argv[1]
    outdir = sys.argv[2]
    length = int(sys.argv[3])

    os.makedirs(outdir, exist_ok=True)

    if template == 'invert':
        machine_text = template_invert()
        tape_text = random_tape(length)
    elif template == 'erase':
        machine_text = template_erase()
        tape_text = random_tape(length)
    elif template == 'binary_increment':
        machine_text = template_binary_increment()
        tape_text = random_tape(length)
    else:
        print("Unknown template. Available: invert, erase, binary_increment")
        sys.exit(2)

    with open(os.path.join(outdir, 'machine.txt'), 'w', encoding='utf-8') as f:
        f.write(machine_text)
    with open(os.path.join(outdir, 'tape.txt'), 'w', encoding='utf-8') as f:
        f.write(tape_text)

    print(f"Files generated in {outdir}")

if __name__ == "__main__":
    main()
