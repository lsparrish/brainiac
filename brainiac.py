import hashlib, sys,base58

'''Brainiac is a simple key derivation tool for making brainwallets.

It is loosely related to scrypt, but simpler. It works as follows:

1. convert passphrase to a random-ish number with sha256 hash
function.
2. feed the result through again and concatenate the two. now we have
a 512-bit random-ish number.
3. keep doing this thousands of times, with the result expanding and
using up at least a few k of memory.
4. when you reach the desired level (256 KiB by default) stop and return
sha256 hash of the result.

The goal of this is to slow down dictionary attacks. Say your password
is 'the rain in spain lies mainly in the plains 93595' -- any attacker
with a decent dictionary will guess 'the rain in spain lies mainly in
the plains' pretty early on. Likewise, '93595' is very easy to brute
force.

If you were to trust sha256 by itself, even the combination of the two
would not be very good because chances are an attacker could step
through a gigantic dictionary many times per second using modern
hardware, for example an ASIC or FPGA. However, if they need to expand
to hundreds of kilobytes every single attempt, it becomes much harder
to efficiently parallelize these attempts, even on very advanced
equipment.

As with any kind of brain wallet, extreme caution is recommended in
choosing your passphrase. Do not choose something extremely short, or
that makes sense in english. Do not use a personal secret. Definitly
do not use any song lyrics. In fact, you are best off not choosing it
yourself at all. There is a perfectly good system for using dice to
pick your words. Raid your nearest board game for five physical dice
and use them to pick from a wordlist:
http://world.std.com/~reinhold/diceware.html

If for some reason you really, really do not want to use physical
dice, you may use an online javascript-based generator that uses mouse
movements as an entropy source to pick words from. For example:
http://rumkin.com/tools/password/diceware.php

Now all you have to do is memorize these eight to twelve randomly
picked words. It is easier than you might think! Write them down and
use them repeatedly. When you are sure you can remember them, you can
then destroy the paper.

'''
default_rounds = 1024
def keyderive(phrase, rounds=default_rounds, quiet=False):
    if not quiet:
        print str(rounds)+' rounds = '+str(256/8*rounds)+' bytes'
    s=''
    data=hashlib.sha256(phrase).digest()
    for i in range(rounds):
        data=s+data
        s=hashlib.sha256(data).digest()
        if not quiet and i % 1024 == 0: sys.stdout.write('.');sys.stdout.flush()
    return s,data

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
        key,data=keyderive(opts.phrase, rounds=rounds, quiet=opts.quiet)
        if opts.keep: keep(data)
        print key.encode('hex')
'''
    else:
        if not sys.stdin: print parser.format_help()
        else:
            line=sys.stdin.readline()
            key,data=keyderive(line.rstrip(), rounds=rounds, quiet=opts.quiet)
            if opts.keep: keep(data)
            print key.encode('hex')
'''
