import subprocess
import os

def training(pdbCodeFile, pdbDirPath, outputDirPath = "data_potentials"):
    path = os.path.join(os.path.dirname(__file__), f"bin/training")
    subprocess.run([path, f"-l{pdbCodeFile}", f"-d{pdbDirPath}", f"-o{outputDirPath}"], check=True)

def scoring(pdbFile, potentialsDir):
    path = os.path.join(os.path.dirname(__file__), f"bin/scoring")
    subprocess.run([path, f"-i{pdbFile}", f"-d{potentialsDir}"])

def batch_download(pdbCodeFile, outputDirPath):
    os.mkdir(outputDirPath)
    os.chdir(outputDirPath)
    path = os.path.join(os.path.dirname(__file__), f"bin/batch_download.sh")
    subprocess.run([path, f"-f {pdbCodeFile}", "-p"], check=True)    
    os.system("gzip -d *")
    os.chdir("..")
