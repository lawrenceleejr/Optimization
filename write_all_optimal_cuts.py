tag = 'small_extended'
supercuts_file = 'supercuts_'+tag+'.json'
output_dir = 'outputHash_'+tag

import csv,glob,re,json
def get_hashes():
  mdict = {}
  with open('mass_windows.txt', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    m = list(reader)
    mdict = {l[0]: [l[1],l[2],l[3]] for l in m}

  def masses(did):
    mlist = mdict[did]
    mglue = mlist[0]
    mstop = mlist[1]
    mlsp = mlist[2]
    return mglue,mstop,mlsp

  sigdir = 'significances_' + tag
  filenames = glob.glob(sigdir+'/s*.b*.json')
  regex = re.compile(sigdir+'/s(\d{6}).b.*.json')
  dids = []
  sigs = []
  for filename in filenames:
    with open(filename) as json_file:
      sig_dict = json.load(json_file)
      entry = sig_dict[0]
      max_sig = entry['hash']
      sigs.append(max_sig)
      did = regex.search(filename)
      dids.append(did.group(1))

  plot_array=[]
  for did,sig in zip(dids,sigs):
    mgluino,mstop,mlsp = masses(did)
    row = [mgluino,mstop,mlsp,sig]
    if int(mstop) == 5000: plot_array.append(row)

  return plot_array

import subprocess
array = get_hashes()
bashCommand = 'python optimize.py hash '
for row in array:
  h = row[3]
  bashCommand += h + ' '
bashCommand += '--supercuts ' + supercuts_file + ' -b'
bashCommand += ' -o ' + output_dir
subprocess.call(bashCommand,shell=True)

import numpy
nparray = numpy.array(array)
import pdb
numpy.savetxt('output/mass_windows_hashes_'+tag+'.txt',nparray,delimiter='\t',fmt='%s')
