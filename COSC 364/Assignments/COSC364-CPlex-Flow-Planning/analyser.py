import subprocess
import time
import json

NO_FILES = 9


def CPLEX(filename):
    '''run CPLEX to solve the problem of given lp file'''
    # args1 = ['/Users/mac/Desktop/364/a2/cplex', '-c', 'read /Users/mac/Desktop/364/a2/' + filename, 'optimize',
    # 'display solution variable -']
    args1 = ['C:/Programs/Cplex/cplex/bin/x64_win64/cplex.exe', '-c', 'read ' + filename, 'optimize',
             'display solution variable -']

    time1 = time.time()
    process1 = subprocess.Popen(args1, stdout=subprocess.PIPE)

    output, error = process1.communicate()
    time2 = time.time()
    execution_time = time2 - time1

    # print('Execution_time: '+str("%.5f" % (execution_time))+'seconds')
    result = output.decode("utf-8").split()

    start = result.index("Incumbent")
    load = {}
    links = []
    link_count = 0
    cappacities = {}
    cappacities = {'max': [0, []]}
    max_cappacity = 0.0
    for i in range(1, NO_FILES):
        load[i] = float(0)
    for n in result[start:]:
        if n.startswith('x'):
            transit_node = int(n[2])
            x_index = result.index(n)
            load[transit_node] += float(result[x_index + 1])
        if (n.startswith('c') or n.startswith('d')) and len(n) == 3:
            capp_index = result.index(n)
            cappacity = float(result[capp_index + 1])
            if cappacity > 0:
                link_count += 1
                links.append(n)
            if cappacity == max_cappacity:
                cappacities['max'][1].append(n)
            if cappacity > max_cappacity:
                max_cappacity = cappacity
                cappacities['max'][0] = max_cappacity
                cappacities['max'][1] = [n]

    result = 'Execution_time: ' + str("%.5f" % (execution_time)) + 'seconds\n' + 'Load on transit nodes: ' + json.dumps(
        load) + '\n' + 'Maximum cappacity: ' + json.dumps(cappacities) + '\nNon-zero capacity link count: ' + str(
        link_count) + '\nNon-zero capacity links: ' + ' '.join(links)
    return result


def main():
    f = open('./Logs/analyser.txt', 'w')
    for n in range(3, NO_FILES):
        filename = 'Path{}.lp'.format(n)
        print(filename)
        result = CPLEX(filename)
        f.write(filename + "\n" + result + "\n\n")
    f.close()

    f = open('./Logs/_analyser.txt', 'w')
    for n in range(3, NO_FILES):
        filename = 'Path{}.lp'.format(n)
        f.write("\n\n" + filename + "\n\n\n")
        for i in range(1, 10):
            print(filename)
            result = CPLEX(filename)
            f.write(result + "\n\n")
    f.close()


main()
