import numpy as np
import pandas as pd


class CreateCustomData:

    def __init__(self, timeDurationHot, timeDurationCold, numberRepetitions, dampSlow, wnSlow, dampFast, wnFast):

        #######################################################################
        # Create general parameters:
        timeDelta = 0.01
        tempRefHot = 37
        tempRefCold = 16
        timeDurationHot = 60 * timeDurationHot
        timeDurationCold = 60 * timeDurationCold

        #######################################################################
        # Create time arrays bases for slow thermocyclers:
        phiSlow = np.arctan(np.sqrt(1 - dampSlow ** 2) / dampSlow)
        timeRiseSlow = (np.pi - phiSlow) / (wnSlow * np.sqrt(1 - dampSlow ** 2))
        timeDurationHotSlow = timeDurationHot + timeRiseSlow
        timeDurationColdSlow = timeDurationCold + timeRiseSlow
        timeHotBaseSlow = np.arange(0, timeDurationHotSlow, timeDelta)
        timeColdBaseSlow = np.arange(0, timeDurationColdSlow, timeDelta)
        print(timeHotBaseSlow)

        # Create the complete time array:
        numberSamples = (len(timeHotBaseSlow) + len(timeColdBaseSlow)) * numberRepetitions
        time = np.array(range(numberSamples)) * timeDelta

        # Create reference array bases for slow thermocyclers:
        refHotBaseSlow = tempRefHot * np.ones(len(timeHotBaseSlow))
        refColdBaseSlow = tempRefCold * np.ones(len(timeColdBaseSlow))

        # Create response arrays bases for slow thermocyclers:
        respHotBaseSlow = SecondOrderSystem(timeHotBaseSlow, dampSlow, wnSlow).stepResponse
        respColdBaseSlow = 1 - SecondOrderSystem(timeColdBaseSlow, dampSlow, wnSlow).stepResponse
        respHotBaseSlow = (tempRefHot - tempRefCold) * (respHotBaseSlow - 0.5) + (tempRefHot + tempRefCold) * 0.5
        respColdBaseSlow = (tempRefHot - tempRefCold) * (respColdBaseSlow - 0.5) + (tempRefHot + tempRefCold) * 0.5

        # Create the complete reference and  the response for slow thermocyclers:
        refBaseSlow = np.concatenate((refHotBaseSlow, refColdBaseSlow))
        respBaseSlow = np.concatenate((respHotBaseSlow, respColdBaseSlow))
        refSlow = refBaseSlow
        respSlow = respBaseSlow
        for i in range(numberRepetitions - 1):
            refSlow = np.concatenate((refSlow, refSlow))
            respSlow = np.concatenate((respSlow, respBaseSlow))

        #######################################################################
        # Create time arrays bases for fast thermocyclers:
        timeHotBaseFast = np.arange(0, timeDurationHot, timeDelta)
        timeColdBaseFast = np.arange(0, timeDurationCold, timeDelta)

        # Create reference array bases for fast thermocyclers:
        refHotBaseFast = tempRefHot * np.ones(len(timeHotBaseFast))
        refColdBaseFast = tempRefCold * np.ones(len(timeColdBaseFast))

        # Create response arrays bases for fast thermocyclers:
        respHotBaseFast = SecondOrderSystem(timeHotBaseFast, dampFast, wnFast).stepResponse
        respColdBaseFast = 1 - SecondOrderSystem(timeColdBaseFast, dampFast, wnFast).stepResponse
        respHotBaseFast = (tempRefHot - tempRefCold)*(respHotBaseFast - 0.5) + (tempRefHot + tempRefCold) * 0.5
        respColdBaseFast = (tempRefHot - tempRefCold) * (respColdBaseFast - 0.5) + (tempRefHot + tempRefCold) * 0.5

        # Get the number of repetitions fro fast thermocyclers:
        numberSamplesBaseFast = len(timeHotBaseFast) + len(timeColdBaseFast)
        numberRepetitionsFast = int(np.ceil(numberSamples / numberSamplesBaseFast))

        # Create the complete reference and  the response for fast thermocyclers:
        refBaseFast = np.concatenate((refHotBaseFast, refColdBaseFast))
        respBaseFast = np.concatenate((respHotBaseFast, respColdBaseFast))
        refFast = refBaseFast
        respFast = respBaseFast
        for i in range(numberRepetitionsFast - 1):
            refFast = np.concatenate((refFast, refBaseFast))
            respFast = np.concatenate((respFast, respBaseFast))

        # Remove the final samples for fast thermocyclers:
        refFast = refFast[:numberSamples]
        respFast = respFast[:numberSamples]

        # Create some parameter for the dataframe:
        COLUMN_INDEX = 'index'
        COLUMN_TIME = 'time'
        COLUMN_REF_SLOW = 'refSlow'
        COLUMN_RESP_SLOW = 'respSlow'
        COLUMN_REF_FAST = 'refFast'
        COLUMN_RESP_FAST = 'respFast'
        dataFrame = pd.DataFrame(columns=[COLUMN_TIME, COLUMN_REF_SLOW, COLUMN_RESP_SLOW, COLUMN_REF_FAST, COLUMN_RESP_FAST])

        # Create a data frame with the data:
        dataFrame[COLUMN_TIME] = pd.Series(time) / 60
        dataFrame[COLUMN_REF_SLOW] = pd.Series(refSlow)
        dataFrame[COLUMN_RESP_SLOW] = pd.Series(respSlow)
        dataFrame[COLUMN_REF_FAST] = pd.Series(refFast)
        dataFrame[COLUMN_RESP_FAST] = pd.Series(respFast)
        dataFrame.reset_index(inplace=True)

        # Create lists with info:
        listIndepColumns = [COLUMN_INDEX, COLUMN_TIME]
        listIndepNames = ['index', 'time']
        listIndepUnits = ['', '[min]']
        listIndepMaxs = []
        listIndepMins = []
        for column in listIndepColumns:
            listIndepMaxs.append(dataFrame[column].max())
            listIndepMins.append(dataFrame[column].min())
        listDepenColumns = [COLUMN_REF_SLOW, COLUMN_RESP_SLOW, COLUMN_REF_FAST, COLUMN_RESP_FAST]
        listDepenNames = ['larger reference', 'slow response', 'shorter reference', 'fast response']
        listDepenUnits = ['[°C]', '[°C]', '[°C]', '[°C]']
        listDepenColors = ['m', 'r', 'c', 'b']
        listDepenMaxs = []
        listDepenMins = []
        for column in listDepenColumns:
            listDepenMaxs.append(dataFrame[column].max())
            listDepenMins.append(dataFrame[column].min())

        # Create dictionaries with info:
        dictIndepVariables = []
        for i in range(len(listIndepColumns)):
            dictIndepVariables.append({
                'column': listIndepColumns[i],
                'name': listIndepNames[i],
                'unit': listIndepUnits[i],
                'max': listIndepMaxs[i],
                'min': listIndepMins[i]
            })

        dictDepenVariables = []
        for i in range(len(listDepenColumns)):
            dictDepenVariables.append({
                'column': listDepenColumns[i],
                'name': listDepenNames[i],
                'unit': listDepenUnits[i],
                'max': listDepenMaxs[i],
                'min': listDepenMins[i]
            })

        # Create public attributes:
        CreateCustomData.dataFrame = dataFrame
        CreateCustomData.listIndepColumns = listIndepColumns
        CreateCustomData.listIndepNames = listIndepNames
        CreateCustomData.listIndepUnits = listIndepUnits
        CreateCustomData.listIndepMaxs = listIndepMaxs
        CreateCustomData.listIndepMins = listIndepMins
        CreateCustomData.dictIndepVariables = dictIndepVariables
        CreateCustomData.listDepenColumns = listDepenColumns
        CreateCustomData.listDepenNames = listDepenNames
        CreateCustomData.listDepenUnits = listDepenUnits
        CreateCustomData.listDepenColors = listDepenColors
        CreateCustomData.dictDepenVariables = dictDepenVariables
        CreateCustomData.listDepenMaxs = listDepenMaxs
        CreateCustomData.listDepenMins = listDepenMins


class SecondOrderSystem:

    def __init__(self, t, damp, wn):

        phi = np.arctan(np.sqrt(1 - damp ** 2) / damp)
        timeRise = (np.pi - phi) / (wn * np.sqrt(1 - damp ** 2))

        timeOvershoot = np.pi / (wn * np.sqrt(1 - damp ** 2))
        timeSettling = 4 / (wn * damp)
        valueOvershoot = np.exp(-np.pi * damp / np.sqrt(1 - damp ** 2))

        wd = wn * np.sqrt(1 - damp ** 2)
        stepResponse = 1 - np.exp(-damp*wn*t)*((np.sqrt(1-damp**2))*np.cos(wd*t) + damp*np.sin(wd*t))/np.sqrt(1-damp**2)

        print('#####################################')
        print('Second Order Response Created.')
        print('damp: ' + str(damp))
        print('wn: ' + str(wn))
        print('timeRise: ' + str(timeRise))
        print('timeOvershoot: ' + str(timeOvershoot))
        print('timeSettling: ' + str(timeSettling))
        print('valueOvershoot: ' + str(valueOvershoot))

        SecondOrderSystem.timeSettling = timeSettling
        SecondOrderSystem.timeOvershoot = timeOvershoot
        SecondOrderSystem.valueOvershoot = valueOvershoot
        SecondOrderSystem.wd = wd
        SecondOrderSystem.stepResponse = stepResponse
