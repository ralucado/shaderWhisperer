import configparser
import sys
import logging
class Setup():
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read("configuration.ini")
        loglevel = self._config['ADVANCED']['Log_Level']
        logfile = self._config['ADVANCED']['Log_File']
        numeric_level = getattr(logging, loglevel.upper(), None)
        self._space = self._config['DEFAULT']['Constant_Coord_Space']
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        if logfile != "NONE":
            logging.basicConfig(filename=logfile,level=numeric_level)
        else:
            logging.basicConfig(level=numeric_level)
    
    def getEncoding(self):
        codings = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp65001', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']
        encoding = self._config['DEFAULT'].get('Encoding', 'utf_8')
        if(encoding in codings):
            return encoding
        sys.stderr.write("WARNING: Specified encoding "+str(encoding)+" not available. Falling back to utf_8.")
        return "utf_8"
    
    def getDefaultVars(self):
        configVars = self._config['VARIABLES']
        vars = {}
        vars[configVars['Model_Matrix']] = ('mat4','transform.object.world')
        vars[configVars['View_Matrix']] = ('mat4','transform.world.eye')
        vars[configVars['Projection_Matrix']] = ('mat4','transform.eye.clip')
        vars[configVars['ModelView_Matrix']] = ('mat4','transform.object.eye')
        vars[configVars['ModelViewProjection_Matrix']] = ('mat4','transform.object.clip')
        vars[configVars['Model_Inverse_Matrix']] = ('mat4','transform.world.object')
        vars[configVars['View_Inverse_Matrix']] = ('mat4','transform.eye.world')
        vars[configVars['Projection_Inverse_Matrix']] = ('mat4','transform.clip.eye')
        vars[configVars['ModelView_Inverse_Matrix']] = ('mat4','transform.eye.object')
        vars[configVars['ModelViewProjection_Inverse_Matrix']] = ('mat4','transform.clip.object')
        vars[configVars['Vertex']] = ('vec3','object')
        vars[configVars['Normal']] = ('vec3','object')
        vars[configVars['Normal_Matrix']] = ('mat3','transform.object.eye')
        vars[configVars['BoundingBox_Min']] = ('vec3','object')
        vars[configVars['BoundingBox_Max']] = ('vec3','object')
        vars[configVars['Light_Position']] = ('vec4','eye')

        vars['glPosition'] = 'vec4'

        return vars

    def getBuiltins(self):
        builtins = {}

        configVars = self._config['VARIABLES']
        builtins[configVars['Model_Matrix']] = 'mat4'
        builtins[configVars['View_Matrix']] = 'mat4'
        builtins[configVars['Projection_Matrix']] = 'mat4'
        builtins[configVars['ModelView_Matrix']] = 'mat4'
        builtins[configVars['ModelViewProjection_Matrix']] = 'mat4'
        builtins[configVars['Model_Inverse_Matrix']] = 'mat4'
        builtins[configVars['View_Inverse_Matrix']] = 'mat4'
        builtins[configVars['Projection_Inverse_Matrix']] = 'mat4'
        builtins[configVars['ModelView_Inverse_Matrix']] = 'mat4'
        builtins[configVars['ModelViewProjection_Inverse_Matrix']] = 'mat4'
        builtins[configVars['Vertex']] = 'vec3'
        builtins[configVars['Normal']] = 'vec3'
        builtins[configVars['Normal_Matrix']] = 'mat3'
        builtins[configVars['BoundingBox_Min']] = 'vec3'
        builtins[configVars['BoundingBox_Max']] = 'vec3'
        builtins[configVars['Light_Position']] = 'vec4'

        builtins['gl_Position'] = 'vec4'
        builtins['gl_PointSize'] = 'float'
        builtins['gl_FragCoord'] = 'vec4'
        builtins['gl_FrontFacing'] = 'bool'
        builtins['gl_PointCoord'] = 'int'
        builtins['gl_FragColor'] = 'vec4'

        builtins['func.radians'] = 'genType'
        builtins['func.degrees'] = 'genType'
        builtins['func.sin'] = 'genType'
        builtins['func.cos'] = 'genType'
        builtins['func.tan'] = 'genType'
        builtins['func.asin'] = 'genType'
        builtins['func.acos'] = 'genType'
        builtins['func.atan'] = 'genType'
        builtins['func.pow'] = 'genType'
        builtins['func.exp'] = 'genType'
        builtins['func.log'] = 'genType'
        builtins['func.exp2'] = 'genType'
        builtins['func.log2'] = 'genType'
        builtins['func.sqrt'] = 'genType'
        builtins['func.inversesqrt'] = 'genType'
        builtins['func.abs'] = 'genType'
        builtins['func.sign'] = 'genType'
        builtins['func.floor'] = 'genType'
        builtins['func.ceil'] = 'genType'
        builtins['func.fract'] = 'genType'
        builtins['func.mod'] = 'genType'
        builtins['func.min'] = 'genType'
        builtins['func.max'] = 'genType'
        builtins['func.clamp'] = 'genType'
        builtins['func.mix'] = 'genType'
        builtins['func.step'] = 'genType'
        builtins['func.smoothstep'] = 'genType'
        builtins['func.length'] = 'float'
        builtins['func.distance'] = 'float'
        builtins['func.dot'] = 'float'
        builtins['func.cross'] = 'vec3'
        builtins['func.normalize'] = 'genType'
        builtins['func.faceforward'] = 'genType'
        builtins['func.reflect'] = 'genType'
        builtins['func.refract'] = 'genType'
        builtins['func.matrixCompMult'] = 'genType'
        builtins['func.lessThan'] = 'boolType'
        builtins['func.lessThanEqual'] = 'boolType'
        builtins['func.greaterThan'] = 'boolType'
        builtins['func.greaterThanEqual'] = 'boolType'
        builtins['func.equal'] = 'boolType'
        builtins['func.notEqual'] = 'boolType'
        builtins['func.any'] = 'bool'
        builtins['func.all'] = 'bool'
        builtins['func.not'] = 'boolType'
        builtins['func.texture2D'] = 'vec4'
        builtins['func.texture'] = 'float'
        builtins['func.textureCube'] = 'vec4'

        return builtins





    def setConstantExpressionSpace(self, space):
        self._space = space 
    
    def getConstantExpressionSpace(self):
        return self._space