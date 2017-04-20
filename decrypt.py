import sys
import os
import subprocess
import time

# call padding oracle and captrue the result
def valid_oracle(input_list):
    with open('test', 'wb') as output:
        for item in input_list:
            output.write(chr(int(item, 0)))
    output.close()

    result = None
    try:
        result = subprocess.check_output(["./oracle", "test"])
        return result
    except subprocess.CalledProcessError as grepexc:
        print "error code", grepexc.returncode, grepexc.output
        sys.exit(1)


def d_byte(yn, previous_yn):
    # generate a random block r
    r = [hex(ord(os.urandom(1))) for i in xrange(15)]
    r.append(None)
    concatenate = [r[i] for i in xrange(15)]
    for i in xrange(15, 32):
        concatenate.append(None)

    Dyn_list = [None for i in xrange(16)]
    Xn_list = [None for i in xrange(16)]

    flag = False  # keep increment i until the padding oracle says yes
    i = 0
    while not flag:
        r[15] = hex(i)  # last byte = i
        concatenate[15] = hex(i)

        # concatenate r and yn
        for j in xrange(16, 32):
            concatenate[j] = yn[j-16]

        # if the padding is not correct (i.e. result = 0)
        if valid_oracle(concatenate) == "0":
            i += 1
        else:
            # Replace r1 with any other byte and ask the oracle if the new (r|yN) has valid padding.
            # If the padding oracle returns "yes", similarly replace r2.

            # flag4: flag for step 4
            # Repeat until either we have finished replacing r15 and the oracle always returned \yes",
            # or the oracle has returns "no" while we were replacing some rk
            flag4 = True
            index = -1
            while flag4:
                for j in xrange(16):
                    x = hex(ord(os.urandom(1)))
                    concatenate[j] = x
                    if valid_oracle(concatenate) == '0':
                        flag4 = False
                        index = j
                        break

            Dyn = None
            # If the oracle always returned "yes" in Step 4
            if flag4:
                Dyn = i ^ 1
            # If the oracle returned "no" when we replaced rk
            else:
                Dyn = i ^ (17 - (index+1))
            Dyn_list[15] = Dyn
            Xn_list[15] = Dyn ^ int(previous_yn[15], 0)
            flag = True
            break

    for k in xrange(14, -1, -1):
        block_r = [r[i] for i in xrange(k)]
        for i in xrange(k, 16):
            block_r.append(None)

        # concatenate r and Dyn
        for j in xrange(1, 16-k):
            block_r[k+j] = hex(Dyn_list[k+j] ^ (17-k-1))

        flag = False  # keep increment i until the padding oracle says yes
        i = 0
        while not flag:
            block_r[k] = hex(i)  # last byte = i

            # concatenate r and y
            block_concatenate = [block_r[j] for j in xrange(16)]
            for j in xrange(16):
                block_concatenate.append(None)
            for j in xrange(16):
                block_concatenate[16+j] = yn[j]

            # if the padding is not correct (i.e. result = 0)
            if valid_oracle(block_concatenate) == "0":
                i += 1
            else:
                Dynk = i ^ (17-k-1)
                Dyn_list[k] = Dynk
                Xn_list[k] = Dynk ^ int(previous_yn[k], 0)
                flag = True
                break
    return Xn_list

# main function
a = time.time()
ciphertext = sys.argv[1]
f = open(ciphertext, "rb")
content = []
final_result = []

block = f.read(16)
IV = [hex(ord(c)) for c in list(block)]
while True:
    block = f.read(16)
    if block != "":
        temp = [hex(ord(c)) for c in list(block)]
        content.append(temp)
    else:
        break

# decrypt the file
for i in xrange(len(content)-1, 0, -1):
    final_result.insert(0, d_byte(content[i], content[i-1]))
final_result.insert(0, d_byte(content[0], IV))

# print "result:", final_result
print ''.join([chr(item) for sublist in final_result for item in sublist])

f.close()
b = time.time()
# print "time used:", b-a
