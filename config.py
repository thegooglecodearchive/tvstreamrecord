"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: pavion
"""

configuration = [
[
'cfg_xmltvinitpath',
'Initial path for an XMLTV-Import',
'http://xmltv.spaetfruehstuecken.org/xmltv/datalist.xml.gz'
],

[
'cfg_purgedelta',
'Purge database records older than [days]',
30
],

[
'cfg_delta_for_epg',
'Lenghten an EPG-record (delta before and after), [minutes]',
3
],

[
'cfg_recordpath',
'Path for your recordings',
'/volume1/common/'
],

[
'cfg_server_bind_address',
'Server bind address (restart needed)',
'0.0.0.0'
],   

[
'cfg_server_port',
'Server port (restart needed)',
8030
],

[
'cfg_file_extension',
'File extension for the recorded stream (default=".ts")',
'.ts'
]
                 
]

for config in configuration:
    globals()[config[0]] = config[2]
    
def getDict():
    ret = []
    for r in globals():
        if r[0:4] =='cfg_':
            ret.append(r)
    return ret

def loadConfig():
    from sql import sqlRun
    sqlRun("INSERT OR IGNORE INTO config VALUES (?, ?, ?)",configuration,1)
    rows = sqlRun("SELECT param, value FROM config WHERE param<>'cfg_version'")
    setConfig(rows)
    return
        
def setConfig(attrlist = []):
    for attr in attrlist:
        if attr[0] in globals():
            globals()[attr[0]] = attr[1]                
    saveConfig()
            
            
def saveConfig():
    from sql import sqlRun
    sql = ''   
    for var in getDict():
        sql += "UPDATE config SET value='%s' WHERE param='%s';" % (globals()[var], var) 
    sqlRun(sql, -1, 1)
    return    
        
