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
		  -v                   : print copyright and version info
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
__version__ = 1.1
__date__ = '2021-03-22'
__updated__ = '2021-03-23'

import os
import io
import re
import codecs
import datetime
import locale
from pathlib import Path
import pdftotext

##################################
# CONSTANTES
##################################
DEBUG_ON = True
INFO = "INFO"
WARN = "WARN"
ERROR = "ERROR"
CMD_PDFTOTEXT = os.path.join(os.path.dirname(os.path.abspath(__file__)),"xpdf-tools-linux-4.02/bin64/pdftotext")


def sprintf(*args, **kwargs):
    sio = io.StringIO()
    print(*args, **kwargs, end="", file=sio)
    return sio.getvalue()
    
def printDebug(*args, **kwargs):
	if DEBUG_ON:
		print("["+str(datetime.datetime.now())+"] - DEBUG :" + sprintf(*args, **kwargs))

def printTraza(strTipoTRAZA, *args, **kwargs):
	print("["+str(datetime.datetime.now())+"] - "+strTipoTRAZA+" :" + sprintf(*args, **kwargs))

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
def getMatchData_ELEC_IBE(matchStrToken, matchStrData, lineNbr, theText):
	data = []
	factMatch = re.match(matchStrToken, theText[lineNbr])
	if factMatch:
		# ---printDebug("lineNbr     : ",lineNbr)
		lineNbr += 2
		# ---printDebug("Next lineNbr: ", lineNbr)
		# ---printDebug("Next line   : ", theText[lineNbr])
		factMatch = re.match(matchStrData, theText[lineNbr])
		matchGroups = factMatch.groups()
		for item in matchGroups:
			# ---printDebug("item:" + item)
			data.append(item)
	return data

def extractInfo_ELEC_IBE(theText):
	sectFecha = ".*Fecha emisión factura: +(.*de +\d{4})"
	sectPoten = "Peaje +acceso +potencia"
	sectComer = "Comercialización"
	dataLine1 = "(\d,\d+) +kW +x +(\d+) +días +x +(\d,\d+) +\/kW +día"
	sectEner = "Peaje +acceso +energía"
	sectCost = "Coste +energía"
	dataLine2 = "(\d+\.\d+|\d+) +kWh +x +(\d,\d+) +\/kWh"
	dataRow = {"fechaFactura":"","mesaño":"","potenciaContratada":"","diasFacturacion":"","terminoPotenciaDiario":"",\
	"terminoCosteDiario":"","potenciaConsumida":"", "precioTermEnerPeajAcc":"","precioTermCostHorEner":""}

	# ---printDebug("teText:", theText)
	for lineNbr in range(0, len(theText)):
		# Fecha emisión factura
		fechaFactura = re.match(sectFecha, theText[lineNbr])
		if fechaFactura:
			printTraza(INFO, "Extrayendo Fecha emisión factura", "")	
			fechaFactura = fechaFactura.group(1)
			# mesAnio =  re.match("\d+ de (\w+) de (\d+)", fechaFactura)
			# mes = mesAnio[1] 
			# anio = mesAnio[2]
			locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
			dtObj = datetime.datetime.strptime(fechaFactura, '%d de %B de %Y')
			# ---printDebug("Fecha emisión factura:",fechaFactura)
			# ---printDebug("Mes emisión factura  :",dtObj.month)
			# ---printDebug("Año emisión factura  :",dtObj.year)
			dataRow.update({"fechaFactura":fechaFactura, "mesaño":sprintf(dtObj.month,"/",dtObj.year).replace(" ","")})

		# Peaje acceso potencia
		data = getMatchData_ELEC_IBE(sectPoten, dataLine1, lineNbr, theText)
		if data:
			printTraza(INFO, "Extrayendo Peaje acceso potencia", "")	
			potenciaContratada = data[0]
			diasFacturacion = data[1]
			terminoPotenciaDiario = data[2]
			# ---printDebug("potenciaContratada   :" + potenciaContratada)
			# ---printDebug("diasFacturacion      :" + diasFacturacion)
			# ---printDebug("terminoPotenciaDiario:" + terminoPotenciaDiario)
			#potenciaContratada = potenciaContratada.replace(" kW", "")
			#diasFacturacion = diasFacturacion.replace(" días", "")
			#terminoPotenciaDiario = terminoPotenciaDiario.replace(" /kW día", "")
			dataRow.update({"potenciaContratada":potenciaContratada, "diasFacturacion":diasFacturacion, "terminoPotenciaDiario":terminoPotenciaDiario})

		# Comercialización
		data = getMatchData_ELEC_IBE(sectComer, dataLine1, lineNbr, theText)
		if data:
			printTraza(INFO, "Extrayendo Comercialización", "")	
			potenciaContratada = data[0]
			diasFacturacion = data[1]
			terminoCosteDiario = data[2]
			# ---printDebug("potenciaContratada   :" + potenciaContratada)
			# ---printDebug("diasFacturacion      :" + diasFacturacion)
			# ---printDebug("terminoCosteDiario   :" + terminoCosteDiario)
			#terminoCosteDiario = terminoCosteDiario.replace(" /kW día", "")
			dataRow.update({"terminoCosteDiario":terminoCosteDiario})

		# Peaje acceso energía
		data = getMatchData_ELEC_IBE(sectEner, dataLine2, lineNbr, theText)
		if data:
			printTraza(INFO, "Extrayendo Peaje acceso energía", "")	
			potenciaConsumida = data[0]
			precioTermEnerPeajAcc = data[1]
			# ---printDebug("potenciaConsumida    :" + potenciaConsumida)
			# ---printDebug("precioTermEnerPeajAcc:" + precioTermEnerPeajAcc)
			#potenciaConsumida = potenciaConsumida.replace("kWh", "")
			#precioTermEnerPeajAcc = precioTermEnerPeajAcc.replace(" /kWh", "")
			dataRow.update({"potenciaConsumida":potenciaConsumida, "precioTermEnerPeajAcc":precioTermEnerPeajAcc})

		# Coste energía
		data = getMatchData_ELEC_IBE(sectCost, dataLine2, lineNbr, theText)
		if data:
			printTraza(INFO, "Extrayendo Coste energía", "")	
			#potenciaConsumida = data[0]
			precioTermCostHorEner = data[1]
			# ---printDebug("potenciaConsumida    :" + potenciaConsumida)
			# ---printDebug("precioTermCostHorEner:" + precioTermCostHorEner)
			#precioTermCostHorEner = precioTermCostHorEner.replace(" /kWh", "")
			dataRow.update({"precioTermCostHorEner":precioTermCostHorEner})
			
	return dataRow

def pdfToTxt_ELEC_IBE(filepath, excelDataTable):
	pdfFP = filepath
	txtFP = filepath+".txt"
	os.system(CMD_PDFTOTEXT + " -table '%s' '%s'" % (pdfFP, txtFP))
	fr = codecs.open(txtFP, "r", "ISO-8859-1")
	printTraza(INFO, "Factura PDF convertida a txt:", txtFP)	
	excelDataTable.append(extractInfo_ELEC_IBE(fr.readlines()))
	# ---printDebug("excelDataTable:", excelDataTable)
	
def getDataFromPdf_ELEC_IBE(iniPath):
	excelDataTable = []
	# ---printDebug("iniPath:", iniPath)
	for root, dirs, files in os.walk(iniPath):
		for fileName in files:
			if re.match(".*Saltar", root):
				continue
			if re.match(".*\d{4}", root):
				filepath = os.path.join(root, fileName)
				if filepath.endswith(".pdf"):
					printTraza(INFO, "Procesando Factura PDF:", filepath)
					pdfToTxt_ELEC_IBE(filepath, excelDataTable)
	# ---printDebug("excelDataTable:", excelDataTable)
	return excelDataTable

def writeToCSV_ELEC_IBE(iniPath, excelDataTable):
	rowStr = "fechaFactura"+";"+\
	"mesanno"+";"+\
	"potenciaContratada"+";"+\
	"diasFacturacion"+";"+\
	"potenciaConsumida"+";"+\
	"terminoPotenciaDiario"+";"+\
	"terminoCosteDiario"+";"+\
	"precioTermEnerPeajAcc"+";"+\
	"precioTermCostHorEner"+os.linesep
	for rowData in excelDataTable:
		rowStr += rowData["fechaFactura"]+";"+\
		rowData["mesaño"]+";"+\
		rowData["potenciaContratada"]+";"+\
		rowData["diasFacturacion"]+";"+\
		rowData["potenciaConsumida"]+";"+\
		rowData["terminoPotenciaDiario"]+";"+\
		rowData["terminoCosteDiario"]+";"+\
		rowData["precioTermEnerPeajAcc"]+";"+\
		rowData["precioTermCostHorEner"]+os.linesep
	# ---printDebug("rowStr:", rowStr)
	csvFile = os.path.join(iniPath, "excelDataTable_ELEC_IBE.csv")
	printTraza(INFO, "Guardando Data Table ELEC_IBE en:", csvFile) 
	with open(csvFile, "wt") as fw:
		fw.write(rowStr)

##################################
# GAS
##################################
def getDataFromPdf_GAS_NTRGY(iniPath):
	excelDataTable = []
	'''
	fileName = "2019/2019_11_01_Factura_FE20321319068135.pdf"
	filepath = os.path.join(iniPath, fileName)
	# ---printDebug("filepath:", filepath)
	pdfToTxt_GAS_NTRGY(filepath, excelDataTable)
	'''
	#'''
	# ---printDebug("iniPath:", iniPath)		
	for root, dirs, files in os.walk(iniPath):
		for fileName in files:
			if re.match(".*Saltar", root):
				continue
			if re.match(".*\d{4}", root):
				filepath = os.path.join(root, fileName)
				if filepath.endswith(".pdf"):
					printTraza(INFO, "Procesando Factura PDF:", filepath)
					subExcelDT = pdfToTxt_GAS_NTRGY(filepath)
					# ---printDebug("+ + + + + + subExcelDT:", subExcelDT)
					for dtRow in subExcelDT:
						excelDataTable.append(dtRow)	
	# ---printDebug("excelDataTable:", excelDataTable)
	#'''
	return excelDataTable

def pdfToTxt_GAS_NTRGY(filepath):
	pdfFP = filepath
	txtFP = filepath+".txt"
	os.system(CMD_PDFTOTEXT + " -table '%s' '%s'" % (pdfFP, txtFP))
	# ---printDebug("Parsing ", txtFP,". . .")
	fr = codecs.open(txtFP, "r", "ISO-8859-1")
	printTraza(INFO, "Factura PDF convertida a txt:", txtFP)	
	subExcelDT = extractInfo_GAS_NTRGY(fr.readlines())
	# ---printDebug("* * * * * * subExcelDT:", subExcelDT)
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

	# ---printDebug("teText:", theText)
	for lineNbr in range(0, len(theText)):
		# Fecha periodo factura
		setcFechaFactura = re.match(sectFecha, theText[lineNbr])
		if setcFechaFactura:
			printTraza(INFO, "Extrayendo Fecha periodo factura", "")	
			fixPartDataRow = {}
			fechaFacturaIni = setcFechaFactura.group(1).replace(".", "/")
			fechaFacturaFin = setcFechaFactura.group(2).replace(".", "/")
			numDias = setcFechaFactura.group(3)
			# ---printDebug("Fecha factura Ini:",fechaFacturaIni)
			# ---printDebug("Fecha factura Fin:",fechaFacturaFin)
			# ---printDebug("Número de días   :",numDias)
			fixPartDataRow.update({"fechaFacturaIni":fechaFacturaIni, "fechaFacturaFin":fechaFacturaFin})
			break

	for lineNbr in range(0, len(theText)):
		# Término fijo
		sectTermFijo = re.match(sectTermi1, theText[lineNbr])
		if sectTermFijo is None:
			# Término fijo: Periodo
			sectTermFijo = re.match(sectTermi2, theText[lineNbr])
			sectTermi = 2
			# ---printDebug("Término fijo: Periodo:", sectTermFijo)
		else:
			sectTermi = 1			
			# ---printDebug("Término fijo:", sectTermFijo)
		if sectTermFijo:
			printTraza(INFO, "Extrayendo Término Fijo(", sectTermi, ")")	
			fixTermDataRow = {}
			numDias = sectTermFijo.group(1)
			terminoFijo = sectTermFijo.group(2)
			# ---printDebug("Número de días:",numDias)
			# ---printDebug("Término fijo  :",terminoFijo)
			fixTermDataRow.update({"numeroDias":numDias, "terminoFijo":terminoFijo})
			fixTermDataTable.append(fixTermDataRow)

	for lineNbr in range(0, len(theText)):
		# Consumo gas
		matchConsumoGas = re.match(sectConsu1, theText[lineNbr])
		if matchConsumoGas is None:
			# Consumo gas: Periodo
			matchConsumoGas = re.match(sectConsu2, theText[lineNbr])
			# ---printDebug("Consumo gas: Periodo:", matchConsumoGas)
			consuGas = 2
		else:
			# ---printDebug("Consumo gas:", matchConsumoGas)
			consuGas = 1
		if matchConsumoGas:
			printTraza(INFO, "Extrayendo Consumo gas(", consuGas, ")")	
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
			# ---printDebug("Periodo Inicial  :",periodoIni)
			# ---printDebug("Periodo Final    :",periodoFin)
			# ---printDebug("Energía Consumida:",energiaConsumida)
			# ---printDebug("Precio Energía   :",precioEnergia)
			periodoDataRow.update({"periodoIni":periodoIni, "periodoFin":periodoFin, "energiaConsumida":energiaConsumida, "precioEnergia":precioEnergia})
			periodoDataTable.append(periodoDataRow)

	for periodoDataRow in periodoDataTable:
		# ---printDebug("periodoDataRow:",periodoDataRow)
		for fixTermDataRow in fixTermDataTable:
			# ---printDebug("fixTermDataRow:",fixTermDataRow)
			dataTable.append({"fechaFacturaIni":fixPartDataRow["fechaFacturaIni"], \
			"fechaFacturaFin":fixPartDataRow["fechaFacturaFin"], \
			"numeroDias":fixTermDataRow["numeroDias"], \
			"terminoFijo":fixTermDataRow["terminoFijo"], \
			"periodoIni":periodoDataRow["periodoIni"], \
			"periodoFin":periodoDataRow["periodoFin"], \
			"energiaConsumida":periodoDataRow["energiaConsumida"], \
			"precioEnergia":periodoDataRow["precioEnergia"]})
			# ---printDebug("dataTable:", dataTable)

	return dataTable

def writeToCSV_GAS_NTRGY(iniPath, excelDataTable):
	rowStr = "fechaFacturaIni"+";"+\
	"fechaFacturaFin"+";"+ \
	"periodoIni"+";"+ \
	"periodoFin"+";"+ \
	"numeroDias"+";"+ \
	"energiaConsumida"+";"+ \
	"terminoFijo"+";"+ \
	"precioEnergia"+os.linesep
	for rowData in excelDataTable:
		rowStr += rowData["fechaFacturaIni"]+";"+\
		rowData["fechaFacturaFin"]+";"+\
		rowData["periodoIni"]+";"+\
		rowData["periodoFin"]+";"+\
		rowData["numeroDias"]+";"+\
		rowData["energiaConsumida"]+";"+\
		rowData["terminoFijo"]+";"+\
		rowData["precioEnergia"]+os.linesep
	# ---printDebug("rowStr:", rowStr)
	csvFile = os.path.join(iniPath, "excelDataTable_GAS_NTRGY.csv")
	printTraza(INFO, "Guardando Data Table GAS_NTRGY en:", csvFile) 
	with open(csvFile, "wt") as fw:
		fw.write(rowStr)

def printStats():
	print("Version      :", __version__)
	print("Creation date:", __date__)
	print("Update date  :", __updated__)

#############################
# Main
#############################

def main():
	printStats()
	iniPath = "/home/ipserc/Documentos/Facturas/Iberdrola.Electricidad Galileo 108"
	printTraza(INFO, "Procesando Facturas de ELECTRICIDAD de ", "IBERDROLA")
	excelDataTable = getDataFromPdf_ELEC_IBE(iniPath)
	writeToCSV_ELEC_IBE(iniPath, excelDataTable)

	iniPath = "/home/ipserc/Documentos/Facturas/Gas Natural Fenosa"
	printTraza(INFO, "Procesando Facturas de GAS de ", "NATURGY")
	excelDataTable = getDataFromPdf_GAS_NTRGY(iniPath)
	writeToCSV_GAS_NTRGY(iniPath, excelDataTable)

if __name__ == "__main__":
    main()

