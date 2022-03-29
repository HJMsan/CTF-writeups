keys = [4, 0xe, 4, 1, 4, 0xb, 4, 0, 3, 0x11, 2, 0xc, 3, 0x11, 4, 0xf, 4, 5, 4, 0x15, 4, 0xf, 3, 0x13, 2, 0xc, 3, 0x11, 1, 0x19, 3, 0x15, 3, 0x11, 3, 0x14, 1, 0x19, 4, 0xc, 1, 0x17, 3, 0x11, 4, 0x13, 3, 0x18]
flag = [i for i in 'a'*32]

mode = 1
ik_max = 4
jl_max = 5
keys_index1 = 0
key_index2 = 0
input_index = 0
while (((0 < ik_max or (0 < jl_max)) and (-1 < ik_max)) and (-1 < jl_max)):
    if (mode == 1) :
        for i in range(0, ik_max):
            flag[input_index] = chr(keys[keys_index1 * 8 + key_index2 * 2] * 0x1a + keys[keys_index1 * 8 + key_index2 * 2 + 1])
            
            input_index = input_index + 1
            key_index2 = key_index2 + 1
        
        ik_max = ik_max + -1
        keys_index1 = keys_index1 + 1
        key_index2 = key_index2 + -1
        mode = 2
    
    elif (mode == 2) :
        for i in range(0, jl_max):
            flag[input_index] = chr(keys[keys_index1 * 8 + key_index2 * 2] * 0x1a + keys[keys_index1 * 8 + key_index2 * 2 + 1])
            keys_index1 = keys_index1 + 1
            input_index = input_index + 1
            
        jl_max = jl_max + -1
        keys_index1 = keys_index1 + -1
        key_index2 = key_index2 + -1
        mode = 3
    
    elif (mode == 3) :
        for i in range(0, ik_max):
            flag[input_index] = chr(keys[keys_index1 * 8 + key_index2 * 2] * 0x1a + keys[keys_index1 * 8 + key_index2 * 2 + 1])
            input_index = input_index + 1
            key_index2 = key_index2 + -1
            
        ik_max = ik_max + -1
        keys_index1 = keys_index1 + -1
        key_index2 = key_index2 + 1
        mode = 4
    
    elif (mode == 4) :
        for i in range(0, jl_max):
            flag[input_index] = chr(keys[keys_index1 * 8 + key_index2 * 2] * 0x1a + keys[keys_index1 * 8 + key_index2 * 2 + 1])
            input_index = input_index + 1
            keys_index1 = keys_index1 + -1
        
        jl_max = jl_max + -1
        keys_index1 = keys_index1 + 1
        key_index2 = key_index2 + 1
        mode = 1
    
print("".join(flag))