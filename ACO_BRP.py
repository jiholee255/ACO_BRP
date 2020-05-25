import numpy as np
import random
import copy
import pprint 

class ACO:

    def __init__(self,row,col,block,ants):
        self.col = col
        self.row = row
        self.block = block
        self.bay = self.make_bay(self.row,self.col,self.block)
        self.ants = ants
        self.solution = []
        self.lowBound = self.get_lb(self.bay)
        self.best_score = None
        


    def make_bay(self,row,col,block):
        idx_lst = []
        block_lst = [n for n in range(1,block+1)]
        random.shuffle(block_lst)
        size=block
        bay =[]
        for r in range(row):
            flag = True
            while(flag):
                val = random.randrange(0,size-1)
                if val in idx_lst:
                    pass
                else:
                    flag = False
                    idx_lst.append(val)
        for x in idx_lst:
            bay.append(block_lst[0:x])
            block_lst = block_lst[x:]

        return bay

    def get_lb(self,current_bay):
        lb = 0
        for r in current_bay:
            for i in range(0,len(r)-1):
                if r[i]<r[i+1]:
                    lb+=1
        return lb

    def get_val(self,lb,size_s):
        val = 1/(size_s-lb+1)
        return val

    def get_dd(self,dest_stack,current_bay):

        return min(current_bay[dest_stack]) if current_bay[dest_stack]!= [] else self.block+1

    def get_dd_ACO(self,dest_stack,current_bay):
        return min(current_bay[dest_stack]) if current_bay[dest_stack]!= [] else dest_stack+self.block

    def get_diff(self,source,current_bay):
        dif_lst = []
        for x in [x for x in range(self.row) if self.row!=source[0]]:
            if len(current_bay[x])<self.col:
                dif_lst.append([x,self.get_dd(x,current_bay)-current_bay[source[0]][source[1]] if self.get_dd(x,current_bay)>current_bay[source[0]][source[1]] else 2*self.block+1-self.get_dd(x,current_bay)])
        return dif_lst
    def get_diff_ACO(self,source,current_bay):
        dif_lst = []
        for x in [x for x in range(self.row) if self.row!=source[0]]:
            if len(current_bay[x])<self.col:
                dif_lst.append([x,self.get_dd_ACO(x,current_bay)-current_bay[source[0]][source[1]] if self.get_dd_ACO(x,current_bay)>current_bay[source[0]][source[1]] else 2*self.block+1-self.get_dd_ACO(x,current_bay)])
        return dif_lst

    def move_container(self,solution_set,current_bay,s,d,t):
        c = current_bay[s[0]].pop(-1)
        dd = self.get_dd_ACO(d,current_bay)
        b_ = sum([x[2] for x in self.solution if x[0] ==c])
        b = b_ if b_ !=0 else 1
        current_bay[d].append(c)
    
        #! solution은 [c,d,b,t] 형태임
        #! c = 옮겨질 컨테이너
        #! d = 목적지 stack (dd()함수로 계산된 dd로 표현)
        #! b = c가 옮겨진 횟수
        #! t = c가 왜 옮겨지는지 (target container)
        solution_set.append([c,dd,b,t])
    
    def get_f(self,source,current_bay):
        f_lst = []
        for dest_stack,dif in self.get_diff_ACO(source,current_bay):
            f_lst.append([dest_stack,1/(1+dif)])
        return f_lst

    def select_relocation(self):
        pass

    def greedy(self):
        tmp_bay = copy.deepcopy(self.bay)
        pprint.pprint(tmp_bay)
        flg_empty=True
        while(flg_empty):
            if sum([len(tmp_bay[x]) for x in range(self.row)])==0:
                # pprint.pprint(tmp_bay)
                flg_empty =False
                continue
            min_value = min([min(x) for x in tmp_bay if x !=[]])
            min_index = None ## [min value의 행,열]
            for r in range(self.row):
                try:
                    min_index = [r,tmp_bay[r].index(min_value)]
                except:
                    pass
            flg_done = True
            if min_index[1]+1==len(tmp_bay[min_index[0]]):
                tmp_bay[min_index[0]].pop()
                continue
            while(flg_done):
                dest_stack = sorted(self.get_diff(min_index,tmp_bay),key = lambda dd:dd[1])[0][0]
                self.move_container(self.solution,tmp_bay,min_index,dest_stack,min_value)
                # pprint.pprint(tmp_bay)
                if tmp_bay[min_index[0]][-1]==min_value:
                    tmp_bay[min_index[0]].pop()
                    # pprint.pprint(tmp_bay)
                    flg_done = False
        pprint.pprint("soltion:")
        pprint.pprint(self.solution)
        pprint.pprint("=======================================================================================")
    def cal_cdmt(self,current_bay,s,d,t):
        c = current_bay[s[0]][-1]
        dd = self.get_dd_ACO(d,current_bay)
        b_ = sum([x[2] for x in self.solution if x[0] ==c])
        b = b_ if b_ !=0 else 1

        #! solution은 [c,d,b,t] 형태임
        #! c = 옮겨질 컨테이너
        #! d = 목적지 stack (dd()함수로 계산된 dd로 표현)
        #! b = c가 옮겨진 횟수
        #! t = c가 왜 옮겨지는지 (target container)

        return [c,dd,b,t]
    
    def start_aco(self):
        self.greedy()
        self.best_score = self.get_val(self.get_lb(self.bay),sum([x[2] for x in self.solution]))
        flg_stop = True
        while(flg_stop):
            for n in range(self.ants):
                not_corr = False
                current_sol =[]
                current = copy.deepcopy(self.bay)
                flg_empt= True
                while(flg_empt):
                    if sum([len(current[x]) for x in range(self.row)])==0:
                        flg_empt =False
                        continue
                    min_value = min([min(x) for x in current if x !=[]])
                    min_index = None ## [min value의 행,열]
                    for r in range(self.row):
                        try:
                            min_index = [r,current[r].index(min_value)]
                        except:
                            pass
                    flg_done = True
                    if min_index[1]+1==len(current[min_index[0]]):
                        current[min_index[0]].pop()
                        continue
                    while(flg_done):
                        f_lst = self.get_f(min_index,current)
                        g_lst = []
                        for dst, f in f_lst:
                            g_lst.append([dst,sum([f*x for x in self.cal_cdmt(current,min_index,dst,min_value)])])
                        dest_heuristic = sorted(self.get_diff_ACO(min_index,current),key = lambda dd:dd[1])[0][0]
                        best_idx = list(sorted(g_lst,key = lambda g:g[1],reverse = True))[0][0]
                        best_Gval = list(sorted(g_lst,key = lambda g:g[1],reverse = True))[0][1]
                        prob = best_Gval/sum([x[1] for x in g_lst])
                        if random.randint(0,1):
                            dest_alpha = best_idx
                        else:
                            dest_alpha = np.random.choice([best_idx,dest_heuristic],p=[prob,1-prob])
                        self.move_container(current_sol,current,min_index,dest_alpha,min_value)
                        size_current = sum([x[2] for x in current_sol])
                        size_best = sum([x[2] for x in self.solution])
                        if size_current+self.lowBound >= size_best:
                            flg_empt =False
                            not_corr = True
                            break
                        if current[min_index[0]][-1]==min_value:
                            current[min_index[0]].pop()
                            flg_done = False
                if not_corr:
                    continue
                current_score = self.get_val(self.get_lb(self.bay),sum([x[2] for x in current_sol]))
                if current_score>self.best_score:
                    self.solution = current_sol
                    self.best_score = current_score
                    print('good')
            flg_stop = False
        return self.solution


aco = ACO(10,10,70,10)
pprint.pprint(aco.start_aco())