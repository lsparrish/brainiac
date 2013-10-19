import hashlib, sys, base58

'''Brainiac is a simple key derivation tool for making brainwallets.
Use at your own discretion. (Diceware strongly recommended.)'''

default_rounds = 1024
def derivekey(passphrase,rounds=default_rounds):
    if not quiet:
        print str(rounds)+' rounds = '+str(256/8*rounds)+' bytes'
    def getdigest(message):
        return hashlib.sha256(x).digest()
    message=getdigest(passphrase)
    for i in range(rounds):
        result=getdigest(message)
        message=result+message
        if not quiet and i % 1024 == 0: sys.stdout.write('.');sys.stdout.flush()
    return result,data

def keep(data,filename='output'):
    f=open(filename,'w')
    f.write(data)
    f.close()

def hexwif(hexinput):
    '''hex string -> wif string'''
    step1=hexinput
    step2='80'+step1
    step3=hashlib.sha256(step2.decode('hex')).digest().encode('hex')
    step4=hashlib.sha256(step3.decode('hex')).digest().encode('hex')
    step5=step3[0:8]
    step6=step2+step5
    return base58.b58encode(step6.decode('hex'))

if __name__ == '__main__':
    import optparse
    parser=optparse.OptionParser()
    parser.add_option("-p", "--phrase", dest='phrase',
                      action='store',
                      help='phrase to use for your brainwallet')
    parser.add_option("-r", "--rounds", dest='rounds',
                      action='store',
                      help='number of rounds to expand the key by (powers of 2 preferred)')
    parser.add_option("-k", "--keep-output", dest='keep',
                      action='store_true',
                      help='keep a copy of the generated data')
    parser.add_option("-q", "--quiet", dest='quiet',
                      action='store_true',
                      help='do not print anything except the key')
    opts, args = parser.parse_args()
    if opts.rounds:
        rounds=int(opts.rounds)
    else:
        rounds=default_rounds
    if opts.phrase:
        key,data=derivekey(opts.phrase, rounds=rounds, quiet=opts.quiet)
        if opts.keep: keep(data)
        print key.encode('hex')
