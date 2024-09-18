from atpg import circuit
circuit_under_test_1 = circuit("p1.txt")
circuit_under_test_1.levelize_circuit()
circuit_under_test_2 = circuit("p2.txt")
circuit_under_test_2.levelize_circuit()
print("-----Circuit from bench file p1.txt-----")
print(circuit_under_test_1)
print("-----Circuit from bench file p2.txt-----")
print(circuit_under_test_2)