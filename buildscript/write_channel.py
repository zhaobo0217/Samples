import argparse
import os
import shutil

import sys
import subprocess

def log(msg):
    sys.stderr.write('%s\n' % msg)

def write_channel(wall_path,input_apk_path, out_apk_path, channel_name):
    write_channel_cmd = "java -jar "+wall_path+" put -c " + channel_name + " " + input_apk_path + " " + out_apk_path
    log(write_channel_cmd)
    log("Writing channel information for channel \"" + channel_name + "\" with APK Signature Scheme v2...")
    subprocess.call(write_channel_cmd, shell=True, env=os.environ.copy())


def main():
    parser = argparse.ArgumentParser(prog="android channel tool")
    subparsers = parser.add_subparsers(dest="subcmd")
    # sign sub command
    sign_parser = subparsers.add_parser("gen", help="generate apks for channels in Config")
    sign_parser.add_argument("-i", "--input", help="input file path", required=True)
    sign_parser.add_argument("-w", "--wall_path", help="wall-cli-all.jar", required=True)
    sign_parser.add_argument("-o", "--output", help="output directory", required=True)
    sign_parser.add_argument("-c", "--channels", help="channels split with ,", required=True)

    args = parser.parse_args()
    print(args)
    list = args.channels.split(',')
    for channel in list:
        dest_apk = os.path.join(args.output, 'release_' + channel + '.apk')
        shutil.copyfile(args.input, dest_apk)
        write_channel(args.wall_path,args.input, dest_apk, channel)


if __name__ == '__main__':
    main()