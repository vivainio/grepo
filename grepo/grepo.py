import pickleshare
import args
import os, glob
from subprocess import *
import tempfile, re


db = pickleshare.PickleShareDB("~/.grepo")

root = db.get('root', None)

def here_c(args):
    db['root'] = os.getcwd()

def runpeco(input):
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(input)
    tf.close()
    p = Popen(['peco', tf.name], stdout = PIPE)
    out = p.stdout.read()
    os.unlink(tf.name)

    return out

def parents(pth):
    cur = pth
    while 1:
        c2 = os.path.dirname(cur)
        if c2 == cur:
            return
        cur = c2
        yield cur

def search_str(pats, files):
    #print pats,'in', files
    res = set()

    for f in files:
        for s in pats:
            if s.lower() in open(f).read().lower():
                res.add(f)
    #print "found",res
    return res

def more_info(fname):
    fname = os.path.abspath(fname)
    print fname
    bname = os.path.basename(fname)

    pats = [bname]

    refs = set()

    for p in parents(fname):
        look = glob.glob(p + '/*.csproj') + glob.glob(p + '/*.sln')
        found = search_str(pats, look)
        if found:
            pats.extend(os.path.basename(f) for f in found)
            refs.update(found)
        #print p, look, found

    for r in refs:
        print r

def peco_and_edit(input):
    top = db['top']
    lines = runpeco(input).splitlines()
    for l in lines:
        fname, line, text = l.split(':', 2)
        print "pick:", fname
        call(['code', '-g', fname + ':' + line], shell=True)
        more_info(fname)


def grep_c(args):
    os.chdir(root)
    out = os.popen('git grep -n ' + args.pattern).read()
    #print out
    db['grepoutput'] = out
    save_top()
    peco_and_edit(out)


def pick_c(args):
    os.chdir(db['top'])
    peco_and_edit(db['grepoutput'])

def checkout_by_git_cmd(cmd):

    out = os.popen(cmd).read()
    lines = runpeco(out).splitlines()
    branch = lines[0].strip()
    print branch
    assert len(branch.split()) == 1
    branch = branch.replace('remotes/origin', '')
    os.system("git checkout %s" % branch)

def checkout_c(args):
    checkout_by_git_cmd("git branch -a")

def recent_c(argn):
    checkout_by_git_cmd("""git for-each-ref --count=30 --sort=-committerdate refs/heads/ --format="%(refname:short)" """)

def save_top():
    db['top'] = os.popen('git rev-parse --show-toplevel').read().strip()


def scan_c(args):
    pat = args.pattern
    out = os.popen('git grep --break --color --heading -p -n --full-name -C 2 ' + pat).read()

    ndx = 0

    for_pick = []
    filechunks = re.split("\n\n", out)
    for chunk in filechunks:
        if chunk == '':
            print "No match"
            return
        fname, cont = chunk.split("\n", 1)
        ndx+=1
        for_pick.append('%s:0: hit #%s' % (fname, ndx))
        print '\n\n  ************ %s (%d) ************\n' % (fname, ndx)
        print cont
    db['grepoutput'] = '\n'.join(for_pick)
    save_top()


def main():
    args.init()

    args.sub('here', here_c, help = 'Set current dir as prjroot')
    s = args.sub('g', grep_c, help = 'Grep the project')
    s.arg("pattern", type=str)
    sc = args.sub('sc', scan_c, help ='Search with context')
    sc.arg("pattern", type=str)

    args.sub('p', pick_c, help = 'Use peco to quick pick one of the earlier choices')
    args.sub('co', checkout_c, help = "select and check out a branch")
    args.sub('r', recent_c, help="select and check out a recently used branch")

    args.parse()


def test():
    pick_c(None)

#test()
if __name__ == "__main__":
    main()
