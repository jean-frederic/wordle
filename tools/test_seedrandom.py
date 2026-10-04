import math

class SeedRandom:
    def __init__(self, seed_str):
        self.u = 256
        self.l = 6
        self.c = 52
        self.f = self.u ** self.l
        self.h = 2 ** self.c
        self.p = 2 * self.h
        self.v = self.u - 1
        
        # function b(e, t)
        t = []
        n = 0
        r = seed_str
        i = 0
        while i < len(r):
            # JS: t[v & i] = v & (n ^= 19 * t[v & i]) + r.charCodeAt(i++)
            idx = self.v & i
            prev_val = t[idx] if idx < len(t) else 0 # undefined in JS -> NaN in multiplication -> 0 in bitwise XOR
            term = (19 * prev_val) & 0xFFFFFFFF
            n = (n ^ term) & 0xFFFFFFFF
            val = (n + ord(r[i])) & self.v
            if idx < len(t):
                t[idx] = val
            else:
                t.append(val)
            i += 1
            
        # y(e)
        self.e = t
        self.init_y()
        
    def init_y(self):
        e = self.e
        n = len(e)
        if n == 0:
            e = [0]
            n = 1
        self.S = list(range(self.u))
        a = 0
        for i in range(self.u):
            t = self.S[i]
            a = self.v & (a + e[i % n] + t)
            self.S[i] = self.S[a]
            self.S[a] = t
        self.i = 0
        self.j = 0
        # Discard first u (256) outputs: (r.g = function(e){...})(u)
        self.g(self.u)
        
    def g(self, count):
        n = 0
        while count > 0:
            count -= 1
            self.i = self.v & (self.i + 1)
            t = self.S[self.i]
            self.j = self.v & (self.j + t)
            # swap
            self.S[self.i] = self.S[self.j]
            self.S[self.j] = t
            n = n * self.u + self.S[self.v & (self.S[self.i] + t)]
        return n
        
    def random(self):
        e = self.g(self.l)
        t = self.f
        n = 0
        while e < self.h:
            e = (e + n) * self.u
            t *= self.u
            n = self.g(1)
        while e >= self.p:
            e = e // 2
            t = t // 2
            n = n >> 1
        return (e + n) / t

sr = SeedRandom("2022-1-10")
print("Random for 2022-1-10:", sr.random())
