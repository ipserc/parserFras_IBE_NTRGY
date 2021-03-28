#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    
    xpdf-tools-linux-4.02/bin64/pdftotext Is required to run properly this script
    
    Equivalent in bash code: for f in *.pdf; do pdftotext -table $f $f.txt; done
	pdftotext Path: os.system("/path_to_script/parserFrasIberdrola/xpdf-tools-linux-4.02/bin64/pdftotext -table '%s' '%s'" % (pdfFP, txtFP))
	ipserc@galileo ~ $pdftotext -h
		pdftotext version 4.02
		Copyright 1996-2019 Glyph & Cog, LLC
		Usage: pdftotext [options] <PDF-file> [<text-file>]
		  -f <int>             : first page to convert
		  -l <int>             : last page to convert
		  -layout              : maintain original physical layout
		  -simple              : simple one-column page layout
		  -table               : similar to -layout, but optimized for tables
		  -lineprinter         : use strict fixed-pitch/height layout
		  -raw                 : keep strings in content stream order
		  -fixed <number>      : assume fixed-pitch (or tabular) text
		  -linespacing <number>: fixed line spacing for LinePrinter mode
		  -clip                : separate clipped text
		  -nodiag              : discard diagonal text
		  -enc <string>        : output text encoding name
		  -eol <string>        : output end-of-line convention (unix, dos, or mac)
		  -nopgbrk             : don't insert page breaks between pages
		  -bom                 : insert a Unicode BOM at the start of the text file
		  -marginl <number>    : left page margin
		  -marginr <number>    : right page margin
		  -margint <number>    : top page margin
		  -marginb <number>    : bottom page margin
		  -opw <string>        : owner password (for encrypted files)
		  -upw <string>        : user password (for encrypted files)
		  -q                   : don't print any messages or errors
		  -cfg <string>        : configuration file to use in place of .xpdfrc
		  -v                   : print copyright and version __INFO__
		  -h                   : print usage information
		  -help                : print usage information
		  --help               : print usage information
		  -?                   : print usage information


    
    @author:     Jose Luis Núñez
    
    @copyright:  2020 organization_name. All rights reserved.
    
    @license:    license
    
    @contact:    joseluis.nunez@selenitas.es
    @deffield    updated: 
"""

__all__ = []
__version__ = 2.4
__date__ = '2021-03-22'
__updated__ = '2021-03-28'

import os
import io
import re
import codecs
import datetime
import locale
from pathlib import Path
#import pdftotext
import random

##################################
# PSEUDO-CONSTANTS
##################################
__DEBUG_ON__ = False
__INFO__ = "INFO"
__WARN__ = "WARN"
__ERROR__ = "ERROR"
__USER_HOME__ = os.path.expanduser('~')
__PDFTOTEXT_PATH__ = "xpdf-tools-linux-4.02/bin64/pdftotext"
__CMD_PDFTOTEXT__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), __PDFTOTEXT_PATH__)
__IBRDL__ = "IBRDL"
__NTRGY__ = "NTRGY"
__BOX_SIZE__ = 65

##################################
# BASE FUNCTIONS
##################################
def sprintf(*args, **kwargs):
    sio = io.StringIO()
    print(*args, **kwargs, end="", file=sio)
    return sio.getvalue()
    
def printDebug(*args, **kwargs):
	if __DEBUG_ON__:
		print("["+str(datetime.datetime.now())+"] - DEBUG :" + sprintf(*args, **kwargs))

def printTraza(strTipoTRAZA, *args, **kwargs):
	print("["+str(datetime.datetime.now())+"] - "+strTipoTRAZA+" :" + sprintf(*args, **kwargs))
	
def toNum(excelNum):
	outNum = str(excelNum)
	outNum = outNum.replace(".", ":")
	outNum = outNum.replace(",", ".")
	outNum = outNum.replace(":", "")
	return float(outNum)

def toExcelNum(realNum):
	outNum = str(realNum)
	return outNum.replace(".", ",")

def numDiasAnho(anho):
	if str(anho) == "" or int(anho) == 0:
		return 365
	if  int(anho) % 4 != 0 or int(anho) % 400 == 0:
		return 365
	else:
		return 366

def strDiasAnho(anho):
	return str(numDiasAnho(anho))

##################################
# DECORATIONS
##################################
def repeat(cadena, veces):
	textorep = ""
	for i in range(0, veces):
		textorep += cadena
	return textorep

def boxTitleRandom(size, title):
	boxNbr = random.randint(1, 6)
	if boxNbr == 1:
		return boxTitle1(size, title)
	elif boxNbr == 2:
		return boxTitle2(size, title)
	elif boxNbr == 3:
		return boxTitle3(size, title)
	elif boxNbr == 4:
		return boxTitle4(size, title)
	elif boxNbr == 5:
		return boxTitle5(size, title)
	elif boxNbr == 6:
		return boxTitle6(size, title)

def makeBoxTitle(size, title, csi, top, csd, msi, msd, mdi, mdd, cii, bot, cid, nmid = False ):
	boxTitle = ""
	if len(title) < size:
		titleSize = size 
	else: 
		titleSize = len(title)+4
	theTitleTop = csi+repeat(top, titleSize-2)+csd
	theTitleMid = msi+repeat(" ", titleSize-2)+msd
	theTitleText = mdi+repeat(" ", int((titleSize-len(title))/2)-2)+" "+title
	theTitleText += " "+repeat(" ", titleSize-len(theTitleText)-2)+mdd
	theTitleBot = cii+repeat(bot, titleSize-2)+cid
	
	boxTitle = theTitleTop+os.linesep\
		+theTitleMid+os.linesep\
		+theTitleText+os.linesep
	if nmid:
		boxTitle += theTitleMid+os.linesep
	boxTitle += theTitleBot;
	return boxTitle

def boxTitle1(size, title):
	return makeBoxTitle(size, title, \
	"_", "_", "_", \
	"|",      "|", \
	"|",      "|", \
	"|", "_", "|" )

def boxTitle2(size, title):
	return makeBoxTitle(size, title, \
	" ", "_", " ", \
	"/",      "\\", \
	"|",      "|", \
	"\\", "_", "/" )

def boxTitle3(size, title):
	return makeBoxTitle(size, title, \
	"_", "_", "_", \
	"\\",     "/", \
	"<",      ">", \
	"/", "_", "\\" )
	
def boxTitle4(size, title):
	return makeBoxTitle(size, title, \
	"+", "-", "+", \
	"|",      "|", \
	"|",      "|", \
	"+", "-", "+", True )

def boxTitle5(size, title):
	return makeBoxTitle(size, title, \
	"#", "=", "#", \
	"I",      "I", \
	"I",      "I", \
	"#", "=", "#", True )
	
def boxTitle6(size, title):
	return makeBoxTitle(size, title, \
	"_", "_", "_", \
	"\\",     "/", \
	"[",      "]", \
	"/", "_", "\\" )
	
def printProgFacts(size):
	print(boxTitleRandom(size, "DATOS DEL PROGRAMA"))
	print("Script name  :", os.path.basename(__file__))
	print("Version      :", __version__)
	print("Creation date:", __date__)
	print("Update date  :", __updated__)
	print(repeat("-", size))


#################################
# USELESS FUNCTIONS JUTS FOR TEST
#################################
def readAfile():
	path = "/home/ipserc/Documentos/Facturas/Iberdrola.Electricidad Galileo 108/2021"
	file = "2021-03-04-21.54.25.530080.pdf.txt"
	pathFile = os.path.join(path, file)
	f = codecs.open(pathFile, "r", "ISO-8859-1")
	return f.readlines()

def playWithDirs():
	filePath = __file__
	print("This script file path is ", filePath)
	absFilePath = os.path.abspath(__file__)
	print("This script absolute path is ", absFilePath)
	absDirName = os.path.dirname(os.path.abspath(__file__))
	print("This script absolute dir name is ", absDirName)


##################################
# ELECTRICIDAD
##################################
def getMatchData_ELEC(matchStrToken, matchStrData, lineNbr, theText):
	data = []
	factMatch = re.match(matchStrToken, theText[lineNbr])
	if factMatch:
		#------ printDebug("lineNbr     : ",lineNbr)
		lineNbr += 2
		#------ printDebug("Next lineNbr: ", lineNbr)
		#------ printDebug("Next line   : ", theText[lineNbr])
		factMatch = re.match(matchStrData, theText[lineNbr])
		if factMatch:
			matchGroups = factMatch.groups()
			for item in matchGroups:
				#------ printDebug("item:" + item)
				data.append(item)
	return data

def extractInfo_ELEC_IBRDL(theText):
	sectFecha = ".*Fecha emisión factura: +(.*de +\d{4})"
	sectPoten = "Peaje +acceso +potencia"
	sectComer = "Comercialización"
	dataLine1 = "(\d,\d+) +kW +x +(\d+) +días +x +(\d,\d+) +\/kW +día"
	sectEner = "Peaje +acceso +energía"
	sectCost = "Coste +energía"
	dataLine2 = "(\d+\.\d+|\d+) +kWh +x +(\d,\d+) +\/kWh"
	dataRow = {"fechaFactura":"","mesAnho":"","potenciaContratada":"","diasFacturacion":"", "diasAnho":"","terminoPotenciaDiario":"","terminoPotenciaAnual":"",\
	"terminoCosteDiario":"","terminoCosteAnual":"","energiaConsumida":"", "precioTermEnerPeajAcc":"","precioTermCostHorEner":""}

	for lineNbr in range(0, len(theText)):
		# Fecha emisión factura
		fechaFactura = re.match(sectFecha, theText[lineNbr])
		if fechaFactura:
			printTraza(__INFO__, "Extrayendo Fecha emisión factura", "")	
			fechaFactura = fechaFactura.group(1)
			# mesAnio =  re.match("\d+ de (\w+) de (\d+)", fechaFactura)
			# mes = mesAnio[1] 
			# anio = mesAnio[2]
			locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
			dtObj = datetime.datetime.strptime(fechaFactura, '%d de %B de %Y')
			printDebug("Fecha emisión factura:",fechaFactura)
			printDebug("Mes emisión factura  :",dtObj.month)
			printDebug("Año emisión factura  :",dtObj.year)
			#dataRow.update({"fechaFactura":fechaFactura, "mesAnho":sprintf("1/",dtObj.month,"/",dtObj.year).replace(" ","")})
			dataRow.update({"fechaFactura":fechaFactura, "mesAnho":("1/"+str(dtObj.month)+"/"+str(dtObj.year))})
			continue

		# Peaje acceso potencia
		data = getMatchData_ELEC(sectPoten, dataLine1, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Peaje acceso potencia", "")	
			potenciaContratada = data[0]
			diasFacturacion = data[1]
			diasAnho = strDiasAnho(dtObj.year)
			terminoPotenciaDiario = data[2]
			if diasAnho != "" or diasAnho != 0:
				printDebug("toNum(terminoPotenciaDiario):", toNum(terminoPotenciaDiario))
				terminoPotenciaAnual = toExcelNum(toNum(terminoPotenciaDiario)*int(diasAnho))
			else:
				terminoPotenciaAnual = ""
			printDebug("potenciaContratada   :", potenciaContratada)
			printDebug("diasFacturacion      :", diasFacturacion)
			printDebug("diasAnho             :", diasAnho)
			printDebug("terminoPotenciaAnual :", terminoPotenciaAnual)
			printDebug("terminoPotenciaDiario:", terminoPotenciaDiario)
			dataRow.update({"potenciaContratada":potenciaContratada, "diasFacturacion":diasFacturacion, "diasAnho":diasAnho, "terminoPotenciaDiario":terminoPotenciaDiario, "terminoPotenciaAnual":terminoPotenciaAnual})
			continue

		# Comercialización
		data = getMatchData_ELEC(sectComer, dataLine1, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Comercialización", "")	
			potenciaContratada = data[0]
			diasFacturacion = data[1]
			terminoCosteDiario = data[2]
			diasAnho = strDiasAnho(dtObj.year)
			if terminoCosteDiario != "":
				printDebug("toNum(terminoCosteDiario):", toNum(terminoCosteDiario))
				terminoCosteAnual = toExcelNum(toNum(terminoCosteDiario)*int(diasAnho))
			else:
				terminoCosteAnual = ""
			printDebug("potenciaContratada   :", potenciaContratada)
			printDebug("diasFacturacion      :", diasFacturacion)
			printDebug("terminoCosteAnual    :", terminoCosteAnual)
			printDebug("terminoCosteDiario   :", terminoCosteDiario)
			dataRow.update({"terminoCosteDiario":terminoCosteDiario, "terminoCosteAnual":terminoCosteAnual})
			continue

		# Peaje acceso energía
		data = getMatchData_ELEC(sectEner, dataLine2, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Peaje acceso energía", "")	
			energiaConsumida = data[0]
			precioTermEnerPeajAcc = data[1]
			printDebug("energiaConsumida     :",energiaConsumida)
			printDebug("precioTermEnerPeajAcc:", precioTermEnerPeajAcc)
			dataRow.update({"energiaConsumida":energiaConsumida, "precioTermEnerPeajAcc":precioTermEnerPeajAcc})
			continue

		# Coste energía
		data = getMatchData_ELEC(sectCost, dataLine2, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Coste energía", "")	
			#energiaConsumida = data[0]
			precioTermCostHorEner = data[1]
			printDebug("energiaConsumida     :",energiaConsumida)
			printDebug("precioTermCostHorEner:", precioTermCostHorEner)
			dataRow.update({"precioTermCostHorEner":precioTermCostHorEner})
			
	return dataRow

def extractInfo_ELEC_NTRGY(theText):
	sectFecha = ".*Fecha emisión factura: +(.*de +\d{4})"
	sectPeaje = " +Importe +por +peaje +de +acceso"
	sectComer = " +Importe +por +margen +de +comercialización +fijo"
	dataLine1 = " +(\d+,\d+).* (\d+,\d+).*\((\d+)\/(\d{3})"
	sectCost = " +Importe +por +coste +de +la +energía"
	dataLine2 = " +(\d+) +kWh .* (\d+,\d+) \/kWh"
	dataRow = {"fechaFactura":"","mesAnho":"","potenciaContratada":"","diasFacturacion":"", "diasAnho":"","terminoPotenciaDiario":"","terminoPotenciaAnual":"",\
	"terminoCosteDiario":"","terminoCosteAnual":"","energiaConsumida":"", "precioTermEnerPeajAcc":"","precioTermCostHorEner":""}

	for lineNbr in range(0, len(theText)):
		# Fecha emisión factura
		fechaFactura = re.match(sectFecha, theText[lineNbr])
		if fechaFactura:
			printTraza(__INFO__, "Extrayendo Fecha emisión factura", "")	
			fechaFactura = fechaFactura.group(1)
			# mesAnio =  re.match("\d+ de (\w+) de (\d+)", fechaFactura)
			# mes = mesAnio[1] 
			# anio = mesAnio[2]
			locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
			dtObj = datetime.datetime.strptime(fechaFactura, '%d de %B de %Y')
			printDebug("Fecha emisión factura:",fechaFactura)
			printDebug("Mes emisión factura  :",dtObj.month)
			printDebug("Año emisión factura  :",dtObj.year)
			dataRow.update({"fechaFactura":fechaFactura, "mesAnho":("1/"+str(dtObj.month)+"/"+str(dtObj.year))})
			continue

		# Peaje acceso potencia
		data = getMatchData_ELEC(sectPeaje, dataLine1, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Importe por peaje de acceso:", "POTENCIA")	
			potenciaContratada = data[0]
			terminoPotenciaAnual = data[1]
			diasFacturacion = data[2]
			diasAnho = data[3]
			if diasAnho != 0:
				printDebug("toNum(terminoPotenciaAnual):", toNum(terminoPotenciaAnual))
				terminoPotenciaDiario = toExcelNum(toNum(terminoPotenciaAnual)/int(diasAnho))
			else:
				terminoPotenciaDiario = ""
			printDebug("potenciaContratada   :", potenciaContratada)
			printDebug("diasFacturacion      :", diasFacturacion)
			printDebug("diasAnho             :", diasAnho)
			printDebug("terminoPotenciaAnual :", terminoPotenciaAnual)
			printDebug("terminoPotenciaDiario:", terminoPotenciaDiario)
			dataRow.update({"potenciaContratada":potenciaContratada, "diasFacturacion":diasFacturacion, "diasAnho":diasAnho, "terminoPotenciaDiario":terminoPotenciaDiario, "terminoPotenciaAnual":terminoPotenciaAnual})
			continue

		# Comercialización
		data = getMatchData_ELEC(sectComer, dataLine1, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Importe por margen de comercialización fijo:", "POTENCIA")	
			potenciaContratada = data[0]
			terminoCosteAnual = data[1]
			diasFacturacion = data[2]
			diasAnho = data[3]
			if diasAnho != "" or diasAnho != 0:
				printDebug("toNum(terminoCosteAnual):", toNum(terminoCosteAnual))
				terminoCosteDiario = toExcelNum(toNum(terminoCosteAnual)/int(diasAnho))
			else:
				terminoPotenciaDiario = ""
			printDebug("potenciaContratada   :", potenciaContratada)
			printDebug("diasFacturacion      :", diasFacturacion)
			printDebug("terminoCosteAnual    :", terminoCosteAnual)
			printDebug("terminoCosteDiario   :", terminoCosteDiario)
			dataRow.update({"terminoCosteDiario":terminoCosteDiario, "terminoCosteAnual":terminoCosteAnual})
			continue
			
		# Peaje acceso energía
		data = getMatchData_ELEC(sectPeaje, dataLine2, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Importe por peaje de acceso:", "ENERGIA")	
			energiaConsumida = data[0]
			precioTermEnerPeajAcc = data[1]
			printDebug("energiaConsumida     :", energiaConsumida)
			printDebug("precioTermEnerPeajAcc:", precioTermEnerPeajAcc)
			dataRow.update({"energiaConsumida":energiaConsumida, "precioTermEnerPeajAcc":precioTermEnerPeajAcc})
			continue

		# Coste energía
		data = getMatchData_ELEC(sectCost, dataLine2, lineNbr, theText)
		if data:
			printTraza(__INFO__, "Extrayendo Coste:", "ENERGIA")	
			#energiaConsumida = data[0]
			precioTermCostHorEner = data[1]
			printDebug("energiaConsumida     :", energiaConsumida)
			printDebug("precioTermCostHorEner:", precioTermCostHorEner)
			dataRow.update({"precioTermCostHorEner":precioTermCostHorEner})

	return dataRow

def getDataFromPdf_ELEC(comp, iniPath):
	excelDataTable = []
	printDebug("iniPath:", iniPath)
	for root, dirs, files in os.walk(iniPath):
		for fileName in files:
			if re.match(".*Saltar", root):
				continue
			if re.match(".*\d{4}", root):
				filepath = os.path.join(root, fileName)
				if filepath.endswith(".pdf"):
					printTraza(__INFO__, "Procesando Factura PDF:", filepath)
					pdfToTxt_ELEC(comp, filepath, excelDataTable)
						
	printDebug("excelDataTable:", excelDataTable)
	return excelDataTable

def pdfToTxt_ELEC(comp, filepath, excelDataTable):
	pdfFP = filepath
	txtFP = filepath+".txt"
	os.system(__CMD_PDFTOTEXT__ + " -table '%s' '%s'" % (pdfFP, txtFP))
	fr = codecs.open(txtFP, "r", "ISO-8859-1")
	printTraza(__INFO__, "Factura PDF convertida a txt:", txtFP)	
	if comp == __IBRDL__:
		excelDataTable.append(extractInfo_ELEC_IBRDL(fr.readlines()))
	elif comp == __NTRGY__:
		excelDataTable.append(extractInfo_ELEC_NTRGY(fr.readlines()))

def writeToCSV_ELEC(comp, iniPath, excelDataTable):
	rowStr = "fechaFactura"+";"+\
	"mesAnho"+";"+\
	"potenciaContratada"+";"+\
	"diasFacturacion"+";"+\
	"energiaConsumida"+";"+\
	"terminoPotenciaDiario"+";"+\
	"terminoPotenciaAnual"+";"+\
	"terminoCosteDiario"+";"+\
	"terminoCosteAnual"+";"+\
	"precioTermEnerPeajAcc"+";"+\
	"precioTermCostHorEner"+";"+\
	"diasAnho"+os.linesep
	for rowData in excelDataTable:
		rowStr += str(rowData["fechaFactura"])+";"+\
		str(rowData["mesAnho"])+";"+\
		str(rowData["potenciaContratada"])+";"+\
		str(rowData["diasFacturacion"])+";"+\
		str(rowData["energiaConsumida"])+";"+\
		str(rowData["terminoPotenciaDiario"])+";"+\
		str(rowData["terminoPotenciaAnual"])+";"+\
		str(rowData["terminoCosteDiario"])+";"+\
		str(rowData["terminoCosteAnual"])+";"+\
		str(rowData["precioTermEnerPeajAcc"])+";"+\
		str(rowData["precioTermCostHorEner"])+";"+\
		str(rowData["diasAnho"])+os.linesep
	printDebug("rowStr:", rowStr)
	csvFile = os.path.join(iniPath, "excelDataTable_ELEC_"+comp+".csv")
	printTraza(__INFO__, "Guardando Data Table ELEC_IBE en:", csvFile) 
	with open(csvFile, "wt") as fw:
		fw.write(rowStr)

def printELECstats(comp, excelDataTable):
	numItem = -1
	totalDiasFacturacion = 0
	totalenergiaConsumida = 0
	totalTerminoPotenciaDiario = 0 
	totalTerminoCosteDiario = 0
	totalPrecioTermEnerPeajAcc = 0
	totalPrecioTermCostHorEner = 0
	CosteEnergiaConsumida = 0
	for rowData in excelDataTable:
		if rowData["energiaConsumida"] == "":
			continue
		numItem += 1
		if numItem == 0:
			continue
		totalDiasFacturacion += toNum(rowData["diasFacturacion"])
		totalenergiaConsumida += toNum(rowData["energiaConsumida"])
		totalTerminoPotenciaDiario += toNum(rowData["terminoPotenciaDiario"])
		totalTerminoCosteDiario += toNum(rowData["terminoCosteDiario"])
		totalPrecioTermEnerPeajAcc += toNum(rowData["precioTermEnerPeajAcc"])
		totalPrecioTermCostHorEner += toNum(rowData["precioTermCostHorEner"])
		CosteEnergiaConsumida += toNum(rowData["energiaConsumida"]) * toNum(rowData["precioTermCostHorEner"])
	if numItem > 0:
		print(boxTitleRandom(__BOX_SIZE__, "RESUMEN DATOS ELECT " + comp))
		print("Num. Total Facturas......................:", len(excelDataTable)-1)
		print("Num. Total Facturas Válidas..............:", numItem)
		print("Num. Total Días Facturación..............:", int(totalDiasFacturacion))
		print("Total Energía Consumida (kWh)............:", totalenergiaConsumida)
		print("V.M. Energía Consumida Diaria (kWh dia)..:", totalenergiaConsumida / totalDiasFacturacion)
		print("V.M. Término Potencia Diario (€ kW día)..:", totalTerminoPotenciaDiario / numItem)
		print("V.M. Term. Coste Diario (€ kW día).......:", totalTerminoCosteDiario / numItem)
		print("V.M. Precio Term. Energía Acc. (€ kWh)...:", totalPrecioTermEnerPeajAcc /  numItem)
		print("V.M. Precio Term. Coste Hor. Ene. (€ kWh):", totalPrecioTermCostHorEner /  numItem)
		print("Total Coste Energia Consumida (€)........:", CosteEnergiaConsumida)
		print(repeat("-", __BOX_SIZE__))

		
##################################
# GAS
##################################
def getDataFromPdf_GAS_NTRGY(iniPath):
	excelDataTable = []
	'''
	fileName = "2019/2019_11_01_Factura_FE20321319068135.pdf"
	filepath = os.path.join(iniPath, fileName)
	printDebug("filepath:", filepath)
	pdfToTxt_GAS_NTRGY(filepath, excelDataTable)
	'''
	#'''
	printDebug("iniPath:", iniPath)		
	for root, dirs, files in os.walk(iniPath):
		for fileName in files:
			if re.match(".*Saltar", root):
				continue
			if re.match(".*\d{4}", root):
				filepath = os.path.join(root, fileName)
				if filepath.endswith(".pdf"):
					printTraza(__INFO__, "Procesando Factura PDF:", filepath)
					subExcelDT = pdfToTxt_GAS_NTRGY(filepath)
					printDebug("+ + + + + + subExcelDT:", subExcelDT)
					for dtRow in subExcelDT:
						excelDataTable.append(dtRow)	
	printDebug("excelDataTable:", excelDataTable)
	#'''
	return excelDataTable

def pdfToTxt_GAS_NTRGY(filepath):
	pdfFP = filepath
	txtFP = filepath+".txt"
	os.system(__CMD_PDFTOTEXT__ + " -table '%s' '%s'" % (pdfFP, txtFP))
	printDebug("Parsing ", txtFP,". . .")
	fr = codecs.open(txtFP, "r", "ISO-8859-1")
	printTraza(__INFO__, "Factura PDF convertida a txt:", txtFP)	
	subExcelDT = extractInfo_GAS_NTRGY(fr.readlines())
	printDebug("* * * * * * subExcelDT:", subExcelDT)
	return (subExcelDT)
		
def extractInfo_GAS_NTRGY(theText):
	sectFecha = " +Del +(\d{2}.\d{2}.\d{4}) +al +(\d{2}.\d{2}.\d{4}).+\((\d+) +días"
	sectConsu1 = " +Consumo +gas +(\d+) +kWh +(\d+,\d+) +\/kWh"
	sectConsu2 = " +Período +de +(\d{2}.\d{2}.\d{4}) +a +(\d{2}.\d{2}.\d{4}) +(\d+) +kWh +(\d+,\d+) +\/kWh"
	sectTermi1 = " +Término +fijo +(\d+) +días +(\d+,\d+) +\/día"
	sectTermi2 = " +Período +de +\d{2}.\d{2}.\d{4} +a +\d{2}.\d{2}.\d{4} +(\d+) +días +(\d+,\d+) +\/día"
	fixTermDataTable = []
	periodoDataTable = []
	dataTable = []

	for lineNbr in range(0, len(theText)):
		# Fecha periodo factura
		setcFechaFactura = re.match(sectFecha, theText[lineNbr])
		if setcFechaFactura:
			printTraza(__INFO__, "Extrayendo Fecha periodo factura", "")	
			fixPartDataRow = {}
			fechaFacturaIni = setcFechaFactura.group(1).replace(".", "/")
			fechaFacturaFin = setcFechaFactura.group(2).replace(".", "/")
			diasFacturacion = setcFechaFactura.group(3)
			printDebug("Fecha factura Ini:", fechaFacturaIni)
			printDebug("Fecha factura Fin:", fechaFacturaFin)
			printDebug("Días Facturacion :", diasFacturacion)
			fixPartDataRow.update({"fechaFacturaIni":fechaFacturaIni, "fechaFacturaFin":fechaFacturaFin})
			break

	for lineNbr in range(0, len(theText)):
		# Término fijo
		sectTermFijo = re.match(sectTermi1, theText[lineNbr])
		if sectTermFijo is None:
			# Término fijo: Periodo
			sectTermFijo = re.match(sectTermi2, theText[lineNbr])
			sectTermi = 2
			if not (sectTermFijo is None):
				printDebug("Término fijo: Periodo:", sectTermFijo)
		else:
			sectTermi = 1			
			printDebug("Término fijo:", sectTermFijo)
		if sectTermFijo:
			printTraza(__INFO__, "Extrayendo Término Fijo(", sectTermi, ")")	
			fixTermDataRow = {}
			diasFacturacion = sectTermFijo.group(1)
			terminoFijo = sectTermFijo.group(2)
			printDebug("Días Facturacion :", diasFacturacion)
			printDebug("Término fijo     :", terminoFijo)
			fixTermDataRow.update({"diasFacturacion":diasFacturacion, "terminoFijo":terminoFijo})
			fixTermDataTable.append(fixTermDataRow)

	for lineNbr in range(0, len(theText)):
		# Consumo gas
		matchConsumoGas = re.match(sectConsu1, theText[lineNbr])
		if matchConsumoGas is None:
			# Consumo gas: Periodo
			matchConsumoGas = re.match(sectConsu2, theText[lineNbr])
			consuGas = 2
			if not (matchConsumoGas is None):
				printDebug("Consumo gas: Periodo:", matchConsumoGas)
		else:
			printDebug("Consumo gas:", matchConsumoGas)
			consuGas = 1
		if matchConsumoGas:
			printTraza(__INFO__, "Extrayendo Consumo gas(", consuGas, ")")	
			periodoDataRow = {}
			if consuGas == 2:
				periodoIni = matchConsumoGas.group(1).replace(".", "/")
				periodoFin = matchConsumoGas.group(2).replace(".", "/")
				energiaConsumida = matchConsumoGas.group(3)
				precioEnergia = matchConsumoGas.group(4)
			else:
				periodoIni = fechaFacturaIni
				periodoFin = fechaFacturaFin
				energiaConsumida = matchConsumoGas.group(1)
				precioEnergia = matchConsumoGas.group(2)
			printDebug("Periodo Inicial  :", periodoIni)
			printDebug("Periodo Final    :", periodoFin)
			printDebug("Energía Consumida:", energiaConsumida)
			printDebug("Precio Energía   :", precioEnergia)
			periodoDataRow.update({"periodoIni":periodoIni, "periodoFin":periodoFin, "energiaConsumida":energiaConsumida, "precioEnergia":precioEnergia})
			periodoDataTable.append(periodoDataRow)

	for periodoDataRow in periodoDataTable:
		printDebug("periodoDataRow:",periodoDataRow)
		for fixTermDataRow in fixTermDataTable:
			printDebug("fixTermDataRow:",fixTermDataRow)
			dataTable.append({"fechaFacturaIni":fixPartDataRow["fechaFacturaIni"], \
			"fechaFacturaFin":fixPartDataRow["fechaFacturaFin"], \
			"diasFacturacion":fixTermDataRow["diasFacturacion"], \
			"terminoFijo":fixTermDataRow["terminoFijo"], \
			"periodoIni":periodoDataRow["periodoIni"], \
			"periodoFin":periodoDataRow["periodoFin"], \
			"energiaConsumida":periodoDataRow["energiaConsumida"], \
			"precioEnergia":periodoDataRow["precioEnergia"]})
			printDebug("dataTable:", dataTable)

	return dataTable

def writeToCSV_GAS_NTRGY(iniPath, excelDataTable):
	rowStr = "fechaFacturaIni"+";"+\
	"fechaFacturaFin"+";"+ \
	"periodoIni"+";"+ \
	"periodoFin"+";"+ \
	"diasFacturacion"+";"+ \
	"energiaConsumida"+";"+ \
	"terminoFijo"+";"+ \
	"precioEnergia"+os.linesep
	for rowData in excelDataTable:
		rowStr += rowData["fechaFacturaIni"]+";"+\
		rowData["fechaFacturaFin"]+";"+\
		rowData["periodoIni"]+";"+\
		rowData["periodoFin"]+";"+\
		rowData["diasFacturacion"]+";"+\
		rowData["energiaConsumida"]+";"+\
		rowData["terminoFijo"]+";"+\
		rowData["precioEnergia"]+os.linesep
	printDebug("rowStr:", rowStr)
	csvFile = os.path.join(iniPath, "excelDataTable_GAS_NTRGY.csv")
	printTraza(__INFO__, "Guardando Data Table GAS_NTRGY en:", csvFile) 
	with open(csvFile, "wt") as fw:
		fw.write(rowStr)

def printGASstats(comp, excelDataTable):
	numItem = -1
	totalDiasFacturacion = 0
	totalenergiaConsumida = 0
	
	CosteEnergiaConsumida = 0
	for rowData in excelDataTable:
		if rowData["energiaConsumida"] == "":
			continue
		numItem += 1
		if numItem == 0:
			continue
		totalDiasFacturacion += toNum(rowData["diasFacturacion"])
		totalenergiaConsumida += toNum(rowData["energiaConsumida"])
		CosteEnergiaConsumida += toNum(rowData["energiaConsumida"]) * toNum(rowData["precioEnergia"])
	if numItem > 0:
		print(boxTitleRandom(__BOX_SIZE__, "RESUMEN DATOS GAS " + comp))
		print("Num. Total Facturas......................:", len(excelDataTable)-1)
		print("Num. Total Facturas Válidas..............:", numItem)
		print("Num. Total Días Facturación..............:", int(totalDiasFacturacion))
		print("Total Energía Consumida (kWh)............:", totalenergiaConsumida)
		print("V.M. Energía Consumida Diaria (kWh dia)..:", totalenergiaConsumida / totalDiasFacturacion)
		print("V.M. Precio Energía (€ kWh)..............:", CosteEnergiaConsumida / totalDiasFacturacion)
		print("Total Coste Energia Consumida (€)........:", CosteEnergiaConsumida)
		print(repeat("-", __BOX_SIZE__))

#############################
# Main
#############################

def main():
	
	# Procesar Facturas de ELECTRICIDAD de IBERDROLA
	iniPath = os.path.join(__USER_HOME__, "Documentos/Facturas/Iberdrola Electricidad Madrid")
	printTraza(__INFO__, "Procesando Facturas de ELECTRICIDAD de ", "IBERDROLA")
	excelDataTable_ELEC_IBRDRL = getDataFromPdf_ELEC(__IBRDL__, iniPath)
	writeToCSV_ELEC(__IBRDL__, iniPath, excelDataTable_ELEC_IBRDRL)

	# Procesar Facturas de ELECTRICIDAD de NATURGY
	iniPath = os.path.join(__USER_HOME__, "Documentos/Facturas/Naturgy Electricidad Cangas")
	printTraza(__INFO__, "Procesando Facturas de ELECTRICIDAD de ", "NATURGY")
	excelDataTable_ELEC_NTRGY = getDataFromPdf_ELEC(__NTRGY__, iniPath)
	writeToCSV_ELEC(__NTRGY__, iniPath, excelDataTable_ELEC_NTRGY)

	# Procesar Facturas de GAS de NATURGY	
	iniPath = os.path.join(__USER_HOME__, "Documentos/Facturas/Gas Natural Fenosa")
	printTraza(__INFO__, "Procesando Facturas de GAS de ", "NATURGY")
	excelDataTable_GAS_NTRGY = getDataFromPdf_GAS_NTRGY(iniPath)
	writeToCSV_GAS_NTRGY(iniPath, excelDataTable_GAS_NTRGY)
	
	# Imprimir estadísticas
	printProgFacts(__BOX_SIZE__)
	printELECstats(__IBRDL__, excelDataTable_ELEC_IBRDRL)
	printELECstats(__NTRGY__, excelDataTable_ELEC_NTRGY)
	printGASstats(__NTRGY__, excelDataTable_GAS_NTRGY)

if __name__ == "__main__":
    main()

