import numpy as np
from game import Game

class Player:
    def __init__(self, p, g, lr, df):
        self.whoami = p
        self.game = g
        self.learning_rate = lr
        self.discount_factor = df

    def file2list(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

    def str2file(self, str, filename):
        file = open(filename, "a")
        file.write(str)
        file.close()

    def board2state(self, b, p):
        st = np.zeros([9])
        for j in range(3):
            for i in range(3):
                if(b[j][i] == p):
                    st[j * 3 + i] = 1
                elif(b[j][i] == 0):
                    st[j * 3 + i] = 0
                else:
                    st[j * 3 + i] = -1 

        return st

    def arr2str(self, arr):
        str = ''
        for i in range(len(arr)):
            str += "{}".format(arr[i])
            if(i < (len(arr) - 1)):
                str += ","
        return str

    def str2arr(self, str, delim):
        a_str = str.split(delim)
        a_num = np.zeros([len(a_str)])
        for i in range(len(a_str)):
            a_num[i] = float(a_str[i])
        return a_num

    def file2data(self, filename):
        data=[]
        file = open(filename, "r")
        while True:
            line = file.readline()
            if not line: break
            data.append(self.str2arr(line, ','))
        return data

    def data2file(self, data, filename):
        file = open(filename, "w")

        for i in range(len(data)):
            str = self.arr2str(data[i])
            file.write(str)
            if(i < (len(data) - 1)):
                file.write("\n")

    def load_model(self):
        statefile = "./state"
        qvfile = "./qv"
        self.state_list = self.file2data(statefile)
        self.qv_list = self.file2data(qvfile)

    def set_model(self, sl, ql):
        self.state_list = sl
        self.qv_list = ql

    def get_state_list(self):
        return self.state_list

    def get_qv_list(self):
        return self.qv_list

    def save_model(self, state, qv_list):
        statefile = "./state"
        qvfile = "./qv"
        self.data2file(state, statefile)
        self.data2file(qv_list, qvfile)

    def state_in_data(self, state, data):
        for i in range(len(data)):
            if(np.array_equal(state, data[i])):
                return True
        return False

    def get_index_from_data(self, state, data):
        for i in range(len(data)):
            if(np.array_equal(state, data[i])):
                return i
        return -1

    def insert_qv_at_index(self, index, qv_l, qv):
        if(len(qv_l) > index):
            qv_l[index] = qv
        else:
            diff = (index + 1) - len(qv_l)
            for i in range(diff):
                qv_l.append(np.zeros([9]))
            qv_l[index] = qv
        return qv_l

    def save_last_status(self, i, qvs, a, nqvs ):
        self.last_index = i
        self.last_qvalues = qvs
        self.last_a = a
        self.last_next_qvalues = nqvs

    def apply_negative_reward(self):
        self.load_model()
        self.last_qvalues[self.last_a] += self.learning_rate * (-1 + self.discount_factor * np.max(self.last_next_qvalues) - self.last_qvalues[self.last_a])
        self.insert_qv_at_index(self.last_index, self.qv_list, self.last_qvalues)
        self.save_model(self.state_list, self.qv_list)

    def get_action_from_max(self, qvs):
        v_max = np.max(qvs)

        v_max_list=[]
        for i in range(len(qvs)):
            if(qvs[i] == v_max):
                v_max_list.append(i)

        return v_max_list[np.random.randint(len(v_max_list))]

    def get_count_for_max(self, qvs):
        v_max = np.max(qvs)

        count = 0
        for i in range(len(qvs)):
            if(qvs[i] == v_max):
                count+=1
        return count




    def learn(self):
        #print("LEARN >> player:{}".format(self.whoami))
        self.load_model()
        state = self.board2state(self.game.get_board(), self.whoami)

        index = 0
        a = 0
        q_values = np.zeros([9])
        if(self.state_in_data(state, self.state_list)):
            index = self.get_index_from_data(state, self.state_list)
            q_values = self.qv_list[index]
            if(self.get_count_for_max(q_values) > 1):
                a = self.get_action_from_max(q_values)
            else:
                a = np.argmax(q_values)

        else:
            self.state_list.append(state)
            self.qv_list.append(q_values)
            index = self.get_index_from_data(state, self.state_list)
            a = np.random.randint(9)

        #print("LEARN >> action:{} qvalue: {} index: {} qvalues: {}".format(a, q_values[a], index, q_values))


        next_board = self.game.action(self.whoami, a)
        next_state = self.board2state(next_board, self.whoami)
        reward = self.game.judge(self.whoami)
        if(np.array_equal(state, next_state)):
            reward = -10
        #print("LEARN >> reward:{}".format(reward))
        next_q_values = np.zeros([9])
        if(self.state_in_data(next_state, self.state_list)):
            next_index = self.get_index_from_data(next_state, self.state_list)
            next_q_values = self.qv_list[next_index]
            q_values[a] += self.learning_rate * (reward + self.discount_factor * np.max(next_q_values) - q_values[a])
        else:
            self.state_list.append(next_state)
            #next_q_values = np.zeros([9])
            self.qv_list.append(next_q_values)
            q_values[a] += self.learning_rate * (reward + self.discount_factor * np.max(next_q_values) - q_values[a])

        #print("LEARN >> action:{} re-qvalue: {} re-qvalues: {}".format(a, q_values[a], q_values))
        self.qv_list = self.insert_qv_at_index(index, self.qv_list, q_values)
        #print("LEARN >> is_done:{}".format(self.game.is_done()))

        #if(self.game.is_done()):
        #    if(reward == 1):
        #        print("WIN player={} reward={} qvalue={}".format(self.whoami, reward, q_values[a]))
        #    elif(reward == -1):
        #        print("LOSE player={} reward={} qvalue={}".format(self.whoami, reward, q_values[a]))
        #    else:
        #        print("DRAW player={} reward={} qvalue={}".format(self.whoami, reward, q_values[a]))
        self.save_last_status(index, q_values, a, next_q_values)
        self.save_model(self.state_list, self.qv_list)


    def run(self):
        print("RUN >> player:{}".format(self.whoami))
        self.load_model()
        state = self.board2state(self.game.get_board(), self.whoami)

        index = 0
        a = 0
        q_values = np.zeros([9])
        if(self.state_in_data(state, self.state_list)):
            index = self.get_index_from_data(state, self.state_list)
            q_values = self.qv_list[index]
            print("RUN >> trained index: {} qv: {}".format(index, q_values))
            if(self.get_count_for_max(q_values) > 1):
                a = self.get_action_from_max(q_values)
            else:
                a = np.argmax(q_values)



        else:
            print("RUN >> not trained")
            a = np.random.randint(9)

        print("RUN >> action:{} qvalue: {}".format(a, q_values[a]))


        next_board = self.game.action(self.whoami, a)
        next_state = self.board2state(next_board, self.whoami)
        reward = self.game.judge(self.whoami)

        print("RUN >> action:{} reward: {}".format(a, reward))

        if(self.game.is_done()):
            if(reward == 1):
                print("WIN player={} reward={} qvalue={}".format(self.whoami, reward, q_values[a]))
            elif(reward == -1):
                print("LOSE player={} reward={} qvalue={}".format(self.whoami, reward, q_values[a]))
            else:
                print("DRAW player={} reward={} qvalue={}".format(self.whoami, reward, q_values[a]))


