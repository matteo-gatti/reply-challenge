import json
from time import process_time_ns
import numpy as np

class Demon:
    def __init__(self, id, s, t, r, ft, f):
        self.id = id
        self.stamina = s
        self.stamina_turns = t
        self.stamina_recover = r
        self.frag_turns = ft
        self.frags = f

    def calculate_spdun(self, current_stamina, MAX_STAMINA, turns_left, maxDemonStamina):       
        if current_stamina < self.stamina:
            return -1
        alpha = sum(self.frags[0:(min(turns_left, self.frag_turns) - 1)])  #α
        alphaFactor = (current_stamina / MAX_STAMINA) * 23 / turns_left
        beta = (self.stamina_recover / self.stamina_turns) if self.stamina_turns <= turns_left else 1  #β
        betaFactor = 1 - (current_stamina / MAX_STAMINA) * 11
        #gamma = (self.stamina / maxDemonStamina)  #γ
        #gammaFactor = 1 - (self.stamina / current_stamina) * .5

        return ((alpha * alphaFactor) + (beta * betaFactor))# * (gamma * gammaFactor)


def main():
    with open('input4.txt', 'r') as input:
        firstline = input.readline().replace("\n", '').split(' ')
        stamina =      int(firstline[0])
        MAX_STAMINA =  int(firstline[1])
        TOT_TURNS =    int(firstline[2])
        tot_enemies =  int(firstline[3])
        current_turn = 0
        demons =       []
        demonIndex = 0
        maxDemonStamina = -np.inf
        for line in input.readlines():
            demonline = line.replace("\n", '').split(' ')
            d = Demon(int(demonIndex), int(demonline[0]), int(demonline[1]), int(demonline[2]), int(demonline[3]), list(map(int, demonline[4:int(demonline[3])])))
            demonIndex += 1
            demons.append(d)
            if d.stamina > maxDemonStamina:
                maxDemonStamina = d.stamina
            #print(json.dumps(d.__dict__))

    #print(demons[1].calculate_spdun(stamina, MAX_STAMINA, TOT_TURNS - current_turn))

    res = []
    staminaRec = [0] * TOT_TURNS
    #staminaRec = [0 for i in range(TOT_TURNS)]

    while current_turn < TOT_TURNS:
        #print(f"Turno {current_turn}")
        stamina = min(stamina + staminaRec[current_turn], MAX_STAMINA)
        #print(f"TURNO {current_turn} - STAMINA: {stamina}")
        matDemon = None
        matDemonValue = -np.inf
        for demon in demons:
            currDemonVal = demon.calculate_spdun(stamina, MAX_STAMINA, TOT_TURNS - current_turn, maxDemonStamina)
            if currDemonVal > matDemonValue and currDemonVal != -1:
                matDemon = demon
                matDemonValue = currDemonVal
        
        if matDemon != None:
            demons.remove(matDemon)
            res.append(matDemon.id)
            stamina -= matDemon.stamina
            #print(f"UCCIDO {json.dumps(matDemon.__dict__)}")
            #print(f"CURRENT STAMINA {stamina}")
            if current_turn + matDemon.stamina_turns < TOT_TURNS:
                staminaRec[current_turn + matDemon.stamina_turns] += matDemon.stamina_recover
                #print(f"STAMINA REC {staminaRec[0:20]}")
                #print(f"___ {current_turn + matDemon.stamina_turns}")
            tot_enemies -= 1
        current_turn += 1 
    
    #print(res)
    
    with open('output4.txt','w') as output:
        for i in range(len(res)):
            output.write('{}\n'.format(res[i]))


if __name__ == "__main__":
    main()