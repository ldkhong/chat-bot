import json

#Symbol : atomic number
symbol_lookup = {
    'h': 1, 'he':2,'li':3 ,'be': 4,'b':5,'c':6,'n':7,'o':8,'f':9,'ne':10,
    'na':11,'mg':12,'al':13,'si':14,'p':15,'s':16,'cl':17,'ar':18,
    'k':19,'ca':20,'ga':31,'ge':32,'as':33,'se':34,'br':35,'kr':36,
    'rb':37,'sr':38,'in':49,'sn':50,'sb':51,'te':52,'i':(53, 0),'xe':(54, 0),
    'cs':55,'ba':56,'tl':81,'pb':82,'bi':83,'po':84,'at':85,'rn':(86, 0),
    'fr':87,'ra':88,'nh':113,'fl':114,'mc':115,'lv':116,'ts':117,'og':118,
    'uue':119,
    'sc':21,'ti':22,'v':23,'cr':24,'mn':25,'fe':26,'co':27,'ni':28,'cu':29,'zn':30,
    'Y':39,'zr':40,'nb':41,'mo':42,'tc':43,'ru':44,'rh':45,'pd':46,'ag':47,'cd':48,
    'hf':72,'ta':73,'w':74,'re':75,'os':76,'ir':77,'pt':78,'au':79,'hg':80,
    'rf':104,'db':105,'sg':106,'bh':107,'hs':108,'mt':109,'ds':110,'rg':111,'cn':112,
    'la':57,'ce':58,'pr':59,'nd':60,'pm':61,'sm':62,'eu':63,'gd':64,'tb':65,'dy':66,'ho':67,'er':68,'tm':69,'yb':70,'lu':71,
    'ac':89,'th':90,'pa':91,'u':92,'np':93,'pu':94,'am':95,'cm':96,'bk':97,'cf':98,'es':99,'fm':100,'md':101,'no':102,'lr':103,
}
#(CAS name, recommended name, list of element's atomic numbers)
group_elements = [
    ('ia','hydrogen and alkali metals',[1,3,11,19,37,55,87]),
    ('iia','alkaline earth metals',[4,12,20,38,56,88]),
    ('iiib', 'scandium family', [21,39,71,103]),
    ('ivb','',[22,40,72,104]),
    ('vb','',[23,41,73,105]),
    ('vib','',[24,42,74,106]),
    ('viib','',[25,43,75,107]),
    ('viiib','',[26,44,76,108]),
    ('viiib','',[27,45,77,109]),
    ('viiib','',[28,46,78,110]),
    ('ib','',[29,47,79,111]),
    ('iib','',[30,48,80,112]),
    ('iiia','',[5,13,31,49,81,113]),
    ('iva','',[6,14,32,50,82,114]),
    ('va','pnictogens',[7,15,33,51,83,115]),
    ('via','chalcogens',[8,16,34,52,84,116]),
    ('viia','halogens',[9,17,35,53,85,117]),
    ('viiia','noble gases',[2,10,18,36,54,86,118]),
]
# (first element, last element)
period_elements =[(1,2),(3,10),(11,18),
    (19,36),(37,54),(55,86),(87,118)]
#atomic numbers of nonmetal_element
nonmetal_element =[1,2,5,6,7,8,9,10,14,15,16,17,18,32,33,34,35,36,51,52,53,54,84,85,86,117,118]

def getFile(filePath):
    f = open(filePath)
    json_str = f.read()
    f.close()
    return json.loads(json_str)

periodic_lookup = getFile("periodic-table-lookup.json")

def getInformation(isSymbol,value,info):
    if info in ['electrons','electron','proton','protons','number']:
        info = 'number'
    if info == 'g/mol':
        info = 'atomic_mass'
    if isSymbol:
        value = periodic_lookup['order'][symbol_lookup[value]-1]
    if info:
        return periodic_lookup[value][info]
    else:
        return periodic_lookup[value]['summary']

def countElements(pos,isCol):
    if isCol:
        if isinstance(pos, int):
            return len(group_elements[pos][2])
        else:
            for col in group_elements:
                if pos.lower() == col[0]:
                    return len(col[2])  
    else:
        if isinstance(pos, int):
            return period_elements[pos][1] - period_elements[pos][0] + 1
    return -1

