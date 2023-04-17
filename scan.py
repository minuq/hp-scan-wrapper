#!/bin/python

'''Usage:
  scan (-o <FILE> | --output=FILE)              Defaults to scanner bed
  scan [-a] [-d] [-r] [-o <FILE> | --output=FILE]

Options:
  -h --help                                     Show this screen.
  -d, --duplex                                  Enables duplex scan
  -a, --adf                                     Scans from adf
  -o FILE, --output=FILE                        File to output to, defaults to ~/Documents/Scans/<output>
  -r, --rsync                                   OCR
'''

from docopt import docopt
from datetime import datetime
from time import sleep
import subprocess

def main():
  options = docopt(__doc__)
  filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  parameters = '--mode color'

  if options['--output']:
    print(f'Scanning to {options["--output"]}.')
    filename = options['--output']
    if filename[-4:] == ".pdf":
      filename = filename[0:len(filename)-4]

  if options['--adf']:
    parameters += ' --adf'

  if options['--duplex']:
    cmd = f'hp-scan {parameters} --output "/tmp/{filename}_odd.pdf" $2 > /dev/null'
    print('Scanning odd pages.')
    subprocess.run(cmd, shell=True)
    input('Press enter to continue...')

    cmd = f'hp-scan {parameters} --output "/tmp/{filename}_even.pdf" $2 > /dev/null'
    print('Scanning even pages')
    subprocess.run(cmd, shell=True)

    A=f'"/tmp/{filename}_odd.pdf"'
    B=f'"/tmp/{filename}_even.pdf"'
    output=f'"$HOME/Documents/Scans/{filename}.pdf"'
    pdftk = f'pdftk A={A} B={B} shuffle A Bend-1 output {output}'
    subprocess.run(pdftk, shell=True)
  else:
    cmd = f'hp-scan {parameters} --output "$HOME/Documents/Scans/{filename}.pdf" $2 > /dev/null'
    print(cmd)
    subprocess.run(cmd, shell=True)

  if options['--rsync']:
    cmd = f'/usr/bin/rsync --progress --chmod=755 --remove-source-files "$HOME/Documents/Scans/{filename}.pdf" $user@$host:/path/to/ocrmypdf/input/'
    subprocess.run(cmd, shell=True)


if __name__=='__main__':
  main()
