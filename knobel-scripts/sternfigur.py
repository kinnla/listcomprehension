# Lösung für 54. Mathe-Olympiade, 1.Stufe Olympiadeklasse 6: 540611
import itertools
[a for a in itertools.permutations(range(1, 25,2), 12) if a[0]+a[3]+a[6]+a[10] == a[1]+a[2]+a[3]+a[4] and a[1]+a[2]+a[3]+a[4] == a[1]+a[5]+a[8]+a[11] and a[1]+a[2]+a[3]+a[4] == a[0]+a[2]+a[5]+a[7] and a[1]+a[2]+a[3]+a[4] == a[7]+a[8]+a[9]+a[10] and a[1]+a[2]+a[3]+a[4] == a[4]+a[6]+a[9]+a[11] ]
