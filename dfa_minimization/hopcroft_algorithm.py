from pprint import pprint

TransitionTable = dict[int, dict]


def get_set_name(state: int, record: dict, memo: dict) -> str | None:
    if memo.get(state) is not None:
        return memo[state]

    for set_name, sset in record.items():
        if state in sset:
            memo[state] = set_name
            return set_name
    return None


def split(
    set_name: str,
    sset: set,
    alphabet: list,
    transitions: TransitionTable,
    current_set_names: dict,
    memo: dict,
) -> set:
    new_sets = {}
    for state in sset:
        transition_behavior = tuple(
            f"{sym}->{get_set_name(transitions[state][sym], current_set_names, memo)}"
            for sym in alphabet
        )
        if transition_behavior not in new_sets:
            new_sets[transition_behavior] = set()
        new_sets[transition_behavior].add(state)

    if len(new_sets) == 1:  # if the set was not splitted
        return {set_name: sset}

    return {
        f"{set_name}_{i}": subset
        for i, subset in enumerate(
            new_sets.values(),
        )
    }


def minimize_dfa(
    states: set,
    alphabet: set,
    transition_table: TransitionTable,
    accepting_states: set,
) -> dict:
    sorted_alphabet = sorted(alphabet)
    old_accepting_states = accepting_states.copy()
    current_partition = {"NA": states - accepting_states, "A": accepting_states}
    previous_partition = {}

    while current_partition != previous_partition:
        previous_partition = current_partition
        current_partition = {}
        memo = {}
        for name, sset in previous_partition.items():
            if len(sset) == 1:
                current_partition[name] = sset
                continue

            split_sets = split(
                name,
                sset,
                sorted_alphabet,
                transition_table,
                previous_partition,
                memo,
            )
            current_partition.update(split_sets)

    # Construct the minimized DFA components
    new_states = set(current_partition.keys())

    new_accepting_states = {
        s
        for s in new_states
        if any(state in old_accepting_states for state in current_partition[s])
    }

    new_transition_table = {}

    for state_name, state_set in current_partition.items():
        # Pick any state from the set, because they all have the same
        # transition behavior
        representative_state = next(iter(state_set))
        new_transition_table[state_name] = {
            symbol: get_set_name(
                transition_table[representative_state][symbol],
                current_partition,
                memo,
            )
            for symbol in alphabet
        }

    return {
        "1.New States": new_states,
        "2.New Accepting States": new_accepting_states,
        "3.Old States Inside New States": current_partition,
        "4.New Transition Table": new_transition_table,
    }


def main() -> None:
    states = {"A", "B", "C", "D", "E"}
    alphabet = {"0", "1"}
    transitions = {
        "A": {"0": "B", "1": "C"},
        "B": {"0": "B", "1": "D"},
        "C": {"0": "B", "1": "C"},
        "D": {"0": "B", "1": "E"},
        "E": {"0": "B", "1": "C"},
    }
    accepting_states = {"E"}

    pprint(
        minimize_dfa(
            states=states,
            alphabet=alphabet,
            transition_table=transitions,
            accepting_states=accepting_states,
        )
    )

    states = {0, 1, 2, 3, 4, 5}
    alphabet = {"a", "b"}
    transitions = {
        0: {"a": 1, "b": 2},
        1: {"a": 0, "b": 3},
        2: {"a": 4, "b": 5},
        3: {"a": 4, "b": 5},
        4: {"a": 4, "b": 5},
        5: {"a": 5, "b": 5},
    }
    accepting_states = {1, 3, 5}

    pprint(
        minimize_dfa(
            states=states,
            alphabet=alphabet,
            transition_table=transitions,
            accepting_states=accepting_states,
        )
    )


if __name__ == "__main__":
    main()
