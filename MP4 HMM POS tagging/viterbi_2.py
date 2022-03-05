"""
Part 3: Here you should improve viterbi to use better laplace smoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
"""
import math
def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    alpha = 0.000001

    tran_dic = {}
    emis_dic = {}

    for i in train:
        for j in range(0, len(i)):
            word = i[j][0]
            tag = i[j][1]

            add_dic(emis_dic, tag, word)

            if (tag != 'END'):
                n_tag = i[j + 1][1]
                add_dic(tran_dic, tag, n_tag)

    tran_pr = cal_pr(tran_dic, alpha)
    emis_pr = cal_em_prob(emis_dic, alpha)

    st_col = {}
    for tag in tran_dic:
        if (tag != 'START'):
            st_col[tag] = math.log((0 + alpha) / (1+alpha*2))
        else:
            st_col[tag] = math.log((1 + alpha) / (1 + alpha * 2))
    result = []

    for i in test:
        b_arr = []
        for word in i:
            if (word != 'START'):
                cur_col, b_col = cal_pr_two(pre_col, tran_pr, emis_pr, word)
                pre_col = cur_col
            else:
                pre_col = st_col.copy()
                b_col = {}
            b_arr.append(b_col)

        temp = []
        for j in range(len(i) - 1, -1, -1):
            if (j == len(i) - 1):
                w_tag = max(pre_col, key=pre_col.get)
                n_tag = b_arr[j][w_tag]
            else:
                w_tag = n_tag
                n_tag = b_arr[j].get(w_tag)
            temp.insert(0, (i[j], w_tag))
        result.append(temp)

    return result

def cal_log(c, u, t, alpha):
    return math.log((c + alpha) / (t+alpha*(u+1)))

def cal_pr(dict, alpha):
    pr_dic = {}

    for i in dict:
        pr_dic[i] = {'unk' : cal_log(0, len(dict[i]), sum(dict[i].values()), alpha)}
        for j in dict[i]:
            pr_dic[i][j] = cal_log(dict[i][j], len(dict[i]), sum(dict[i].values()), alpha)

    return pr_dic


def cal_em_prob(dict, alpha):
    pr_dic = {}
    over_cnt = 0
    scale_dic = {}
    for key in dict:
        count = 0
        for word in dict[key]:
            if (dict[key][word] == 1):
                count += 1
                over_cnt += 1
        if (count == 0):
            count = 0.00001
        scale_dic[key] = count
    for tag in scale_dic:
        scale_dic[key] = scale_dic[key] / over_cnt

    for i in dict:
        scale_alpha = scale_dic[i]
        pr_dic[i] = {'unk' : cal_log(0, len(dict[i]), sum(dict[i].values()), alpha * scale_alpha)}
        for j in dict[i]:
            pr_dic[i][j] = cal_log(dict[i][j], len(dict[i]), sum(dict[i].values()), alpha * scale_alpha)

    return pr_dic

def add_dic(dict, key, key2):
    if(key in dict):
        if(key2 in dict[key]):
            dict[key][key2] = dict[key][key2] + 1
        else:
            dict[key][key2] = 1
    else:
        dict[key] = {key2 : 1}

def cal_pr_two(pre_col, tran_pr, emis_pr, word):
    b_col = {}
    cur_col = {}
    for tag in pre_col:
        start_flag = 1
        for i in pre_col:
            if(start_flag):
                start_flag = 0
                m_tag = i
                m_pr = pre_col[i] + tran_pr[i].get(tag, tran_pr[i]['unk']) + emis_pr[tag].get(word, emis_pr[tag]['unk'])
            else:
                temp = pre_col[i] + tran_pr[i].get(tag, tran_pr[i]['unk']) + emis_pr[tag].get(word, emis_pr[tag]['unk'])
                if(temp > m_pr):
                    m_pr = temp
                    m_tag = i
        b_col[tag] = m_tag
        cur_col[tag] = m_pr

    return cur_col, b_col