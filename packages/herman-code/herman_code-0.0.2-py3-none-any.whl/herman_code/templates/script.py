"""
A template python script.
"""

import logging
import os
from pathlib import Path
# Third-party packages
import pandas as pd
from sqlalchemy import URL
# Local packages
from herman_code import __version__ as drapiVersion
from herman_code.code import (choosePathToLog,
                              getTimestamp,
                              makeDirPath)

# Arguments: Main
pass

# Arguments: General
LOG_LEVEL = "INFO"

# Arguments: SQL parameters
USER_ID = None
USER_PWD = None
USER_DOMAIN = None
USERNAME = None
SERVER = None
DATABASE = None


if __name__ == "__main__":
    # Variables: Path construction: General
    runTimestamp = getTimestamp()
    thisFilePath = Path(__file__)
    thisFileStem = thisFilePath.stem
    currentWorkingDir = Path(os.getcwd()).absolute()
    projectDir = currentWorkingDir
    dataDir = projectDir.joinpath("data")
    if dataDir:
        inputDataDir = dataDir.joinpath("input")
        intermediateDataDir = dataDir.joinpath("intermediate")
        outputDataDir = dataDir.joinpath("output")
        if intermediateDataDir:
            runIntermediateDir = intermediateDataDir.joinpath(thisFileStem, runTimestamp)
        if outputDataDir:
            runOutputDir = outputDataDir.joinpath(thisFileStem, runTimestamp)
    logsDir = projectDir.joinpath("logs")
    if logsDir:
        runLogsDir = logsDir.joinpath(thisFileStem)
    sqlDir = projectDir.joinpath("sql")

    # Variables: Path construction: Project-specific
    pass

    # Variables: SQL Parameters
    if USER_ID:
        userID = USER_ID[:]
    else:
        userID = fr"{USER_DOMAIN}\{USERNAME}"
    if USER_PWD:
        userPwd = USER_PWD
    else:
        raise Exception("Need password.")
    connectionString = URL.create(drivername="mssql+pymssql",
                                  username=userID,
                                  password=userPwd,
                                  host=SERVER,
                                  database=DATABASE)

    # Variables: Other
    pass

    # Directory creation: General
    makeDirPath(runIntermediateDir)
    makeDirPath(runOutputDir)
    makeDirPath(runLogsDir)

    # Logging block
    logpath = runLogsDir.joinpath(f"log {runTimestamp}.log")
    logFormat = logging.Formatter("""[%(asctime)s][%(levelname)s](%(funcName)s): %(message)s""")

    logger = logging.getLogger(__name__)

    fileHandler = logging.FileHandler(logpath)
    fileHandler.setLevel(9)
    fileHandler.setFormatter(logFormat)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(LOG_LEVEL)
    streamHandler.setFormatter(logFormat)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    logger.setLevel(9)

    logger.info(f"""Begin running "{choosePathToLog(path=thisFilePath, rootPath=projectDir)}".""")
    logger.info(f"""DRAPI-Lemur version is "{drapiVersion}".""")
    logger.info(f"""All other paths will be reported in debugging relative to the current working directory: "{choosePathToLog(path=projectDir, rootPath=projectDir)}".""")
    logger.info(f"""Script arguments:


    # Arguments
    ``: "{""}"

    # Arguments: General
    `LOG_LEVEL` = "{LOG_LEVEL}"
    """)

    # >>> Begin script body >>>

    _ = pd

    # Output location summary
    logger.info(f"""Script output is located in the following directory: "{choosePathToLog(path=runOutputDir, rootPath=projectDir)}".""")

    # <<< End script body <<<
    logger.info(f"""Finished running "{choosePathToLog(path=thisFilePath, rootPath=projectDir)}".""")
