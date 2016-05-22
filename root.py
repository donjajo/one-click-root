#!/usr/bin/python3
import subprocess
from getpass import getuser
import os
import sys
import time
try:
	from apt import Cache
except ImportError:
	print( 'Install python3-apt to use this package' )
	sys.exit( 1 )

def is_installed( package ):
	cache = Cache()
	return cache[ package ].is_installed if package in cache else False

if( getuser() != 'root' ):
	print( 'Run as root' )
	sys.exit( 1 )

print( 'Checking dependancies...' )
if( not is_installed( 'fastboot' ) and not is_installed( 'android-tools-fastboot' ) ):
	print( 'Install <android-tools-fastboot> or <fastboot> package to use this' )
	sys.exit( 1 )
elif( not is_installed( 'adb' ) and not is_installed( 'android-tools-adb' ) ):
	print( 'Install <adb> or <android-tools-adb> to use this tool' )
	sys.exit( 1 )
print( 'Dependancy check passed!' )

print( '\nMaking sure magic, busybox, supersu.tgz and installer exists...' )
if( not os.path.isfile( 'magic' ) and not os.path.isfile( 'busybox' ) and not os.path.isfile( 'supersu.tgz' ) and not os.path.isfile( 'installer' ) ):
	print( """\n\nRooting interrupted to avoid bricking, make sure these files exist \n\n=> {0}\n=>{1}\n=>{2}\n=>{3}\n""".format( os.path.join( os.getcwd(), 'magic' ), os.path.join( os.getcwd(), 'busybox' ), os.path.join( os.getcwd(), 'supersu.tgz' ), os.path.join( os.getcwd(), 'installer' ) ) )
	sys.exit()
time.sleep( 2 )
print( 'Rooting...' )

print( '\nPassing over to ADB...' )
subprocess.check_call( [ 'adb', 'kill-server' ] )
try:
	subprocess.call( [ 'adb', 'wait-for-devices' ] )
	subprocess.check_call( [ 'adb', 'reboot', 'bootloader' ] )
	print( 'Rebooting device...' )
	time.sleep( 5 )
	print( 'Waiting for fastboot' )
	time.sleep( 25 )

	subprocess.call( [ 'fastboot', 'flash', '/system/bin/resize2fs', 'magic' ] )
	subprocess.call( [ 'fastboot', 'flash', '/system/bin/tune2fs', 'busybox' ] )
	subprocess.call( [ 'fastboot', 'flash', '/system/bin/partlink', 'supersu.tgz' ] )
	subprocess.call( [ 'fastboot', 'oem', 'start_partitioning' ] )
	subprocess.call( [ 'fastboot', 'flash', '/system/bin/logcat', 'installer' ] )
	subprocess.call( [ 'fastboot', 'oem', 'stop_partitioning' ] )
	time.sleep( 2 )

	subprocess.call( [ 'fastboot', 'reboot' ] )
	subprocess.call([ 'adb', 'kill-server' ] )
	sys.exit( 1 )
except subprocess.CalledProcessError:
	sys.exit( 1 )