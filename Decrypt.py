

import sys,os
import rsa
import arc4 




RSA_key ="""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAxTC/Igjuybr1QbQ1RmD9YxpzVnJKIkgvYpBrBzhsczHQ8WeC7ikmC5jTbum1eCxTFTxvtnONEy2qDbnSS5fbK/lxYExj6aDLKzQxXCOVSdSQCesWg1i5AAdUC9S246sdS9VKxT0QL24I+SG+ixckBhcB+ww6z47ACegoH0aLDwvRvehZYcc1qFr1lhRXQpHunrlg4WRphH5xBbszOI+dFRDOpprnbN56CHoLb0q1SzzV3ZFAFF6Df68Pux1wMHwEXbULRHo5AIZJPJq8L9ThWVsj6v42jAjJQ8m8bRh0+Jz4RohkWwPgL+VFxDG2AiiCU5/yLNoQX0JM9VWBxy6Z3QIDAQABAoIBADi/KoH06CMNtn7OCXbTepgGiKKcCVGMTHak8OgHCM6ty19tVnSLSvOTa2VDxIFs4AwAdHWhEzwtq/5/N1GhxeUFx+balPYq28z3HC1T4CZ7EWiJStVJtxOXCEzPTkJ+f9PO8dGJHRtJIzPuzhLg+fD2tg81GceZYRJ4yPMXLfWKA5DmGkRv/1Usq5zvMClLdrmw/q2rnCbRLdeEEAzSAi9kqsnEaZKfCbXb/gby+bUwAgn7mxs+CJ611hzD/r2w9dgXkaUJYuKRRv+BGlQHBRQ7hXogkIzeaGqmw8M3xko7xzADsytFYxt2Kthuww2YV4E6Q1Hl4bBW0q+gw+jSolECgYEA0Tnns+LaqMd5KCQiyWlCodQ2DtOMOefhIrJbRhdAkAq6FtVICxkLnIJL0gmo4T/zDaMr8vsn7Ck+wLjXUsYt1/EulLtVnuH76FU0PkjJqBdre5Gjf23/YGHW7DJEoH3p/7DIgV4+wXPu6dD+8eECqwm1hLACOxkfZnOFZ1VGxeMCgYEA8UYHjaA69ILlz0TzDzoRdTmam6RDqjsVO/bwaSChGphV0dicKue25iUUDj87a1yLU5Nqt0Kt0w1FL/iile1Eu4fe4ryukPGw2jAZh/xq7i2RRSFLXim5an9AbBVQ55478AJasTaIOSoODgBspsBLShnXQRKEfwYPv2GthhcJLT8CgYAssRDERQ3uBYXkxCtGGJzqEnllm1yVtelKTwzeIPNikVgErpRQAo6PZOmrOPMBAnb5j8RAh9OUR48m/ZTJEpoSSWtoy8dTQ/RaQXECaOviYvZLk+V3v9hQDzYoh+hO2/aS7oE12RrQmeILwd/jbOvz+wPyDuK7GvexG7YAR5/xfwKBgQCA8p6C0MnxeCv+dKk60BwYfKrm2AnZ5y3YGIgwh2HS5uum9Y+xVpnnspVfb+f/3zwPdNAqFZb1HziFBOtQGbkMSPeUUqcxjBqq4d4jUYKMvQnQ2pR/ROl1w4DYwyO0RlteUMPLxotTkehlD1ECZe9XMSxb+NubT9AGxtuIuLMM3QKBgGl0mYCgCVHi4kJeBIgabGqbS2PuRr1uogAI7O2b/HQh5NAIaNEqJfUaaTKS5WzQ6lJwhRLpA6Un38RDWHUGVnEmm8/vF50f74igTMgSddjPwpWEf3NPdu0ZUIfJd1hd77BYLviBVYft1diwIK3ypPLzhRhsBSp7RL2L6w0/Y9rf
-----END RSA PRIVATE KEY-----
"""

progressBar = ['-', '\\', '|', '/']
progressBarCount = 0

rsaKey = rsa.PrivateKey.load_pkcs1(RSA_key)

def isEncrypt(filePath):
	if filePath[-8:] == "WannaRen":
		return 1
	return 0

def rc4Decode(data,key):
	rc41 = arc4.ARC4(key)
	decryptData = rc41.decrypt(data)
	return decryptData

def DecryptFile(filePath):
	global progressBarCount

	if False == os.path.exists(filePath):
		raise ("[ERROR]%s not Exist" % filePath)

	# 读取元数据
	try:
		fileData = open(filePath,'rb').read()
	except:
		raise("[ERROR]Can't open %s" % filePath)
	
	# 解密 RC4 密钥
	EnCryptData = fileData[11:256 + 11]
	rc4key = rsa.decrypt(EnCryptData, rsaKey)

	# 解密文件
	encryptFileData = fileData[278:-9]
	decryptFileData = rc4Decode(encryptFileData, rc4key)[9:-9]

	# 写回
	try:
		open(filePath,"wb").write(decryptFileData)
	except:
		raise("[ERROR]Can't write to %s" % filePath)
	
	# 重命名
	try:
		os.rename(filePath, filePath[:-9])
	except:
		raise("[ERROR]Can't rename %s, pass" % filePath)
	
	progressBarCount += 1

	return 



def DecryptDir(dirPath):
	global progressBarCount

	files = os.listdir(dirPath)

	for File in files:
		fullPath = dirPath + "/" + File

		if os.path.isdir(fullPath):
			DecryptDir(fullPath)
		else:
			if True == isEncrypt(fullPath):
				try:
					DecryptFile(fullPath)
				except Exception as string:
					print("\b", end="")
					print(string)
					pass
			else:
				pass

		print("\b%c" % progressBar[progressBarCount % 4], end="")

	print("\b", end="")
	return 



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print ('Parameter error!')
		print ("User: Decrypter.exe <filePath>")
		print ("User: Decrypter.exe <DirPath>")
		sys.exit()

	path = sys.argv[1] 

	if False == os.path.exists(path):
		print("path not exist!")
		sys.exit()

	print("Start Decrypt!")

	try:
		if os.path.isdir(path):
			DecryptDir(path)
		else:
			DecryptFile(path)
	except Exception as string:
		print(string)

	print("Decrypt Done!")
	
