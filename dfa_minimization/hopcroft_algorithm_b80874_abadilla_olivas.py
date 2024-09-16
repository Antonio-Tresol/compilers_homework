from pprint import pprint
from collections import defaultdict

TransitionTable = dict[int, dict]


def get_set_name(state: int, record: dict, memo: dict) -> str | None:
    if memo.get(state) is not None:
        return memo[state]

    for set_name, sset in record.items():
        if state in sset:
            memo[state] = set_name
            return set_name
    return None


def subset_to_str(subset: set) -> str:
    subset = sorted(subset)
    return "-".join(map(str, subset))


def split(
    set_name: str,
    sset: set,
    alphabet: list,
    transitions: TransitionTable,
    current_set_names: dict,
    memo: dict,
) -> set:

    new_sets = defaultdict(set)
    for state in sset:
        transition_behavior = tuple(
            f"{sym}->"
            f"{get_set_name(transitions[state][sym], current_set_names, memo)}"
            for sym in alphabet
        )

        new_sets[transition_behavior].add(state)

    if len(new_sets) == 1:  # if the set was not splitted
        return {set_name: sset}

    return {f"{subset_to_str(subset)}": subset for subset in new_sets.values()}


def minimize_dfa(
    states: set,
    alphabet: set,
    transition_table: TransitionTable,
    accepting_states: set,
) -> dict:
    sorted_alphabet = sorted(alphabet)
    old_accepting_states = accepting_states.copy()
    current_partition = {
        "NA": states - accepting_states,
        "Accepting": accepting_states,
    }
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

    new_states, new_accepting_states, new_transitions = build_minimized_dfa(
        alphabet,
        transition_table,
        old_accepting_states,
        current_partition,
        memo,
    )

    return {
        "1.New States": new_states,
        "2.New Accepting States": new_accepting_states,
        "3.New Transition Table": new_transitions,
    }


def build_minimized_dfa(
    alphabet: list,
    transition_table: dict,
    old_accepting_states: set,
    current_partition: dict,
    memo: dict,
) -> tuple[set, set, dict]:
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

    return new_states, new_accepting_states, new_transition_table


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
        ),
    )

    print()

    states = {"q_0", "q_1", "q_2", "q_3", "q_4", "q_5", "q_6", "q_7"}
    alphabet = {"0", "1"}
    transitions = {
        "q_0": {"0": "q_1", "1": "q_5"},
        "q_1": {"0": "q_6", "1": "q_2"},
        "q_2": {"0": "q_0", "1": "q_2"},
        "q_3": {"0": "q_2", "1": "q_6"},
        "q_4": {"0": "q_7", "1": "q_5"},
        "q_5": {"0": "q_2", "1": "q_6"},
        "q_6": {"0": "q_6", "1": "q_4"},
        "q_7": {"0": "q_6", "1": "q_2"},
    }
    accepting_states = {"q_2"}
    pprint(
        minimize_dfa(
            states=states,
            alphabet=alphabet,
            transition_table=transitions,
            accepting_states=accepting_states,
        ),
    )

    print()

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
        ),
    )


if __name__ == "__main__":
    main()
