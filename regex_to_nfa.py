#!/usr/bin/python

import copy


class NFA(object):
    """Non-deterministic finite automata abstraction """

    HELL_STATE = "HELL_STATE"
    EMPTY_STRING = 'EMPTY_STRING'
    _state_counter = 0

    @classmethod
    def create_new_state(cls):
        new_state = 'Q' + str(cls._state_counter)
        cls._state_counter += 1
        return new_state

    def __init__(self):
        self._alphabet = set()
        self._start = None
        self._end = set()
        self._transitions = {}
        self._states = set()

    def __str__(self):
        result = []
        return result

    def init_from_symbol(self, symbol):
        self._start = NFA.create_new_state()
        self._end.add(NFA.create_new_state())

        self._states.add(self._start)
        self._states = self._states.union(self._end)
        self._alphabet.add(symbol)
        self._transitions[(self._start, symbol)] = set(self._end)

    def init_empty_string(self):
        """NFA that accepts the empty string '#'"""
        self._start = NFA.create_new_state()
        self._end.add(self._start)

        self._states.add(self._start)
        self._alphabet.add('#')

    def init_empty_set(self):
        """NFA that accepts the empty set '%'"""
        self._start = NFA.create_new_state()
        self._states.add(self._start)

    def add_transition(self, state, symbol, next_states):
        """
        symbol may be a number
        next_states should be a set
        """
        key = (state, str(symbol))
        next_states_set = self._convert_to_set(next_states)

        if key in self._transitions:
            self._transitions[key] = self._transitions[key].union(next_states_set)
        else:
            self._transitions[key] = next_states_set
            self._states.add(state)
        self._alphabet.add(symbol)
        self._states = self._states.union(next_states_set)

    def _convert_to_set(self, state):
        if isinstance(state, set):
            return state
        elif isinstance(state, str):
            return set([state])
        elif isinstance(state, list):
            return set(state)
        else:
            raise ValueError("ERROR: invalid state type set, str or list\n")

    def transition(self, current_state, symbol):
        """clients should handle KeyError exception
        current_state may be a string (single state)
        or a set of states"""
        if isinstance(current_state, str):
            key = (current_state, str(symbol))
            return self._transitions[key]

        result = set()
        if isinstance(current_state, set):
            for a_state in current_state:
                key = (a_state, str(symbol))
                try:
                    goto = self._transitions[key]
                except KeyError:
                    goto = set()
                result = result.union(goto)

        if result:
            return result
        else:
            raise KeyError


    def transition_union(self, transtision_funcion):
        """transition_function is a valid data structure"""
        for key in transtision_funcion.keys():
            if key in self._transitions:
                self._transitions[key] = self._transitions[key].union(transtision_funcion[key])
            else:
                self._transitions[key] = transtision_funcion[key]

            # update NFA alphabet and NFA set of states
            nfa_state, nfa_input = key
            self._states.add(nfa_state)
            self._alphabet.add(nfa_input)

            self._states = self._states.union(self._transitions[key])

    def get_transition_function_copy(self):
        return copy.deepcopy(self._transitions)

    def get_start_state(self):
        return self._start

    def set_start_state(self, new_state):
        """new_state should be a string"""
        self._states.add(new_state)
        self._start = new_state

    def update_states(self):
        """analyzes the transition function and updates the
        states of the NFA"""
        pass

    def add_a_final_state(self, state):
        """receives a string that represent a final state
        and add it to the set of final states"""
        self._end.add(state)
        self._states.add(state)

    def get_final_states(self):
        """get a reference to the set of final states"""
        return self._end

    def set_final_states(self, new_states):
        """receives a set, a list or string (single state) that
        contains the final states"""
        new_states_set = self._convert_to_set(new_states)
        self._states = self._states.union(new_states_set)
        self._end = new_states_set

    def get_final_states_copy(self):
        """get a full copy of the final states"""
        return self._end.copy()

    def set_nfa_alphabet(self, alphabet):
        self._alphabet = alphabet

    def get_nfa_alphabet_copy(self):
        """get a full copy of the alphabet"""
        return self._alphabet.copy()

    def get_nfa_alphabet(self):
        """get a reference to the alphabet"""
        return self._alphabet

    def get_nfa_states(self):
        """get a reference to the set of states"""
        return self._states

    def includes_final_state(self, states):
        """receives a set, a list or string (single state) that
        contains possible some states returns True if at least
        a single state belongs to the set of final states"""
        states_set = self._convert_to_set(states)
        return not self._end.isdisjoint(states_set)

    def get_list_of_rechable_states(self):
        """returns a list of rechable states"""
        # initially start state is rechable
        result = set([self._start])
        for states in self._transitions.values():
            result = result.union(states)

        return list(result)


def nfa_union(nfa1, nfa2):
    """takes two NFA's returns the union NFA1+NFA2 """
    nfa = copy.deepcopy(nfa1)

    new_start = NFA.create_new_state()
    new_end = NFA.create_new_state()

    # add transitions for new start state
    nfa.add_transition(new_start, NFA.EMPTY_STRING, nfa.get_start_state())
    nfa.add_transition(new_start, NFA.EMPTY_STRING, nfa2.get_start_state())

    # add transitions from nfa1 and nfa2 final states to new final state
    for a_final_state in nfa.get_final_states():
        nfa.add_transition(a_final_state, NFA.EMPTY_STRING, new_end)

    for a_final_state in nfa2.get_final_states():
        nfa.add_transition(a_final_state, NFA.EMPTY_STRING, new_end)

    # merge transition functions
    nfa.transition_union(nfa2.get_transition_function_copy())

    # set NFA start and final states
    nfa.set_start_state(new_start)
    nfa.set_final_states(new_end)

    return nfa


def nfa_concatenation(nfa1, nfa2):
    """takes two NFA's returns the concatenation NFA1.NFA2 """
    nfa = copy.deepcopy(nfa1)

    # update transitions from nfa1 final state to nfa2 start state
    for a_final_state in nfa.get_final_states():
        nfa.add_transition(a_final_state, NFA.EMPTY_STRING, nfa2.get_start_state())

    # merge transition functions
    nfa.transition_union(nfa2.get_transition_function_copy())

    # no need to update nfa start state but we do need to update the final state
    nfa.set_final_states(nfa2.get_final_states())

    return nfa


def nfa_kleene_star(nfa1):
    """takes an NFA returns the kleene star NFA1*"""
    nfa = copy.deepcopy(nfa1)

    new_start = NFA.create_new_state()
    new_end = NFA.create_new_state()

    # add transitions to/from new start and new final states
    nfa.add_transition(new_start, NFA.EMPTY_STRING, nfa.get_start_state())
    for a_final_state in nfa.get_final_states():
        nfa.add_transition(a_final_state, NFA.EMPTY_STRING, new_end)
        nfa.add_transition(a_final_state, NFA.EMPTY_STRING, nfa.get_start_state())

    # create additional transition from new start to new final state
    # to accept the empty string
    nfa.add_transition(new_start, NFA.EMPTY_STRING, new_end)

    # set NFA start and final states
    nfa.set_start_state(new_start)
    nfa.set_final_states(new_end)

    return nfa


def epsilon_closure(state, nfa):
    """state should be a string"""
    # RECURSIVE????
    stack = [state]
    e_closure = set(stack)
    analized_states = set()

    while stack:
        current_state = stack.pop()
        try:
            new_states = nfa.transition(current_state, NFA.EMPTY_STRING)
        except KeyError:
            new_states = set()

        analized_states.add(current_state)
        for a_state in new_states:
            e_closure.add(a_state)
            if a_state not in analized_states:
                stack.append(a_state)

    return e_closure


def remove_empty_transitions(nfa1):
    """receives an NFA and returns the equivalent NFA
    without empty transitions"""
    nfa = NFA()
    nfa.set_start_state(nfa1.get_start_state())
    nfa.set_final_states(nfa1.get_final_states_copy())
    # alphabet and states will be set automatically

    ext_function = {}
    for state in nfa1.get_nfa_states():
        ext_function[state] = epsilon_closure(state, nfa1)

    # refactor nested loop??
    for state in nfa1.get_nfa_states():
        states_to_analize = _follow_empty_paths(state, ext_function)
        for symbol in nfa1.get_nfa_alphabet():
            if symbol != NFA.EMPTY_STRING:
                for current_state in states_to_analize:
                    try:
                        goto = nfa1.transition(current_state, symbol)
                        goto = _follow_empty_paths(goto, ext_function)
                        nfa.add_transition(state, symbol, goto)
                    except KeyError:
                        continue

    # if start_state in F then start_start is also an accepting state
    if not ext_function[nfa1.get_start_state()].isdisjoint(nfa1.get_final_states()):
        nfa.add_a_final_state(nfa1.get_start_state())

    return nfa


def _follow_empty_paths(states, eclosure_function):
    """receives an iterable of states and a eclosure_function
    (a dictionary) that maps state to set of states"""

    if isinstance(states, str):
        states = [states]

    final_states = set()
    for state in states:
        goto = eclosure_function[state]
        final_states = final_states.union(goto)

    return final_states


class DFA(NFA):
    """deterministic finite automata abstraction """

    def __str__(self):
        return 'hola DFA'

    def add_transition(self, state, symbol, next_state):
        """
        symbol may be a number
        next_state should be a string
        raises and exception if a transition already exists
        """
        key = (state, str(symbol))

        if key in self._transitions:
            if self._transitions[key] != next_state:
                err_mgs = ("ERROR: funcion de transicion ya "
                           "contiene una entrada de {0} a {1}")
                raise KeyError(err_mgs.format(key, self._transitions[key]))

        self._transitions[key] = next_state
        self._states.add(state)
        self._alphabet.add(symbol)
        self._states.add(next_state)

    def transition_union(self, transtision_funcion):
        """transition_function is a valid data structure"""
        print "ERROR: Invalid function for a DFA"


def nfa_to_dfa(nfa1):
    """the NFA should NOT contain empty transitions"""
    dfa = DFA()
    dfa.set_start_state(nfa1.get_start_state())
    # states and alphabet will be set automatically

    # add initial state to the final states set if
    # initial state is a final state
    if nfa1.get_start_state() in nfa1.get_final_states():
        dfa.add_a_final_state(nfa1.get_start_state())

    stack = nfa1.get_list_of_rechable_states()
    states_analized = set([NFA.HELL_STATE])
    while stack:
        current_state = stack.pop()
        for symbol in nfa1.get_nfa_alphabet():
            try:
                next_state = nfa1.transition(current_state, symbol)
            except KeyError:
                next_state = NFA.HELL_STATE
            current_state_name = current_state.__str__()
            next_state_name = next_state.__str__()
            dfa.add_transition(current_state_name, symbol, next_state_name)

            # verify if new state is a final state
            if nfa1.includes_final_state(next_state):
                dfa.add_a_final_state(next_state_name)

            # push new state into stack if not analized
            states_analized.add(current_state_name)
            if next_state_name not in states_analized:
                stack.append(next_state)

    # transtitions for HELL_STATE
    for symbol in nfa1.get_nfa_alphabet():
        dfa.add_transition(NFA.HELL_STATE, symbol, NFA.HELL_STATE.__str__())

    return dfa


def compare_dfas(dfa1, dfa2):
    """recevies 2 deterministic finite automatas, returns
    true if both DFA's recognize the same language"""
    if dfa1.get_nfa_alphabet() != dfa2.get_nfa_alphabet():
        return (False, "No tienen el mismo alfabeto")

    # verify if start states are 'compatible'
    both_accept = (dfa1.get_start_state() in dfa1.get_final_states() and
                   dfa2.get_start_state() in dfa2.get_final_states())
    both_reject = (dfa1.get_start_state() not in dfa1.get_final_states() and
                   dfa2.get_start_state() not in dfa2.get_final_states())

    if not (both_accept or both_reject):
        dfa1_accepts = dfa1.get_start_state() in dfa1.get_final_states()
        output_message = ("La {0} expresion regular accepta la palabra"
                          " vacia pero la {1} expresion regular no")
        if dfa1_accepts:
            return (False, output_message.format('1ra', '2da'))
        else:
            return (False, output_message.format('2da', '1ra'))

    stack = []
    stack.append((dfa1.get_start_state(), dfa2.get_start_state(), ''))

    result = (True, "dfa1 and dfa2 accept the same language")
    states_analized = set()
    while stack:
        current_state1, current_state2, input_str = stack.pop()
        for symbol in dfa1.get_nfa_alphabet():
            next_state1 = dfa1.transition(current_state1, symbol)
            next_state2 = dfa2.transition(current_state2, symbol)

            # verify if states are 'compatible'
            both_accept = (next_state1 in dfa1.get_final_states() and
                           next_state2 in dfa2.get_final_states())
            both_reject = (next_state1 not in dfa1.get_final_states() and
                           next_state2 not in dfa2.get_final_states())

            if not (both_accept or both_reject):
                dfa1_accepts = next_state1 in dfa1.get_final_states()
                output_message = ("La {0} expresion regular accepta la palabra '{1}'"
                                  " pero la {2} expresion regular no")
                if dfa1_accepts:
                    result = (False, output_message.format('1ra', input_str + symbol, '2da'))
                else:
                    result = (False, output_message.format('2da', input_str + symbol, '1ra'))
                break

            # prepare stack for future iterations
            states_analized.add((current_state1, current_state2))
            if (next_state1, next_state2) not in states_analized:
                stack.append((next_state1, next_state2, input_str + symbol))

    return result


def build_dfa(regex):
    """receives a regex in prefix notation and returns
    the equivalent DFA"""
    regex = regex[::-1]
    stack = []

    for symbol in regex:
        if symbol.isalnum():
            symbol_nfa = NFA()
            symbol_nfa.init_from_symbol(symbol)
            stack.append(symbol_nfa)
        elif symbol == '.':
            op1 = stack.pop()
            op2 = stack.pop()
            nfa = nfa_concatenation(op1, op2)
            stack.append(nfa)
        elif symbol == '+':
            op1 = stack.pop()
            op2 = stack.pop()
            nfa = nfa_union(op1, op2)
            stack.append(nfa)
        elif symbol == '*':
            op = stack.pop()
            nfa = nfa_kleene_star(op)
            stack.append(nfa)
        elif symbol == '#':
            symbol_nfa = NFA()
            symbol_nfa.init_empty_string()
            stack.append(symbol_nfa)
        elif symbol == '%':
            symbol_nfa = NFA()
            symbol_nfa.init_empty_set()
            stack.append(symbol_nfa)
        else:
            print "ERROR: Simbolo desconocido {0}\n".format(symbol)
            return -1

    nfa = stack.pop()
    if stack:
        print "ERROR: stack is not empty\n"
        return -1

    nfa = remove_empty_transitions(nfa)
    dfa = nfa_to_dfa(nfa)
    return dfa
