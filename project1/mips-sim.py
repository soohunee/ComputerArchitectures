# -*- coding: utf-8 -*-
import sys
binfile = sys.argv[1]

List = list()
with open(binfile, "rb") as f:
    while True:
        byte = f.read(1)
        
        if not byte:
            break
        List.append(bin(ord(byte))) 

        
dst_funct = {'100000':'add','100001':'addu','100100':'and','100111':'nor',
             '100101':'or','100010':'sub','100011':'subu','100110':'xor',
             '101010':'slt','101011':'sltu'}
dts_funct={'000100':'sllv','000111':'srav','000110':'srlv'}
st_funct={'011010':'div','011011':'divu','011000':'mult','011001':'multu'}
ds_funct={'001001':'jalr'}
s_funct={'001000':'jr','010001':'mthi','010011':'mtlo'}
d_funct={'010000':'mfhi','010010':'mflo'}
dt_shamt_funct = {'000000':'sll','000011':'sra','000010':'srl'}
syscall_funct={'001100' : 'syscall'}
st_label_opcode={'000100':'beq','000101':'bne'}
t_address_opcode={'100000':'lb','100100':'lbu','100001':'lh','100101':'lhu',
                  '100011':'lw','101001':'sh','101011':'sw','101000':'sb'}
ts_opcode_s={'001000':'addi','001100':'andi','001101':'ori','001110':'xori',
             '001010':'slti'}
ts_opcode_us={'001001':'addiu','001011':'sltiu'}
target_opcode = {'000010':'j','000011':'jal'}
t_imm_opcode={'001111':'lui'}


def toHex(s):
    binary_value = int('0b'+s, 2)
    hex_value = hex(binary_value)
    hex_string = str(hex_value)[2:]
    if len(hex_string) == 2:
        return hex_string
    else:
        hex_string = '0'+hex_string
        return hex_string

def toDecStr_2(a, n):
    result = 0
    if a[0] == '0':
        return str(int('0b'+a, 2))
    else:
        neg = a.index('1')
        rest = int('0b' + a[neg+1:], 2)
        neg = pow(2,(n-1)-neg) * (-1)
        a = a[neg+1:]
        result += neg + rest
        return str(result)

        
for i in range(len(List)):
    item = List[i]
    item = item[2:]
    numZero = 8 - len(item)
    item = '0'*numZero + item
    List[i] = item
    
insts = list()
hex_list = list()
for i in range(0,len(List),4):
    insts.append(List[i]+List[i+1]+List[i+2]+List[i+3])
    hex_list.append(toHex(List[i])+toHex(List[i+1])+toHex(List[i+2])
                    +toHex(List[i+3]))

for idx, inst in enumerate(insts):
    result = ""
    result += 'inst ' + str(idx) + ': ' + hex_list[idx] + ' '
    #print('inst : ', inst)
    opcode = inst[:6]
    rs = inst[6:11] # 5bits
    rt = inst[11:16] # 5bits
    rd = inst[16:21] # 5bits
    shamt = inst[21:26] # 5bits
    funct = inst[26:] # 6bits
    if opcode == '000000' : #R-type instructions
        if funct in dst_funct.keys() :
            result += dst_funct[funct]+' $'+str(int('0b'+rd, 2))+', $'+str(int('0b'+rs, 2))+', $'+str(int('0b'+rt, 2))
            print(result)
        elif funct in dts_funct.keys():
            result += dts_funct[funct]+' $'+str(int('0b'+rd, 2))+', $'+str(int('0b'+rt, 2))+', $'+str(int('0b'+rs, 2))
            print(result)
        elif funct in st_funct.keys():
            result += st_funct[funct]+' $'+str(int('0b'+rs, 2))+', $'+str(int('0b'+rt, 2))
            print(result)
        elif funct in ds_funct.keys():
            result += ds_funct[funct]+' $'+str(int('0b'+rd, 2))+', $'+str(int('0b'+rs, 2))
            print(result)
        elif funct in s_funct.keys():
            result += s_funct[funct]+' $'+str(int('0b'+rs, 2))
            print(result)
        elif funct in d_funct.keys():
            result += d_funct[funct]+' $'+str(int('0b'+rd, 2))
            print(result)
        elif funct in dt_shamt_funct.keys():
            result += dt_shamt_funct[funct]+' $'+str(int('0b'+rd, 2))+', $'+str(int('0b'+rt, 2))+', '+str(int('0b'+shamt, 2))
            print(result)
        elif funct in syscall_funct.keys():
            result += syscall_funct[funct]
            print(result)
        else:
            result += 'unknown instruction'
            print(result)
    else: #I-type instructions
        rs = inst[6:11] # 5bits
        rt = inst[11:16] # 5bits
        off_imm = inst[16:] # 16bits
        if opcode in st_label_opcode.keys(): #I-type instructions
            result += st_label_opcode[opcode]+' $'+str(int('0b'+rs, 2))+', $'+str(int('0b'+rt, 2)) + ', ' + toDecStr_2(off_imm,16)
            print(result)
        elif opcode in t_address_opcode.keys():
            result += t_address_opcode[opcode]+' $'+str(int('0b'+rt, 2))+', '+str(int('0b'+off_imm, 2)) + '($' + str(int('0b'+rs, 2)) + ')'
            print(result)
        elif opcode in ts_opcode_s.keys():
            result += ts_opcode_s[opcode]+' $'+str(int('0b'+rt, 2))+', $'+str(int('0b'+rs, 2)) + ', ' + toDecStr_2(off_imm,16)
            print(result)
        elif opcode in ts_opcode_us.keys():
            result += ts_opcode_us[opcode]+' $'+str(int('0b'+rt, 2))+', $'+str(int('0b'+rs, 2)) + ', ' + toDecStr_2(off_imm,16)
            print(result)
        elif opcode in t_imm_opcode.keys():
            result += t_imm_opcode[opcode]+' $'+str(int('0b'+rt, 2))+', ' + toDecStr_2(off_imm,16)
            print(result)
        else: #j-type instructions
            target = inst[6:] # 26bits        
            if opcode in target_opcode.keys():
                result += target_opcode[opcode]+ ' ' + toDecStr_2(target,26)
                print(result)
            else :
                result += 'unknown instruction'
                print(result)
            
            
            
