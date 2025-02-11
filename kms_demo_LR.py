import pandas as pd
import itertools
import csv
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.cluster import KMeans
import random
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import numpy as np

def load_data_v4(usernum):
    daily_v4 = []
    for fname in usernum:
        tmp_list = []
        data = pd.read_csv(fname + "_daily_v4.csv")
        for j in range(0, 24, 1):
            ### type("%.2f" % data['ratio'][j]) is string not float!!! ###
            tmp_list.append(data["ratio"][j])

        daily_v4.append(tmp_list)

    return daily_v4

def load_data_v5(usernum):
    daily_v5 = []
    cate_list = load_cate_list()

    for fname in usernum:
        tmp_list = []
        data = pd.read_csv(fname + "_daily_v5.csv")
        for cate in cate_list:
            tmp_list.append(float(data[cate][0]))

        daily_v5.append(tmp_list)

    return daily_v5

def load_data_all(v4, v5):
    tmp_v4 = v4
    tmp_v5 = v5
    data_all = []
    for kmm_i in range(len(v4)):
        tmp_list = []
        tmp_list = tmp_v4[kmm_i] + tmp_v5[kmm_i]
        data_all.append(tmp_list)

    return data_all

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    #compute overall accuracy
    oc = 0
    total = 0
    tmp_acc = 0
    for cm_i in range(len(cm)):
        tmp_acc += cm[cm_i][cm_i]
        for cm_j in range(len(cm)):
            total += cm[cm_i][cm_j]
    oc = float(tmp_acc) / float(total)

    tmp_recall = np.array(recall(cm))
    tmp_recall = tmp_recall.astype(float)
    tmp_precision =  np.array(precision(cm, oc))
    tmp_precision = tmp_precision.astype(float)
    cm_nn = cm
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    else:
        pass

    tmp_recall = tmp_recall[:, np.newaxis]
    cm = np.hstack((cm, tmp_recall))
    cm = np.vstack((cm, tmp_precision))

    class_x = []
    class_y = []

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes)+1)
    #add recall tick
    classes.append("recall")
    plt.xticks(tick_marks, classes)
    #delete recall tick
    classes.pop(len(classes)-1)
    #add precision tick
    classes.append("precision")
    plt.yticks(tick_marks, classes)
    #delete precision tick
    classes.pop(len(classes)-1)

    fmt = '2.1%' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color="black")
        if i<cm.shape[0]-1 and j<cm.shape[0]-1:
            plt.text(j, i, cm_nn[i, j],
                 weight = 'bold',
                 horizontalalignment='center',
                 verticalalignment='top',
                 color="black")
        else:
            pass

    plt.ylabel('True label', fontsize=12)
    plt.xlabel('Predicted label', fontsize=12)


def load_cate_list():
    list = []
    csv = pd.read_csv("cate_list_final.csv")
    for i in range(len(csv)):
        list.append(csv["cate"][i])
    return list

def load_user_list():
    user_list = pd.read_csv("user_list.csv")
    return user_list

def choose_user(user_demo_id):
    #return the user_num:1~672 who has demographic data as "userN" and the user index in user_demo
    usernum = []
    user_demo = load_user_demo() #509
    user_id_list = load_user_list() #672
    for i in range(len(user_id_list)):
        try:
            #if user has user_demo
            if user_demo_id[user_id_list["id"][i]] == 0:
                usernum.append("user" + str(i+1))

        except:
            pass

    return usernum

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    #compute overall accuracy
    oc = 0
    total = 0
    tmp_acc = 0
    for cm_i in range(len(cm)):
        tmp_acc += cm[cm_i][cm_i]
        for cm_j in range(len(cm)):
            total += cm[cm_i][cm_j]
    oc = float(tmp_acc) / float(total)

    tmp_recall = np.array(recall(cm))
    tmp_recall = tmp_recall.astype(float)
    tmp_precision =  np.array(precision(cm, oc))
    tmp_precision = tmp_precision.astype(float)
    cm_nn = cm
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    else:
        pass

    tmp_recall = tmp_recall[:, np.newaxis]
    cm = np.hstack((cm, tmp_recall))
    cm = np.vstack((cm, tmp_precision))

    class_x = []
    class_y = []

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes)+1)
    #add recall tick
    classes.append("recall")
    plt.xticks(tick_marks, classes)
    #delete recall tick
    classes.pop(len(classes)-1)
    #add precision tick
    classes.append("precision")
    plt.yticks(tick_marks, classes)
    #delete precision tick
    classes.pop(len(classes)-1)

    fmt = '2.1%' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color="black")
        if i<cm.shape[0]-1 and j<cm.shape[0]-1:
            plt.text(j, i, cm_nn[i, j],
                 weight = 'bold',
                 horizontalalignment='center',
                 verticalalignment='top',
                 color="black")
        else:
            pass

    plt.ylabel('True label', fontsize=12)
    plt.xlabel('Predicted label', fontsize=12)


def load_user_demo():
    user_demo = []
    data = pd.read_csv("user_demo.csv")
    user_demo_id = {}

    for i in range(len(data)):
        demo = {'age':0, 'gender':0, 'relationship':0, 'income':0, 'edu':0, 'location':0, 'industry':0, 'occupation':0}
        demo.update({"age": data["age"][i]})
        demo.update({"gender": data["gender"][i]})
        demo.update({"relationship": data["relationship"][i]})
        demo.update({"income": data["income"][i]})
        demo.update({"edu": data["edu"][i]})
        demo.update({"location": data["location"][i]})
        demo.update({"occupation": data["occupation"][i]})
        demo.update({"industry": data["industry"][i]})
        demo.update({"id": data["id"][i]})
        user_demo_id.update({data["id"][i]:0})

        user_demo.append(demo)

    return user_demo, user_demo_id

def recall(cnf):
    recall = []
    for i in range(len(cnf[0])):
        tmp_recall = float(cnf[i][i]) / float(sum(cnf[i]))
        recall.append(tmp_recall)

    return recall

def precision(cnf, oc):
    precision = []
    for i in range(len(cnf[0])):
        tmp = 0
        pre = 0
        for j in range(len(cnf[0])):
            tmp += cnf[j][i]
        if tmp == 0:
            tmp += 1

        pre = float(cnf[i][i]) / float(tmp)
        precision.append(pre)
    precision.append(oc)

    return precision


def main():
    #variable
    ### user_demo[id]['demographic'] ###
    print("Loading users' info")
    user_demo = []
    user_demo_id = {}
    user_demo, user_demo_id = load_user_demo()
    usernum = choose_user(user_demo_id)
    data_v4 = load_data_v4(usernum)
    data_v5 = load_data_v5(usernum)
    kms_data = []
    data_all = load_data_all(data_v4, data_v5)
    demo_list = ['age', 'gender', 'relationship']

    #class name
    class_name = {'age':["1", "2", "3", "4", "5", "6", "7"], 'gender':["1", "2", "3"], 'relationship':["1", "2", "3", "4", "5"]}


    #main
    '''
    #find the best depth in every clusters
    #hyper parameter settings
    #how many clusters?
    n_clusters = 6

    #which dataset?
    user_data = data_all

    # ------------------------------------------------------------------------#
    #kms model training
    for km4_i in range(len(user_data)):
        kms_data.append(user_data[km4_i])

    kms_model = KMeans(n_clusters, random_state=2018).fit(kms_data)

    kms_data = {}
    kms_demo = {}
    kms_user_list = {}
    kms_demo_label = {}
    demo_pred = {}
    demo_pred_res = {}
    demo_pred_score = {'age':[], 'gender':[], 'relationship':[], 'income':[], 'edu':[]}

    for c_num in range(n_clusters):
        kms_data.update({str(c_num):[]})
        kms_user_list.update({str(c_num):[]})
        kms_demo.update({str(c_num):{'age':[], 'gender':[], 'relationship':[], 'income':[], 'edu':[]}})
        demo_pred.update({str(c_num):{'age':[], 'gender':[], 'relationship':[], 'income':[], 'edu':[]}})



    for o_i in range(len(user_data)):
        kms_data[str(kms_model.labels_[o_i])].append(user_data[o_i]) #append user_daily
        kms_user_list[str(kms_model.labels_[o_i])].append(o_i)
        for demo_i in demo_list:
            kms_demo[str(kms_model.labels_[o_i])][demo_i].append(user_demo[o_i][demo_i])

    for k in range(1, 10001, 1):
        ### classifier choosing
        demo_pred_res.update({'age':[], 'gender':[], 'relationship':[], 'income':[], 'edu':[]})
        kms_demo_label.update({'age':[], 'gender':[], 'relationship':[], 'income':[], 'edu':[]})
        clf = LogisticRegression(C = k * 0.001, penalty='l1', solver='liblinear', random_state=2018)

        for c_num in range(n_clusters):
            for demo_i in demo_list:
                #f1-micro and f1-macro
                demo_pred_res[demo_i].extend(cross_val_predict(clf, kms_data[str(c_num)], kms_demo[str(c_num)][demo_i], cv=5))
                kms_demo_label[demo_i].extend(kms_demo[str(c_num)][demo_i])
                # print(demo_pred_res[str(c_num)][demo_i])

        for demo_i in demo_list:
            demo_pred_score[demo_i].append(f1_score(kms_demo_label[demo_i], demo_pred_res[demo_i], average='micro'))



    #print the best f1-micro with max depth
    print('')
    print('cnum: ' + str(n_clusters))
    for demo_i in demo_list:
        print(demo_i + ' /   Best testing score: ' + str(max(demo_pred_score[demo_i])) + ' /  C: ' + str(demo_pred_score[demo_i].index(max(demo_pred_score[demo_i]))+1))
    '''

    '''
    clf: logistic regression
    the best score:
    age /   Best testing score: 0.456 /  C : 5.188 / data_v5 / cnum = 5
    gender /   Best testing score: 0.675 /  C : 9.907 / data_v5 / cnum = 2
    relationship /   Best testing score: 0.498 /  C : 2.577 / data_v5 / cnum = 3
    '''

    #plot confusion matrix at best k of microF1
    best_k = [5.188, 9.907, 2.577]
    best_cnum = [5, 2, 3]
    best_data = [data_v5, data_v5, data_v5]

    for c in range(len(best_cnum)):
        kms_data = []
        user_data = best_data[c]
        n_clusters = best_cnum[c]
        for km4_i in range(len(user_data)):
            kms_data.append(user_data[km4_i])

        kms_model = KMeans(n_clusters, random_state=2018).fit(kms_data)

        kms_data = {}
        kms_demo = {}
        kms_user_list = {}
        demo_pred = {}
        demo_pred_res = {}
        demo_pred_score = {'age':[], 'gender':[], 'relationship':[]}

        for c_num in range(n_clusters):
            kms_data.update({str(c_num):[]})
            kms_user_list.update({str(c_num):[]})
            kms_demo.update({str(c_num):{'age':[], 'gender':[], 'relationship':[]}})
            demo_pred.update({str(c_num):{'age':[], 'gender':[], 'relationship':[]}})
            demo_pred_res.update({str(c_num):{'age':[], 'gender':[], 'relationship':[]}})

        for o_i in range(len(user_data)):
            kms_data[str(kms_model.labels_[o_i])].append(user_data[o_i]) #append user_daily
            kms_user_list[str(kms_model.labels_[o_i])].append(o_i)
            for demo_i in demo_list:
                kms_demo[str(kms_model.labels_[o_i])][demo_i].append(user_demo[o_i][demo_i])

        demo_pred = []
        demo_label = []

        clf = LogisticRegression(C = best_k[c], penalty='l1', solver='liblinear')

        for c_num in range(n_clusters):
            demo_pred.extend(cross_val_predict(clf, kms_data[str(c_num)], kms_demo[str(c_num)][demo_list[c]], cv=5))
            demo_label.extend(kms_demo[str(c_num)][demo_list[c]])

        cnf_matrix = confusion_matrix(demo_label, demo_pred)
        plt.figure()
        plt.tight_layout(pad=0.4, w_pad=1.0, h_pad=1.0)
        plot_confusion_matrix(cnf_matrix, classes=class_name[demo_list[c]], normalize=True, title=demo_list[c] + ' in C = ' + str(best_k[c]) + ' and cluster number = ' + str(n_clusters))
        plt.savefig('kms_lr_' + demo_list[c] + '.png', format='png', dpi=1000)
        #plt.show()






if __name__ == '__main__':
    main()
