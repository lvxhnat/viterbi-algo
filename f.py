def viterbi(obs, states, start_p, trans_p, emit_p):
    V, path = [{}], {}  # Path will store the Hot, Cold, ... sequence i.e. v_t(j)
    # Specifically do for t = 0, because its a special case requiring start_p
    for y in states:  # y = "Hot" | "Cold"
        V[0][y] = (
            start_p[y] * emit_p[y][obs[0]]
        )  # { "Hot": P(Hot|start) * P(3|Hot) } at t = 0, (V index 0)
        path[y] = [y]  # "Hot"

    for t in range(1, len(obs)):  # This will be left with t = 1 and 2
        V.append({})
        newpath = {}
        for cur_state in states:  # cur_state = "Hot" | "Cold"
            # We want to take the max probability of the transition from v_0 to v_1
            # max( v_{t-1} * P(Hot|Hot) * P(3|Hot), v_{t-1} * P(Cold|Hot) * P(3|Cold))
            (prob, state2) = max(
                (V[t - 1][y] * trans_p[y][cur_state] * emit_p[cur_state][obs[t]], y)
                for y in states
            )
            # Set the time step to the probability calculated
            V[t][cur_state] = prob
            # This will store the state movement
            newpath[cur_state] = path[state2] + [cur_state]
        # Update path
        path = newpath

    # Return the most likely sequence and its probability
    n = len(obs) - 1
    (prob, state) = max((V[n][y], y) for y in states)

    # If we print this
    print(V, path)
    # We Get
    # [{'Hot': 0.32, 'Cold': 0.020}, {'Hot': 0.0384, 'Cold': 0.064}, {'Hot': 0.0128, 'Cold': 0.0032}]
    # {'Hot': ['Hot', 'Cold', 'Hot'], 'Cold': ['Hot', 'Cold', 'Cold']}
    return (prob, path[state])


if __name__ == "__main__":
    obs = (3, 1, 3)
    states = ("Hot", "Cold")
    start_p = {"Hot": 0.8, "Cold": 0.2}
    trans_p = {
        "Hot": {"Hot": 0.6, "Cold": 0.4},
        "Cold": {"Hot": 0.5, "Cold": 0.5},
    }
    emit_p = {
        "Hot": {1: 0.2, 2: 0.4, 3: 0.4},
        "Cold": {1: 0.5, 2: 0.4, 3: 0.1},
    }
    viterbi(obs, states, start_p, trans_p, emit_p)
