__author__ = "Jordan Sanders"
def recall(gold, test, at):
    rel_ret = 0.0
    for doc in gold:
        if doc in test[:at]:
            rel_ret+=1
    rel_docs = len(gold)

    return rel_ret/rel_docs

def precision(gold, test, at):
    rel_ret = 0.0
    for doc in gold:
        if doc in test[:at]:
            rel_ret+=1

    return rel_ret/min(len(test),at)

def main():
    test = list()
    gold = list()

    for line in open("relevance.txt", "r").readlines():
        line = line.split(" ")
        if len(gold) < int(line[0]):
            gold.append(list())
        gold[int(line[0])-1].append(int(line[1]))

    for line in open("output.txt", "r").readlines():
        line = line.split(" ")
        if len(test) < int(line[0]):
            test.append(list())
        test[int(line[0])-1].append(int(line[1]))

    N = [10,50,100,500]
    for i in range(len(test)):
        print "Query " + str(i+1)
        for n in N:
            print n
            print "Recall: " + str(recall(gold[i],test[i],n))
            print "Precision: " + str(precision(gold[i],test[i],n))
            print

    print "Averages"
    for n in N:
        total_recall = 0.0
        total_precision = 0.0
        for i in range(len(test)):
            total_recall += recall(gold[i],test[i],n)
            total_precision += precision(gold[i],test[i],n)
        print n
        print "Recall: " + str(total_recall/10)
        print "Precision: " + str(total_precision/10)



if __name__ == '__main__':
    main()
