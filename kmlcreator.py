import pandas as pd
import PySimpleGUI as sg
import xml.dom.minidom
import os
import math

# create data for format table
table_header = ['SITEID', 'CELLID', 'SITENAME', 'TECH', 'AZIMUTH', 'DECLAT', 'DECLON', 'BW']
table_data = [['1', '1A', 'name', 'GSM', '120', '-30.12345', '30.12345', '65']]

# Define global variables
sitelist = pd.DataFrame()
header_list = ()
global_string = ''
listval = 0

# Import file into dataframe
def import_csv_into_db():
    sitelist=pd.read_csv(values['Browse'])
    #Remove invalid entries for XML format
    sitelist=sitelist.replace(regex=['&'], value='&amp;')
    # Remove duplicate site entries
    sites=sitelist.drop_duplicates("SITEID")[['SITEID', 'SITENAME','DECLAT','DECLON']]
    header_list = sitelist.iloc[0].tolist()
    # Create technology lists
    global techs
    techs=sitelist.drop_duplicates("TECH")[['TECH']]
    # Create image length list to append to tech list, starting from largest to smallest
    i=0
    tech_index = []
    for item in techs.iterrows():
        tech_index.append(0.003 - i*0.0003)
        i+=1
    # Add image length list to techs list
    techs['IMG_LEN'] = tech_index
    # Create colour list to append to tech list
    k=0
    colour_index = []
    for item in techs.iterrows():
        colour_index.append(k + 70)
        k+=1
    # Add colour list to tech list
    techs['COLOUR'] = colour_index
    # Create default XML script for first part of XML file
    part1 = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"><Document><name>KML_Created_file.kml</name><Style id="s_ylw-pushpin_hl3"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ff00ffff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="failed"><LineStyle><color>ff00ffff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="failed0"><LineStyle><color>ffffff00</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="failed1"><LineStyle><color>ff0055ff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><StyleMap id="m_ylw-pushpin75"><Pair><key>normal</key><styleUrl>#failed0</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl1</styleUrl></Pair></StyleMap><Style id="failed2"><LineStyle><color>ff00ff00</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><StyleMap id="m_ylw-pushpin74"><Pair><key>normal</key><styleUrl>#failed5</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl0</styleUrl></Pair></StyleMap><StyleMap id="m_ylw-pushpin30"><Pair><key>normal</key><styleUrl>#s_ylw-pushpin40</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl30</styleUrl></Pair></StyleMap><StyleMap id="m_ylw-pushpin72"><Pair><key>normal</key><styleUrl>#failed1</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl</styleUrl></Pair></StyleMap><StyleMap id="m_ylw-pushpin76"><Pair><key>normal</key><styleUrl>#failed3</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl4</styleUrl></Pair></StyleMap><Style id="s_ylw-pushpin_hl4"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ff7f00ff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="s_ylw-pushpin_hl"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ff0055ff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="failed3"><LineStyle><color>ff7f00ff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="s_ylw-pushpin40"><IconStyle><scale>0.4</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle><LabelStyle><scale>0.9</scale></LabelStyle><LineStyle><color>cc00ff00</color><width>1.5</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><StyleMap id="m_ylw-pushpin73"><Pair><key>normal</key><styleUrl>#failed4</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl2</styleUrl></Pair></StyleMap><StyleMap id="m_ylw-pushpin70"><Pair><key>normal</key><styleUrl>#failed2</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl5</styleUrl></Pair></StyleMap><Style id="s_ylw-pushpin_hl2"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ff0000ff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="s_ylw-pushpin_hl1"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ffffff00</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="failed4"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="s_ylw-pushpin_hl0"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ffff0000</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><StyleMap id="m_ylw-pushpin71"><Pair><key>normal</key><styleUrl>#failed</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl3</styleUrl></Pair></StyleMap><Style id="s_ylw-pushpin_hl30"><IconStyle><scale>0.472727</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href></Icon></IconStyle><LabelStyle><scale>0.9</scale></LabelStyle><LineStyle><color>cc00ff00</color><width>1.5</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="failed5"><LineStyle><color>ffff0000</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="s_ylw-pushpin_hl5"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/></IconStyle><LineStyle><color>ff00ff00</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>'
    part2 = '<Folder><name>Sitename</name><open>1</open>'
    part3 = '<Placemark><name>'
    part4 = '</name><styleUrl>#m_ylw-pushpin30</styleUrl><Point><extrude>1</extrude><altitudeMode>relativeToGround</altitudeMode><coordinates>'
    part5 = '</coordinates></Point></Placemark>'
    part6 = '</Folder>'
    part7 = '</Document></kml>'
    secpart1 = '<Folder><name>'
    secpart2 = '</name>'
    secpart3 = '<Placemark><name>'
    secpart4 = '</name><styleUrl>#m_ylw-pushpin'
    secpart5 = '</styleUrl><Polygon><extrude>1</extrude><tessellate>1</tessellate><outerBoundaryIs><LinearRing><coordinates>'
    secpart6 = '</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
    secpart7 = '</Folder>'

    for index, data2 in techs.iterrows():
        global listval
        if sg.OneLineProgressMeter('Progress...', listval, len(techs)-1,'--progress__', bar_color=('blue', 'white'), orientation='h') is False:
            break
        listval += 1
        global placemark_str
        placemark_str = ''
        for index, data in sites.iterrows():
            placemark_str = placemark_str + part3 + ('{} - {}'). format(data['SITEID'], data['SITENAME']) + part4 + ('{},{}'). format(data['DECLON'], data['DECLAT']) + part5
        global sector_str
        sector_str = ''
        for index, data in sitelist[sitelist.TECH == data2['TECH']].iterrows():
            sector_split = []
            azimuth_split = []
            for  i in range(0,data['BW'], 10):
                azimuth_split.append(data['AZIMUTH'] - data['BW']/2 +(i))
            azimuth_split.append(data['AZIMUTH'] + data['BW']/2)
            if data['BW'] != 360:
                sector_split.append(data['DECLON'])
                sector_split.append(data['DECLAT'])
                sector_split.append(0)
            for i in azimuth_split:
                sector_split.append(data['DECLON'] + math.sin(math.radians(i))*data2['IMG_LEN'])
                sector_split.append(data['DECLAT'] + math.cos(math.radians(i))*data2['IMG_LEN'])
                sector_split.append(0)
            if data['BW'] != 360:
                sector_split.append(data['DECLON'])
                sector_split.append(data['DECLAT'])
                sector_split.append(0)
            sector_split = str(sector_split).replace('[','').replace('[','').replace(' ','')
            sector_str = sector_str + secpart3 + ('{}'). format(data['CELLID']) + secpart4 + str(data2['COLOUR']) + secpart5 + str(sector_split) + secpart6
        sector_str = secpart1 + data['TECH'] + secpart2 + sector_str + secpart7
        global global_string
        global_string = global_string + sector_str
        if values['__sites__'] and values['__sectors__']:
            placemark_str = part1 + part2 + placemark_str + part6 + global_string + part7
        elif values['__sites__'] and not values['__sectors__']:
            placemark_str = part1 + part2 + placemark_str + part6 + part7
        elif values['__sectors__'] and not values['__sites__']:
            placemark_str = part1 + global_string + part7
        else:
            placemark_str = part1 + part7
        # use xml.dom.minidom to parseString to xml default formatting
        placemark_str = xml.dom.minidom.parseString(placemark_str).toprettyxml()

menu_def = [['&File', ['E&xit']],
            ['&Help', ['&About...']] ]

sg.change_look_and_feel('SystemDefaultForReal')    # Add a touch of color
# Window layout.
layout = [  [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
            [sg.Text('When importing a CSV, please ensure the column heading follow the table example below:')],
            [sg.Table(values=table_data,headings=table_header, auto_size_columns=False, background_color='light gray' ,hide_vertical_scroll=True, justification='center' ,num_rows=1)],
            [sg.Text('')],
            [sg.Text('Import Location:',), sg.Text(justification='right', background_color= 'white', size=[30,1]), sg.FileBrowse(auto_size_button=False)],
            [sg.Checkbox('Create Sites (Only unique site IDs will be used)',key='__sites__')],
            [sg.Checkbox('Create Sectors (Grouped by technology)', key='__sectors__')],
            [sg.Text('Export Location:',), sg.Text(justification='right', background_color= 'white', size=[30,1]), sg.FileSaveAs(key='export_location', button_text='Browse', file_types=(('Kml', '*.kml'),('All Files', '*.*')) , auto_size_button=False), sg.Ok(button_text='Export', key='__export__' ,auto_size_button=False), sg.Exit(auto_size_button=False)],
        ]

# Create the Window
window = sg.Window('KML Creator', layout, icon = 'tower.png')

# Event Loop to process "events" and get the "values" of the inputs
while True:                             # The Event Loop
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    elif event == 'About...':
        sg.popup('KML Creator', 'Version 1.3',
                'https://github.com/mtneben/kmlcreator',  grab_anywhere=True)
    if values['Browse'] != None and values['export_location'] != None and event == '__export__':
        import_csv_into_db()
        export_location = values['export_location']
        with open(export_location, 'w') as out:
            out.write(placemark_str)
        sg.popup_auto_close('Export Successful. Program will close automatically', auto_close_duration=4)
        window.close()

window.close()