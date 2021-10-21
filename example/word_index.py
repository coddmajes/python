#coding:utf-8
import sys
import os
import re
import subprocess
import time
import random
import win32com
import win32com.client

from win32com.client import Dispatch, constants


class SortOptions(object):

	def __init__(self):
		self.quest_num = 21#题号
		self.index = 0#题号位置
		self.insert_pos = 0#插入未知
		# self.distinguish = 0#用于区分正常句子0，题号句1，options2
		self.option = ''
	
	def options_sort(self, reading_part, fileinterimAbspath, fileNewAbspath):
		
		reading_list = []
		options = []
		
		try:
			# options_file = open(fileinterimAbspath, 'w')
			for line in reading_part:
				reading_list.append(line)
				#找到21等序号的list 对其进行的操作：
				#1.记录插入位置
				#2.获得随机位置的list
				#3.并设置区别于options的判断操作
				if line.find(str(self.quest_num) + '.')>-1 and self.quest_num <= 40:
					self.index = reading_list.index(line)
					# self.insert_pos = self.index + 1
					#self.distinguish = 1
					#获得随机位置list
					pos = [0,1,2,3]
					random.shuffle(pos)
					# print(self.index)
					continue
				#if self.distinguish == 1:
				if line.find('[A]')>-1 and not line.find('[B]')>-1:
					self.option = '['+str(pos[0])+']'
					options.insert(pos[0],line.replace('[A]', self.option))
					self.index = reading_list.index(line)
					self.insert_pos = self.index
					reading_list.pop(self.index)
					continue
				elif line.find('[B]')>-1 and not line.find('[C]')>-1:
					self.option = '['+str(pos[1])+']'
					options.insert(pos[1],line.replace('[B]', self.option))
					self.index = reading_list.index(line)
					reading_list.pop(self.index)
					continue
				elif line.find('[C]')>-1 and not line.find('[D]')>-1:
				#elif line.find('[C]')>-1:
					self.option = '['+str(pos[2])+']'
					options.insert(pos[2],line.replace('[C]', self.option))
					self.index = reading_list.index(line)
					reading_list.pop(self.index)
					continue
				elif line.find('[D]')>-1 and not line.find('[B]')>-1:
					self.option = '['+str(pos[3])+']'
					options.insert(pos[3],line.replace('[D]', self.option))
					# options.append(line.replace('[D]', self.option))
					self.index = reading_list.index(line)
					reading_list.pop(self.index)
					#val=pos[0]%4
					# reading_list.insert(self.index, options[pos[3]])
					# options_file.write(line)
					# options_file.write()
				
					self.quest_num += 1
				
					opts = []
					for opt in options:
						if opt.find('[0]')>-1:
							opts.insert(0, opt)
						elif opt.find('[1]')>-1:
							opts.insert(1, opt)
						elif opt.find('[2]')>-1:
							opts.insert(2, opt)
						elif opt.find('[3]')>-1:
							opts.insert(3, opt)
					options = []
				
					for op in opts:
						reading_list.insert(self.insert_pos, op)
						self.insert_pos +=1	
					opts = []
					continue
		except:pass
		parta = open(fileinterimAbspath, 'w')
		for li in reading_list:
			parta.write(li)
		parta.close()
		# if os.path.exists(fileinterimAbspath):
			# os.remove(fileinterimAbspath)
		
		# word=win32com.client.Dispatch("Word.Application")
		# docx=word.Documents.Add()
		# for list in reading_list:
			# docx.Paragraphs.Last.Range.Text = list
		# docx.SaveAs(fileNewAbspath)
		# word.Documents.Close()  
		# word.Quit()
	
	def cutoff(self, fileinterimAbspath, fileNewAbspath):
		#截取reading comprehension部分,并写入TXT中
		interim_filestr = open(fileinterimAbspath).read()
		if len(interim_filestr)>536870912:
			return False
		print(len(interim_filestr))
		# print(interim_filestr.split('Section')[2].split('Part')[1]) #split返回一个list
		if os.path.exists(fileinterimAbspath):
			os.remove(fileinterimAbspath)
		reading_file = open(fileinterimAbspath, 'w')
		try:
			reading_file.write(interim_filestr.split('Section')[2].split('Part')[1])
		except:
			pass
		reading_file.close()
		
		#将TXT文件读到list 对list进行操作
		reading_file = open(fileinterimAbspath)
		reading_part = []
		for line in reading_file:
			reading_part.append(line)
		reading_file.close()
		# print(reading_part)
		if os.path.exists(fileinterimAbspath):
			os.remove(fileinterimAbspath)
		self.options_sort(reading_part, fileinterimAbspath, fileNewAbspath)
		
		
	def capture(self, fileabspath, fileinterimAbspath, fileNewAbspath):
		#打开文档，并保存临时文档
		wc=win32com.client.constants
		try:
			wordapp = win32com.client.gencache.EnsureDispatch('Word.Application')
		except:  
			wordapp = win32com.client.Dispatch("wps.Application")  
		# else:  
			# wordapp = win32com.client.Dispatch("kwps.application") 
		# except:pass
		wordapp.Visible = 0  #1时 为使文档可见
		wordapp.DisplayAlerts = 0 
		doc = wordapp.Documents.Open(fileabspath)
		doc.SaveAs(FileName=fileinterimAbspath,FileFormat=wc.wdFormatText)
		# try:
			# #doc.SaveAs(fileinterimAbspath,4)
			# doc.SaveAs(FileName=fileinterimAbspath,FileFormat=wc.wdFormatText) #为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4 
		# except:
			# wordapp.Documents.Close() 
			# wordapp.Quit()
		# try:  
			# wordapp=win32com.client.gencache.EnsureDispatch('Word.Application')  
		# except:  
			# pass 
		try:  
			wordapp.Documents.Close()  
			wordapp.Documents.Close(wc.wdDoNotSaveChanges)  
			wordapp.Quit 
			
		except:pass
		# def getChildrenPidsOfPid(): 
		"""Returns the children pids of a pid""" 
		# newpidcnt = 0 
		# pid = 0 
		# wmi = win32com.client.GetObject('winmgmts:') 
		# for win32_process_instance in wmi.InstancesOf('win32_process'): 
			# if win32_process_instance.Name and win32_process_instance.Name.upper() == "HuaYang.exe".upper(): 
				# pTime = win32_process_instance.Properties_('CreationDate').Value 
				# processId = int(win32_process_instance.Properties_('ProcessId')) 
				# if pTime > 5: 
					# newpidcnt = newpidcnt + 1 
					# pid = processId 
		# if newpidcnt > 2: 
			# raise RuntimeError("error") 
		# print pid 
		# return pid 
		# # def kill(pid): 
		# try: 
			# # command = 'taskkill /F /IM %d' %pid 
			# # print type(command) 
			# # os.system(command) 
			# #1111 
			 
			# subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i"%pid , shell=True) 
		# except OSError, e: 
			# print 'no process'

		time.sleep(2)
		self.cutoff(fileinterimAbspath, fileNewAbspath)
		
		
		
		
def traverse_dir(root_dir):
	# sortOptions = SortOptions()
	filePath = []#文件绝对路径
	
	fileNames = []#文件本来的名字doc
	fileNames_new = []#文件新的名字doc （1）
	filePath_new = []#文件新的绝对地址 doc （1）
	# fileNames_interim = []#文件临时名字 TXT
	filePath_interim = []#文件临时绝对路径 TXT
	# fileNames_reading = []#文件reading部分的名字 （1）TXT
	# filePath_reading = []#文件reading部分的绝对路径 （1）TXT
	for dirpath,dirnames,files in os.walk(root_dir):
		for file in files:
			# fileNames.append(file)
			#获得文件最终的绝对路径，并将其放入list中 (1).docx
			# fileNames_new.append(file.split('.')[0] + '(1)'+('.doc'))#新的文件名全部在后面加上（1）
			if file.split('.')[-1] == 'docx':
				fileNew_abspath = os.path.abspath(os.path.join(dirpath, file.split('.')[0] + '(1)'+('.docx')))
			elif file.split('.')[-1] == 'doc':
				fileNew_abspath = os.path.abspath(os.path.join(dirpath, file.split('.')[0] + '(1)'+('.doc')))
			filePath_new.append(fileNew_abspath)
			
			# fileNames_interim.append(file.split('.')[0]+('.txt'))#临时文件后面全都加上.txt
			#获得文件暂存的绝对路径，并将其放入list中 TXT
			fileinterim_abspath = os.path.abspath(os.path.join(dirpath, file.split('.')[0]+('.txt')))
			filePath_interim.append(fileinterim_abspath)
			
			#获得文件的绝对路径，并将其放进list中 docx
			file_abspath = os.path.abspath(os.path.join(dirpath, file))
			filePath.append(file_abspath)
			sortOptions = SortOptions()
			sortOptions.capture(file_abspath, fileinterim_abspath, fileNew_abspath)#将文件的绝对路径，文件临时绝对路径, 文件reading部分新的doc的绝对路径作为参数
	print(filePath)
	print(filePath_interim)
	print(filePath_new)
	# print(filePath_interim)
	
if '__main__' == __name__:
	if len(sys.argv) == 2:
		traverse_dir(sys.argv[1])
	else:
		print('Usage:\n%s word_path' % (sys.argv[0],))