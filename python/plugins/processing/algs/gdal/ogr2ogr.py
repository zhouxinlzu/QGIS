# -*- coding: utf-8 -*-

"""
***************************************************************************
    ogr2ogr.py
    ---------------------
    Date                 : November 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'November 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.core import (QgsProcessingException,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterString,
                       QgsProcessingParameterVectorDestination)
from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils


class ogr2ogr(GdalAlgorithm):

    INPUT = 'INPUT'
    OPTIONS = 'OPTIONS'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              self.tr('Input layer')))

        options_param = QgsProcessingParameterString(self.OPTIONS,
                                                     self.tr('Additional creation options'),
                                                     defaultValue='',
                                                     optional=True)
        options_param.setFlags(options_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(options_param)

        self.addParameter(QgsProcessingParameterVectorDestination(self.OUTPUT,
                                                                  self.tr('Converted')))

    def name(self):
        return 'convertformat'

    def displayName(self):
        return self.tr('Convert format')

    def group(self):
        return self.tr('Vector conversion')

    def commandName(self):
        return 'ogr2ogr'

    def getConsoleCommands(self, parameters, context, feedback):
        ogrLayer, layerName = self.getOgrCompatibleSource(self.INPUT, parameters, context, feedback)
        options = self.parameterAsString(parameters, self.OPTIONS, context)
        outFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        output, outputFormat = GdalUtils.ogrConnectionStringAndFormat(outFile, context)

        if outputFormat == 'SQLite' and os.path.isfile(output):
            raise QgsProcessinException(self.tr('Output file "{}" already exists.'.format(output)))

        arguments = []
        if outputFormat:
            arguments.append('-f {}'.format(outputFormat))

        if options:
            arguments.append(options)

        arguments.append(output)
        arguments.append(ogrLayer)
        arguments.append(layerName)

        return ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
