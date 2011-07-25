#!/usr/bin/env python
import subprocess
import os
import sys

#########################################################
###################### Settings #########################
#########################################################
package = "python-collate"
package_version = "0.2.99-0"
ppa_version = "1"
#########################################################
#########################################################

#########################################################
# Functions
#########################################################
def p(cmd):
    print "> %s" % cmd
    pipe = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdout=pipe, stderr=pipe, stdin=pipe)
    stdout, stderr = p.communicate()
    return p.returncode, stdout.strip(), stderr.strip()

def clean():
    global start, package
    os.chdir(start)
    cmd = "rm %s*.changes %s*.tar.gz %s*.dsc %s*.upload  %s*.build" % ((package,) * 5)
    p(cmd)

def fail(out):
    status, stdout, stderr = out
    if status != 0:
        print "#" * 24
        print stdout
        print stderr
        print "#" * 24
        clean()
        sys.exit()
    return out

#########################################################
# Start
#########################################################
dput_cfg = os.path.join(os.getcwd(), "dput.cf")

start = os.getcwd()
clean()

hg_dir = "python-collate"
if not os.path.isdir(hg_dir):
    p("hg clone https://python-collate.googlecode.com/hg/ %s" % hg_dir)
os.chdir(hg_dir)

p("hg revert --all")
p("hg pull")
p("hg up -C")

rev = p("hg tip")[1].split()[1].replace(":","~")
date = p("date -R")[1]

debian = "debian_quodlibet"
for release in "lucid maverick natty oneiric".split():
    p("rm -R debian")
    p("cp -R ../%s ." % debian)
    p("mv %s debian" % debian)

    changelog = "debian/changelog"
    t = open(changelog).read()
    t = t.replace("%ver%", package_version)
    t = t.replace("%rev%", rev)
    t = t.replace("%ppa%", ppa_version)
    t = t.replace("%dist%", release)
    t = t.replace("%date%", date)
    open(changelog, "w").write(t)

    fail(p("debuild -uc -us -S -I -rfakeroot"))

p("rm -Rf debian")
os.chdir("..")
fail(p("debsign %s*.changes %s*.dsc" % ((package,) * 2)))

dput = "dput --config '%s'" % dput_cfg
#fail(p("%s stable %s*.changes" % (dput, package)))
fail(p("%s unstable %s*.changes" % (dput, package)))
#fail(p("%s experimental %s*.changes" % (dput, package)))

clean()
