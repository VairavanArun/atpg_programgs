from atpg import circuit

circuit_under_test = circuit("p2.txt")
circuit_under_test.levelize_circuit()
print(circuit_under_test)