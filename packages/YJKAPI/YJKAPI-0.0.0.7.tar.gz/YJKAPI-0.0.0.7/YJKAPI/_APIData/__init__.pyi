class DdeErrorState:
    kdeOK = 0
    kdeInvalidName = 1
    kdeInvalidInputArg = 2
    kdeInvalidKey = 3
    kdeInvalidPath = 4
    kdeInvalidContext = 5
    kdeContainerIsFull = 6
    kdeInvalidObj = 7
    kdeIdDuplicated = 8
    kdeNotImplemented = 9
    kdeObjNotFound = 10
    kdeObjDuplicated = 11
    kdeModifyConstant = 12
    kdeInvalidModule = 13
    kdeInvalidType = 10000
    kdeTypeNotFound = 10001
    kdeTypeDuplicated = 10002
    kdeInvalidParentType = 10003
    kdeParentTypeNotFound = 10004
    kdeTypeMismatch = 10005
    kdeTypeHasRef = 10006

class Mdl_DTHFLOORINDEX:
    xMaxValue: list[float]
    yMaxValue: list[float]
    xCQCMaxValue: list[float]
    yCQCMaxValue: list[float]
class Mdl_LinkKeCeData:
    Type: LinkType
    NonLinear: list[int]
    Linear: list[int]
    EquKe: list[float]
    EquCe: list[float]
    Ks: list[float]
    ParmA: list[float]
    ParmB: list[float]
    ParmC: list[float]
class Mdl_JcModelDBData_Py:
    m_LoadZHFloat: list
    m_jcVer: list
    m_jcNode: list
    m_jcAppDJ: list
    m_jcIwag: list
    m_jcAppBrace: list
    m_jcAppColumn: list
    m_jcAppDais: list
    m_jcAppElevator: list
    m_jcAppFbeam: list
    m_jcAppFwall: list
    m_jcAppLL: list
    m_jcAppPile: list
    m_jcAppTJ: list
    m_jcAppwall: list
    m_jcAppWaterPipe: list
    m_jcAppWaterPit: list
    m_jcAxis: list
    m_jcCalPara: list
    m_jcDaisCir: list
    m_jcDaisPt: list
    m_jcDaisStepH: list
    m_jcDEFBrace: list
    m_jcDEFColumn: list
    m_jcDEFDais: list
    m_jcDEFDJ: list
    m_jcDEFElevator: list
    m_jcDEFFbeam: list
    m_jcDEFFwall: list
    m_jcDEFLL: list
    m_jcDEFPile: list
    m_jcDEFRaftY: list
    m_jcDEFTJ: list
    m_jcDEFWall: list
    m_jcDEFWaterPipe: list
    m_jcDEFWaterPit: list
    m_jcDEFZD: list
    m_jcHouJiaoDai: list
    m_jcLoads: list
    m_jcLoadsFuJiaLine: list
    m_jcLoadsFuJiaPoint: list
    m_jcLoadsLine: list
    m_jcLoadsDiaoChe: list
    m_jcLoadsLineDiaoChe: list
    m_jcLoadsZDYLine: list
    m_jcLoadsZDYPoint: list
    m_jcLoadV2ArcShow: list
    m_jcLoadV2LineCal: list
    m_jcLoadV2LineShow: list
    m_jcLoadV2LoadCase: list
    m_jcLoadV2Point: list
    m_jcLoadZhuHe: list
    m_jcLoadZHReal: list
    m_jcLoadZHFloat: list
    m_jcLoadArc: list
    m_jcLoadChose: list
    m_jcLoadLine: list
    m_jcLoadZDYArc: list
    m_jcLoadZDYLine: list
    m_jcParaNums: list
    m_jcPointsLoad: list
    m_jcRaftCornerPoint: list
    m_jcRaftSlab: list
    m_jcRaftYInfo: list
    m_jcZDYName: list
    m_jcChildRaft: list
class Mdl_JcModelDBData:
    m_LoadZHFloatList: list[Mdl_jc_LoadZH_Float]
    m_jcVerList: list[Mdl_jc_ver]
    m_jcNodeList: list[Mdl_jc_node]
    m_jcAppDJList: list[Mdl_jc_app_DJ]
    m_jcIwagList: list[Mdl_jc_iwag]
    m_jcAppBraceList: list[Mdl_jc_app_brace]
    m_jcAppColumnList: list[Mdl_jc_app_column]
    m_jcAppDaisList: list[Mdl_jc_app_dais]
    m_jcAppElevatorList: list[Mdl_jc_app_Elevator]
    m_jcAppFbeamList: list[Mdl_jc_app_fbeam]
    m_jcAppFwallList: list[Mdl_jc_app_fwall]
    m_jcAppLLList: list[Mdl_jc_app_LL]
    m_jcAppPileList: list[Mdl_jc_app_Pile]
    m_jcAppTJList: list[Mdl_jc_app_TJ]
    m_jcAppwallList: list[Mdl_jc_app_wall]
    m_jcAppWaterPipeList: list[Mdl_jc_app_WaterPipe]
    m_jcAppWaterPitList: list[Mdl_jc_app_WaterPit]
    m_jcAxisList: list[Mdl_jc_axis]
    m_jcCalParaList: list[Mdl_jc_CalPara]
    m_jcDaisCirList: list[Mdl_jc_dais_Cir]
    m_jcDaisPtList: list[Mdl_jc_dais_pt]
    m_jcDaisStepHList: list[Mdl_jc_dais_stepH]
    m_jcDEFBraceList: list[Mdl_jc_DEF_brace]
    m_jcDEFColumnList: list[Mdl_jc_DEF_column]
    m_jcDEFDaisList: list[Mdl_jc_DEF_dais]
    m_jcDEFDJList: list[Mdl_jc_DEF_DJ]
    m_jcDEFElevatorList: list[Mdl_jc_DEF_Elevator]
    m_jcDEFFbeamList: list[Mdl_jc_DEF_fbeam]
    m_jcDEFFwallList: list[Mdl_jc_DEF_fwall]
    m_jcDEFLLList: list[Mdl_jc_DEF_LL]
    m_jcDEFPileList: list[Mdl_jc_DEF_Pile]
    m_jcDEFRaftYList: list[Mdl_jc_DEF_RaftY]
    m_jcDEFTJList: list[Mdl_jc_DEF_TJ]
    m_jcDEFWallList: list[Mdl_jc_DEF_wall]
    m_jcDEFWaterPipeList: list[Mdl_jc_DEF_WaterPipe]
    m_jcDEFWaterPitList: list[Mdl_jc_DEF_WaterPit]
    m_jcDEFZDList: list[Mdl_jc_DEF_ZD]
    m_jcHouJiaoDaiList: list[Mdl_jc_HouJiaoDai]
    m_jcLoadsList: list[Mdl_jc_Loads]
    m_jcLoadsFuJiaLineList: list[Mdl_jc_LoadsFuJia_Line]
    m_jcLoadsFuJiaPointList: list[Mdl_jc_LoadsFuJia_Point]
    m_jcLoadsLineList: list[Mdl_jc_LoadsLine]
    m_jcLoadsDiaoCheList: list[Mdl_jc_Loads_diaoche]
    m_jcLoadsLineDiaoCheList: list[Mdl_jc_Loads_line_diaoche]
    m_jcLoadsZDYLineList: list[Mdl_jc_Loads_ZiDingYi_Line]
    m_jcLoadsZDYPointList: list[Mdl_jc_Loads_ZiDingYi_Point]
    m_jcLoadV2ArcShowList: list[Mdl_jc_LoadV2_Arc_Show]
    m_jcLoadV2LineCalList: list[Mdl_jc_LoadV2_Line_Cal]
    m_jcLoadV2LineShowList: list[Mdl_jc_LoadV2_Line_Show]
    m_jcLoadV2LoadCaseList: list[Mdl_jc_LoadV2_LoadCase]
    m_jcLoadV2PointList: list[Mdl_jc_LoadV2_Point]
    m_jcLoadZhuHeList: list[Mdl_jc_LoadZhuHe]
    m_jcLoadZHRealList: list[Mdl_jc_LoadZH_real]
    m_jcLoadZHFloatList: list[Mdl_jc_LoadZH_Float]
    m_jcLoadArcList: list[Mdl_jc_Load_Arc]
    m_jcLoadChoseList: list[Mdl_jc_load_Chose]
    m_jcLoadLineList: list[Mdl_jc_Load_Line]
    m_jcLoadZDYArcList: list[Mdl_jc_Load_ZiDingYi_Arc]
    m_jcLoadZDYLineList: list[Mdl_jc_load_ZiDingYi_Line]
    m_jcParaNumsList: list[Mdl_jc_ParaNums]
    m_jcPointsLoadList: list[Mdl_jc_Points_Load]
    m_jcRaftCornerPointList: list[Mdl_jc_RaftCornerPoint]
    m_jcRaftSlabList: list[Mdl_jc_RaftSlab]
    m_jcRaftYInfoList: list[Mdl_jc_RaftYInfo]
    m_jcZDYNameList: list[Mdl_jc_ZiDingYi_Name]
    m_jcChildRaftList: list[Mdl_jc_ChildRaft]
    def ToPyList(self) -> Mdl_JcModelDBData_Py: ...
class Mdl_jc_ver:
    ID: int
    version: str
    CreateVer: str
    strPath: str
    projflag: int
    LoadFlag: int
class Mdl_jc_node:
    ID: int
    X: float
    Y: float
    Z: float
    id_old: int
    jcAdd: int
class Mdl_jc_app_DJ:
    ID: int
    nj: int
    kind: int
    ex: float
    ey: float
    ang: float
    nMarkCho: int
    dBotElevat: float
    isBGAbs: int
    padd: float
    fk: float
    amb: float
    amd: float
    lNewFlag: int
    fk_dd: float
    HSoil_dd: float
    ex2: float
    ey2: float
    ang2: float
    baseZ: float
    bFea: int
    fk_Euro: float
class Mdl_jc_iwag:
    ID: int
    nbg: int
    ned: int
    ngrid: int
    lID: int
    nAxis: int
    nCeng: int
    id_old: int
    jcAdd: int
    lIDRaft: int
    lIDDefY_L: int
    lIDDefY_R: int
    cName: str
class Mdl_jc_app_brace:
    ID: int
    nj: int
    kind: int
    ex1: int
    ey1: int
    ez1: int
    ex2: int
    ey2: int
    ez2: int
    ang: float
    ex: float
    ey: float
    nodeId: float
    idUp: int
    vX: float
    vY: float
    vZ: float
    ptX: float
    ptY: float
    ptZ: float
class Mdl_jc_app_column:
    ID: int
    nj: int
    kind: int
    ex: float
    ey: float
    ez: float
    ang: float
    lKJZKind: int
    lZDKind: int
    zd_ec: int
    zd_nc: int
    hgh: float
    baseZ: int
    idUp: int
    levelh: int
class Mdl_jc_app_dais:
    ID: int
    kind: int
    nj: int
    ex: float
    ey: float
    ang: float
    nMarkCho: int
    idaispilelen: float
    dBotElevat: float
    isBGAbs: int
    padd: int
    fk: float
    amb: float
    amd: float
    lNewFlag: int
    fk_dd: float
    HSoil_dd: float
    baseZ: int
    pile_peijin_para: str
    Fumozupara: str
    bFea: int
    fk_Euro: float
class Mdl_jc_app_Elevator:
    ID: int
    kind: int
    nRaftID: int
    ang: float
    cenx: float
    ceny: float
    npt: int
    ptx: str
    pty: str
class Mdl_jc_app_fbeam:
    ID: int
    nbg: int
    ned: int
    kind: int
    ec: int
    ngrid: int
    ngrid2: int
    nMarkCho: int
    dBotElevat: float
    isBGAbs: int
    fl_njl: float
    fl_njr: float
    padd: int
    fk: float
    amb: float
    amd: float
    fk_dd: float
    HSoil_dd: float
    jcAdd: int
    baseZ: float
    idUp: float
    strY: str
    SoilK: float
    fk_Euro: float
class Mdl_jc_app_fwall:
    ID: int
    nbg: int
    ned: int
    kind: int
    ec: int
    ngrid: int
    hgh: float
class Mdl_jc_app_LL:
    ID: int
    nbg: int
    ned: int
    kind: int
    ec: int
    fMD: float
    fML: float
    dBotElevat: float
    isBGAbs: int
    ngrid: int
    iHinge: int
class Mdl_jc_app_Pile:
    ID: int
    x: float
    y: float
    z: int
    kind: int
    ang: float
    NIK: int
    fKn: int
    fKm: int
    fALFQ: int
    DaisFlag: int
    idaispilelen: float
    lNewFlag: int
    idUp: int
    pile_peijin_para: str
    Fumozupara: str
class Mdl_jc_app_TJ:
    ID: int
    nbg: int
    ned: int
    kind: int
    ec: int
    ngrid: int
    nMarkCho: int
    dBotElevat: float
    isBGAbs: int
    padd: int
    fk: float
    amb: float
    amd: float
    lNewFlag: int
    fk_dd: float
    HSoil_dd: float
    fk_Euro: float
class Mdl_jc_app_wall:
    ID: int
    nbg: int
    ned: int
    kind: int
    ec: int
    ez: int
    ngrid: int
    hgh: float
    ndist_bg: float
    nlen_hole: float
    nStyle: int
    baseZ: float
    starth: int
    endh: int
    levelh: int
    ndist_ez: int
    nhei_hole: int
class Mdl_jc_app_WaterPipe:
    ID: int
    kind: int
    nRaftID: int
    npt: int
    ptx: str
    pty: str
class Mdl_jc_app_WaterPit:
    ID: int
    kind: int
    nRaftID: int
    ang: float
    cenx: float
    ceny: float
    npt: int
    ptx: str
    pty: str
class Mdl_jc_axis:
    ID: int
    j1: int
    j2: int
    ik: int
    id_old: int
    cname: int
    nCeng: str
    newName: str
    newCeng: int
class Mdl_jc_CalPara:
    ID: int
    strName: str
    strValue: str
    strSecName: str
class Mdl_jc_dais_Cir:
    ID: int
    DaisFlag: int
    D: float
class Mdl_jc_dais_pt:
    ID: int
    DaisFlag: int
    nstep: int
    x: float
    y: float
    z: int
class Mdl_jc_dais_stepH:
    ID: int
    DaisFlag: int
    nstep: int
    H: int
class Mdl_jc_DEF_brace:
    ID: int
    k: int
    b: int
    h: int
    u: int
    t: int
    d: int
    f: int
    l: int
    m: int
    p: int
    name: str
    igzz: int
    b1: int
    lID: int
    Poly: str
    bb: int
    hh: int
class Mdl_jc_DEF_column:
    ID: int
    k: int
    b: int
    h: int
    u: int
    t: int
    d: int
    f: int
    l: int
    m: int
    p: int
    name: str
    igzz: int
    b1: int
    lID: int
    Poly: str
    bb: int
    hh: int
class Mdl_jc_DEF_dais:
    ID: int
    ns: int
    means: int
    nstep: int
    npile: int
    DaisFlag: int
    ecx: int
    ecy: int
    lID: int
    lNewFlag: int
    lIsUsed: int
class Mdl_jc_DEF_DJ:
    ID: int
    kind: int
    n: int
    ak: int
    padthick: int
    cupdist: int
    asx: int
    asy: int
    ecx: int
    ecy: int
    s0: int
    s1: int
    s2: int
    s3: int
    s4: int
    b0: int
    b1: int
    b2: int
    b3: int
    b4: int
    h0: int
    h1: int
    h2: int
    h3: int
    h4: int
    lID: int
    lNewFlag: int
    lIsUsed: int
    lBeamB1: int
    lBeamB2: int
    lBeamH1: int
    lBeamH2: int
    lBeamNums: int
    lDis1: int
    lDis2: int
    lBeamBearing: int
class Mdl_jc_DEF_Elevator:
    ID: int
    lID: int
    shape: int
    rectL: int
    rectB: int
    depth: int
    botThick: int
    nEdge: int
    horzDist_vec: str
    vertDist_vec: str
    slope_vec: str
    equalSize: int
class Mdl_jc_DEF_fbeam:
    ID: int
    b: int
    h: int
    bb: int
    h1: int
    h2: int
    ec: int
    lID: int
    idUp: int
class Mdl_jc_DEF_fwall:
    ID: int
    lW: int
    lID: int
class Mdl_jc_DEF_LL:
    ID: int
    B: int
    H: int
    zj: int
    gj: int
    lID: int
class Mdl_jc_DEF_Pile:
    ID: int
    B: int
    H: int
    F1: float
    means: int
    topd: int
    w: int
    r2: int
    toph_u: int
    toph_m: int
    toph_b: int
    name: int
    lID: int
    F0: float
    F2: float
    idUp: int
    weight: float
    blade_D: int
    blade_dis: int
class Mdl_jc_DEF_RaftY:
    ID: int
    B: int
    H: int
    lID: int
class Mdl_jc_DEF_TJ:
    ID: int
    kind: int
    b: int
    h: int
    area: int
    length: int
    b1: int
    h1: int
    WLb: int
    WLh: int
    ec: int
    zj: int
    BTop4: int
    tana01: int
    gj: int
    zj_l: int
    gj_l: int
    HAll: int
    BTop6: int
    HEndL: int
    HEndR: int
    bw1: int
    bw2: int
    wSpace: int
    lID: int
    lNewFlag: int
    lIsUsed: int
    lArea_b: int
class Mdl_jc_DEF_wall:
    ID: int
    lW: int
    lID: int
    k: int
    m: int
class Mdl_jc_DEF_WaterPipe:
    ID: int
    lID: int
    shape: int
    rectB: int
    rectH: int
    arcH: float
class Mdl_jc_DEF_WaterPit:
    ID: int
    lID: int
    shape: int
    rectL: int
    rectB: int
    depth: int
    botThick: int
    nEdge: int
    horzDist_vec: str
    vertDist_vec: str
    slope_vec: str
    equalSize: int
class Mdl_jc_DEF_ZD:
    ID: int
    x: int
    y: int
    h: int
    h1: int
    lID: int
    kind: int
    idUp: int
    ex: int
    ey: int
    disL: float
    disR: float
    disU: float
    disD: float
class Mdl_jc_HouJiaoDai:
    ID: int
    xx: float
    yy: float
    ww: int
    lID: int
    nn: int
class Mdl_jc_Loads:
    ID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    lFlag: int
    strTN: str
    lIndex: int
    lCustom: int
class Mdl_jc_LoadsFuJia_Line:
    ID: int
    lID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    mark0: int
    jcAdd: int
class Mdl_jc_LoadsFuJia_Point:
    ID: int
    lID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    mark0: int
class Mdl_jc_LoadsLine:
    ID: int
    lID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    lFlag: int
    jcAdd: int
    lCustom: int
class Mdl_jc_Loads_diaoche:
    ID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    lFlag: int
    strTN: str
    lIndex: int
class Mdl_jc_Loads_line_diaoche:
    ID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    lFlag: int
    strTN: str
    lIndex: int
class Mdl_jc_Loads_ZiDingYi_Line:
    ID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    data10: float
    data11: float
    data12: float
    data13: float
    data14: float
    data15: float
    data16: float
    data17: float
    data18: float
    data19: float
    lFlag: int
    strTN: str
    lIndex: int
    data_Array: str
class Mdl_jc_Loads_ZiDingYi_Point:
    ID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    data10: float
    data11: float
    data12: float
    data13: float
    data14: float
    data15: float
    data16: float
    data17: float
    data18: float
    data19: float
    lFlag: int
    strTN: str
    lIndex: int
    data_Array: str
class Mdl_jc_LoadV2_Arc_Show:
    ID: int
    LdCaseID: int
    lID: int
    nbg: int
    ned: int
    cenx: float
    ceny: float
    rad: float
    bga: float
    eda: float
    fN: float
    fMx: float
    fMy: float
    fQx: float
    fQy: float
    nDwFlag: int
class Mdl_jc_LoadV2_Line_Cal:
    ID: int
    LdCaseID: int
    lID: int
    fN: float
    fMx: float
    fMy: float
    fQx: float
    fQy: float
    nDwFlag: int
    jcAdd: int
    lCustom: int
class Mdl_jc_LoadV2_Line_Show:
    ID: int
    LdCaseID: int
    lID: int
    nbg: int
    ned: int
    bgx: float
    bgy: float
    edx: float
    edy: float
    fN: float
    fMx: float
    fMy: float
    fQx: float
    fQy: float
    nDwFlag: int
class Mdl_jc_LoadV2_LoadCase:
    ID: int
    nIndex: int
    nID: int
    nLDKind: int
    nLDCaseID: int
    nLDCaseOld: int
    nXFC: int
    strName: str
    nDwFlag: int
    nFeaLcID: int
class Mdl_jc_LoadV2_Point:
    ID: int
    LdCaseID: int
    NodeID: int
    fN: float
    fMx: float
    fMy: float
    fQx: float
    fQy: float
    nDwFlag: int
    lCustom: int
class Mdl_jc_LoadZhuHe:
    ID: int
    XiShu_1_0: float
    XiShu_1_1: float
    XiShu_1_2: float
    XiShu_1_3: float
    XiShu_1_4: float
    XiShu_1_5: float
    XiShu_1_6: float
    XiShu_1_7: float
    XiShu_1_8: float
    XiShu_1_9: float
    XiShu_1_10: float
    XiShu_1_11: float
    XiShu_1_12: float
    XiShu_1_13: float
    XiShu_1_14: float
    XiShu_1_15: float
    XiShu_1_16: float
    XiShu_1_17: float
    XiShu_1_18: float
    XiShu_1_19: float
    XiShu_1_20: float
    XiShu_1_21: float
    XiShu_1_22: float
    XiShu_1_23: float
    XiShu_1_24: float
    XiShu_1_25: float
    XiShu_1_26: float
    XiShu_1_27: float
    XiShu_1_28: float
    XiShu_1_29: float
    XiShu_1_30: float
    XiShu_1_31: float
    XiShu_1_32: float
    XiShu_1_33: float
    XiShu_1_34: float
    XiShu_1_35: float
    XiShu_1_36: float
    XiShu_1_37: float
    XiShu_2_0: float
    XiShu_2_1: float
    XiShu_2_2: float
    XiShu_2_3: float
    XiShu_2_4: float
    XiShu_2_5: float
    XiShu_2_6: float
    XiShu_2_7: float
    XiShu_2_8: float
    XiShu_2_9: float
    XiShu_2_10: float
    XiShu_2_11: float
    XiShu_2_12: float
    XiShu_2_13: float
    XiShu_2_14: float
    XiShu_2_15: float
    XiShu_2_16: float
    XiShu_2_17: float
    XiShu_2_18: float
    XiShu_2_19: float
    XiShu_2_20: float
    XiShu_2_21: float
    XiShu_2_22: float
    XiShu_2_23: float
    XiShu_2_24: float
    XiShu_2_25: float
    XiShu_2_26: float
    XiShu_2_27: float
    XiShu_2_28: float
    XiShu_2_29: float
    XiShu_2_30: float
    XiShu_2_31: float
    XiShu_2_32: float
    XiShu_2_33: float
    XiShu_2_34: float
    XiShu_2_35: float
    XiShu_2_36: float
    XiShu_2_37: float
    nFuHao0: int
    nFuHao1: int
    nFuHao2: int
    nFuHao3: int
    nFuHao4: int
    nFuHao5: int
    nFuHao6: int
    nFuHao7: int
    nFuHao8: int
    nFuHao9: int
    nFuHao10: int
    nFuHao11: int
    nFuHao12: int
    nFuHao13: int
    nFuHao14: int
    nFuHao15: int
    nFuHao16: int
    nFuHao17: int
    nFuHao18: int
    nFuHao19: int
    nFuHao20: int
    nFuHao21: int
    nFuHao22: int
    nFuHao23: int
    nFuHao24: int
    nFuHao25: int
    nFuHao26: int
    nFuHao27: int
    nFuHao28: int
    nFuHao29: int
    nFuHao30: int
    nFuHao31: int
    nFuHao32: int
    nFuHao33: int
    nFuHao34: int
    nFuHao35: int
    nFuHao36: int
    nFuHao37: int
    nType: int
    nEarthQuk: int
    nWaterGK: int
    strName: str
    dWaterXS: float
    nLinearity: int
    Mark_PM_SATE: int
    nDefault: int
    XiShu_1_Array: str
    XiShu_2_Array: str
    nFuHao_Array: str
    nProperties: int
class Mdl_jc_LoadZH_real:
    ID: int
    LoadIndex: int
    LoadCoef: float
    LoadName: str
class Mdl_jc_LoadZH_Float:
    ID: int
    LoadIndex: int
    LoadCoef: float
    LoadName: str
class Mdl_jc_Load_Arc:
    ID: int
    nbg: int
    ned: int
    cenx: float
    ceny: float
    rad: float
    bga: float
    eda: float
    lID: int
    fM_0: float
    fM_1: float
    fM_2: float
    fM_3: float
    fM_4: float
    fM_5: float
    fM_6: float
    fM_7: float
    fM_8: float
    fM_9: float
    fN_0: float
    fN_1: float
    fN_2: float
    fN_3: float
    fN_4: float
    fN_5: float
    fN_6: float
    fN_7: float
    fN_8: float
    fN_9: float
    fMy_0: float
    fMy_1: float
    fMy_2: float
    fMy_3: float
    fMy_4: float
    fMy_5: float
    fMy_6: float
    fMy_7: float
    fMy_8: float
    fMy_9: float
class Mdl_jc_load_Chose:
    ID: int
    nMark_Load_Chose: int
class Mdl_jc_Load_Line:
    ID: int
    nbg: int
    ned: int
    bgx: float
    bgy: float
    edx: float
    edy: float
    lID: int
    fM_0: float
    fM_1: float
    fM_2: float
    fM_3: float
    fM_4: float
    fM_5: float
    fM_6: float
    fM_7: float
    fM_8: float
    fM_9: float
    fN_0: float
    fN_1: float
    fN_2: float
    fN_3: float
    fN_4: float
    fN_5: float
    fN_6: float
    fN_7: float
    fN_8: float
    fN_9: float
    fMy_0: float
    fMy_1: float
    fMy_2: float
    fMy_3: float
    fMy_4: float
    fMy_5: float
    fMy_6: float
    fMy_7: float
    fMy_8: float
    fMy_9: float
class Mdl_jc_Load_ZiDingYi_Arc:
    ID: int
    nbg: int
    ned: int
    cenx: float
    ceny: float
    rad: float
    bga: float
    eda: float
    lID: int
    data0: float
    data1: float
    data2: float
    data3: float
    data4: float
    data5: float
    data6: float
    data7: float
    data8: float
    data9: float
    data10: float
    data11: float
    data12: float
    data13: float
    data14: float
    data15: float
    data16: float
    data17: float
    data18: float
    data19: float
    data_Array: str
class Mdl_jc_load_ZiDingYi_Line:
    ID: int
    nbg: int
    ned: int
    bgx: float
    bgy: float
    edx: float
    edy: float
    lID: int
    data0: int
    data1: int
    data2: int
    data3: int
    data4: int
    data5: int
    data6: int
    data7: int
    data8: int
    data9: int
    data10: int
    data11: int
    data12: int
    data13: int
    data14: int
    data15: int
    data16: int
    data17: int
    data18: int
    data19: int
    data_Array: str
class Mdl_jc_ParaNums:
    ID: int
    Nums_LoadZhuHe: int
    Nums_Points_All: int
    Nums_Grid_Line: int
    Nums_Grid_Arc: int
    njan: int
    naxis: int
    Nums_Col: int
    Nums_Col_Sec: int
    Nums_Wall_UP: int
    Nums_Wall_Sec: int
    Nums_Load_Line: int
    Nums_Load_Arc: int
    Mark_Soil_Use: int
    Mark_Water_Use: int
    Nums_ZiDingYi_Dead: int
    Nums_ZiDingYi_Live: int
    cMark_Dead: str
    cMark_Live: str
    Mark_Soil_Have: int
    Mark_Water_Have: int
    Str_ZiDingYi_Dead: str
    Str_ZiDingYi_Live: str
    cc: int
    ccc: int
class Mdl_jc_Points_Load:
    ID: int
    lNJ: int
    lIndex: int
    Ang: float
    fLiveLoad_Blp: float
class Mdl_jc_RaftCornerPoint:
    ID: int
    RaftID: int
    ec1: int
    ec2: int
    ptx: float
    pty: float
    rad: int
    cx: int
    cy: int
class Mdl_jc_RaftSlab:
    ID: int
    nCeng: int
    lID: int
    nMainRaftId: int
    b_h: float
    thick: float
    BotElevat: float
    nDire: int
    padd: float
    padd_os: float
    FLD: float
    FLL: float
    RfGrade: int
    RfLoad: float
    bRfPara: int
    RebarAngle: float
    EndH: float
    isBGAbs: int
    fk: float
    amb: float
    amd: float
    InewFlag: int
    lOutB: int
    lBotH: int
    baseZ: int
    idUp: int
    SoilK: float
    DJCL_Kexi: float
    DJCL_Thick: float
    fk_Euro: float
class Mdl_jc_RaftYInfo:
    ID: int
    x1: float
    y1: float
    z1: float
    x2: float
    y2: float
    z2: float
    B: float
    H: float
    lDir: int
    dOffsetL: float
class Mdl_jc_ZiDingYi_Name:
    ID: int
    nType: int
    cName: str
class Mdl_jc_ChildRaft:
    ID: int
    dFLD: float
    dFLL: float
    dRigidity: float
    padd: float
    X: str
    Y: str
    dCX: float
    dCY: float
    vecCustomLoad: str
    listGrid: str
    vecData: str
    nIndexPoolRoom: int
class Mdl_JcResultData_Py:
    m_jcResultAntifloatRaft: list
    m_jcResultGeoFeaElem: list
    m_jcResultGeoFeaPoint: list
    m_jcResultGeoGrid: list
    m_jcResultGeoNode: list
    m_jcResultGeoRoom: list
    m_jcResultInforceCT: list
    m_jcResultInforceCTBeam: list
    m_jcResultInforceDJ: list
    m_jcResultInforceFBeam: list
    m_jcResultInforceFeaElem: list
    m_jcResultInforceLL: list
    m_jcResultLoadCase: list
    m_jcResultLoadComb: list
    m_jcResultLocalcompressCT: list
    m_jcResultLocalcompressDJ: list
    m_jcResultLocalcompressFBeam: list
    m_jcResultLocalcompressRaft: list
    m_jcResultPunchCT: list
    m_jcResultPunchDJ: list
    m_jcResultPunchRaft: list
    m_jcResultReactionDJ: list
    m_jcResultReactionFBeam: list
    m_jcResultReactionFeaElem: list
    m_jcResultReactionPile: list
    m_jcResultReactionRaft: list
    m_jcResultReinCT: list
    m_jcResultReinCTBeam: list
    m_jcResultReinCTTri: list
    m_jcResultReinDJ: list
    m_jcResultReinFBeam: list
    m_jcResultReinLL: list
    m_jcResultSettleCT: list
    m_jcResultSettleDJ: list
    m_jcResultSettleFBeam: list
    m_jcResultSettleFeaElem: list
    m_jcResultSettlePile: list
    m_jcResultSettleRaft: list
    m_jcResultSettleTotalCT: list
    m_jcResultSettleTotalDJ: list
    m_jcResultSettleTotalFBeam: list
    m_jcResultSettleTotalPile: list
    m_jcResultSettleTotalRaft: list
    m_jcResultShearCT: list
    m_jcResultShearCTBeam: list
    m_jcResultShearDJ: list
    m_jcResultSoilcapDJ: list
    m_jcResultSoilcapFBeam: list
    m_jcResultSoilcapFeaElem: list
    m_jcResultSoilcapPile: list
    m_jcResultSoilcapRaft: list
    m_jcResultTotalloadCT: list
    m_jcResultTotalloadDJ: list
    m_jcResultTotalloadRaft: list
    m_jcResultVer: list
class Mdl_JcResultData:
    m_jcResultAntifloatRaftList: list[Mdl_jcResult_antifloat_Raft]
    m_jcResultGeoFeaElemList: list[Mdl_jcResult_geo_FeaElem]
    m_jcResultGeoFeaPointList: list[Mdl_jcResult_geo_FeaPoint]
    m_jcResultGeoGridList: list[Mdl_jcResult_geo_Grid]
    m_jcResultGeoNodeList: list[Mdl_jcResult_geo_Node]
    m_jcResultGeoRoomList: list[Mdl_jcResult_geo_Room]
    m_jcResultInforceCTList: list[Mdl_jcResult_inforce_CT]
    m_jcResultInforceCTBeamList: list[Mdl_jcResult_inforce_CTBeam]
    m_jcResultInforceDJList: list[Mdl_jcResult_inforce_DJ]
    m_jcResultInforceFBeamList: list[Mdl_jcResult_inforce_FBeam]
    m_jcResultInforceFeaElemList: list[Mdl_jcResult_inforce_FeaElem]
    m_jcResultInforceLLList: list[Mdl_jcResult_inforce_LL]
    m_jcResultLoadCaseList: list[Mdl_jcResult_load_Case]
    m_jcResultLoadCombList: list[Mdl_jcResult_load_Comb]
    m_jcResultLocalcompressCTList: list[Mdl_jcResult_localcompress_CT]
    m_jcResultLocalcompressDJList: list[Mdl_jcResult_localcompress_DJ]
    m_jcResultLocalcompressFBeamList: list[Mdl_jcResult_localcompress_FBeam]
    m_jcResultLocalcompressRaftList: list[Mdl_jcResult_localcompress_Raft]
    m_jcResultPunchCTList: list[Mdl_jcResult_punch_CT]
    m_jcResultPunchDJList: list[Mdl_jcResult_punch_DJ]
    m_jcResultPunchRaftList: list[Mdl_jcResult_punch_Raft]
    m_jcResultReactionDJList: list[Mdl_jcResult_reaction_DJ]
    m_jcResultReactionFBeamList: list[Mdl_jcResult_reaction_FBeam]
    m_jcResultReactionFeaElemList: list[Mdl_jcResult_reaction_FeaElem]
    m_jcResultReactionPileList: list[Mdl_jcResult_reaction_Pile]
    m_jcResultReactionRaftList: list[Mdl_jcResult_reaction_Raft]
    m_jcResultReinCTList: list[Mdl_jcResult_rein_CT]
    m_jcResultReinCTBeamList: list[Mdl_jcResult_rein_CTBeam]
    m_jcResultReinCTTriList: list[Mdl_jcResult_rein_CT_Tri]
    m_jcResultReinDJList: list[Mdl_jcResult_rein_DJ]
    m_jcResultReinFBeamList: list[Mdl_jcResult_rein_FBeam]
    m_jcResultReinLLList: list[Mdl_jcResult_rein_LL]
    m_jcResultSettleCTList: list[Mdl_jcResult_settle_CT]
    m_jcResultSettleDJList: list[Mdl_jcResult_settle_DJ]
    m_jcResultSettleFBeamList: list[Mdl_jcResult_settle_FBeam]
    m_jcResultSettleFeaElemList: list[Mdl_jcResult_settle_FeaElem]
    m_jcResultSettlePileList: list[Mdl_jcResult_settle_Pile]
    m_jcResultSettleRaftList: list[Mdl_jcResult_settle_Raft]
    m_jcResultSettleTotalCTList: list[Mdl_jcResult_settle_total_CT]
    m_jcResultSettleTotalDJList: list[Mdl_jcResult_settle_total_DJ]
    m_jcResultSettleTotalFBeamList: list[Mdl_jcResult_settle_total_FBeam]
    m_jcResultSettleTotalPileList: list[Mdl_jcResult_settle_total_Pile]
    m_jcResultSettleTotalRaftList: list[Mdl_jcResult_settle_total_Raft]
    m_jcResultShearCTList: list[Mdl_jcResult_shear_CT]
    m_jcResultShearCTBeamList: list[Mdl_jcResult_shear_CTBeam]
    m_jcResultShearDJList: list[Mdl_jcResult_shear_DJ]
    m_jcResultSoilcapDJList: list[Mdl_jcResult_soilcap_DJ]
    m_jcResultSoilcapFBeamList: list[Mdl_jcResult_soilcap_FBeam]
    m_jcResultSoilcapFeaElemList: list[Mdl_jcResult_soilcap_FeaElem]
    m_jcResultSoilcapPileList: list[Mdl_jcResult_soilcap_Pile]
    m_jcResultSoilcapRaftList: list[Mdl_jcResult_soilcap_Raft]
    m_jcResultTotalloadCTList: list[Mdl_jcResult_totalload_CT]
    m_jcResultTotalloadDJList: list[Mdl_jcResult_totalload_DJ]
    m_jcResultTotalloadRaftList: list[Mdl_jcResult_totalload_Raft]
    m_jcResultVerList: list[Mdl_jcResult_ver]
    def ToPyList(self) -> Mdl_JcResultData_Py: ...
class Mdl_jcResult_antifloat_Raft:
    ID: int
    G: float
    Sigma_Rt: float
    Nwk: float
    Kw: float
class Mdl_jcResult_geo_FeaElem:
    ID: int
    npt_0: int
    npt_1: int
    npt_2: int
    npt_3: int
    nRaft_CT_DJ: int
class Mdl_jcResult_geo_FeaPoint:
    ID: int
    ptx: float
    pty: float
    ptz: float
class Mdl_jcResult_geo_Grid:
    ID: int
    nbg: int
    ned: int
    ngrid: int
class Mdl_jcResult_geo_Node:
    ID: int
    X: float
    Y: float
    Z: float
class Mdl_jcResult_geo_Room:
    ID: int
    ang: float
    nodes: str
    grids: str
class Mdl_jcResult_inforce_CT:
    ID: int
    Comb: int
    IsFea: int
    Mx_bot: float
    My_bot: float
    Mx_top: float
    My_top: float
class Mdl_jcResult_inforce_CTBeam:
    ID: int
    Comb: int
    M: float
    V: float
class Mdl_jcResult_inforce_DJ:
    ID: int
    Comb: int
    IsFea: int
    Mx_bot: float
    My_bot: float
    Mx_top: float
    My_top: float
class Mdl_jcResult_inforce_FBeam:
    ID: int
    Comb: int
    M_Sec_I: float
    M_Sec_1: float
    M_Sec_2: float
    M_Sec_3: float
    M_Sec_4: float
    M_Sec_5: float
    M_Sec_6: float
    M_Sec_7: float
    M_Sec_J: float
    V_Sec_I: float
    V_Sec_1: float
    V_Sec_2: float
    V_Sec_3: float
    V_Sec_4: float
    V_Sec_5: float
    V_Sec_6: float
    V_Sec_7: float
    V_Sec_J: float
class Mdl_jcResult_inforce_FeaElem:
    ID: int
    Comb: int
    Mx: float
    My: float
    Qx: float
    Qy: float
class Mdl_jcResult_inforce_LL:
    ID: int
    Comb: int
    M_Sec_I: float
    M_Sec_1: float
    M_Sec_2: float
    M_Sec_3: float
    M_Sec_4: float
    M_Sec_5: float
    M_Sec_6: float
    M_Sec_7: float
    M_Sec_J: float
    V_Sec_I: float
    V_Sec_1: float
    V_Sec_2: float
    V_Sec_3: float
    V_Sec_4: float
    V_Sec_5: float
    V_Sec_6: float
    V_Sec_7: float
    V_Sec_J: float
class Mdl_jcResult_load_Case:
    ID: int
    nLDKind: int
    strName: str
class Mdl_jcResult_load_Comb:
    ID: int
    nType: int
    nLinearity: int
    CaseID: int
    Xishu: float
class Mdl_jcResult_localcompress_CT:
    ID: int
    Type: int
    ComponentID: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_localcompress_DJ:
    ID: int
    Type: int
    ComponentID: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_localcompress_FBeam:
    ID: int
    Type: int
    ComponentID: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_localcompress_Raft:
    ID: int
    Type: int
    ComponentID: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_punch_CT:
    ID: int
    Type: int
    ComponentID: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_punch_DJ:
    ID: int
    SecID: int
    Step: int
    Direct: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_punch_Raft:
    ID: int
    Type: int
    ComponentID: int
    Fl: float
    Comb: int
    RS: float
class Mdl_jcResult_reaction_DJ:
    ID: int
    Comb: int
    Comb_type: int
    pkmax: float
    pkmin: float
    pkavg: float
class Mdl_jcResult_reaction_FBeam:
    ID: int
    Comb: int
    Comb_type: int
    pkmax: float
    pkmin: float
    pkavg: float
class Mdl_jcResult_reaction_FeaElem:
    ID: int
    Comb: int
    Comb_type: int
    pk: float
class Mdl_jcResult_reaction_Pile:
    ID: int
    Comb: int
    Comb_type: int
    verti_force: float
    hori_force_x: float
    hori_force_y: float
class Mdl_jcResult_reaction_Raft:
    ID: int
    Comb: int
    Comb_type: int
    pkmax: float
    pkmin: float
    pkavg: float
class Mdl_jcResult_rein_CT:
    ID: int
    Style: int
    Asx_top: float
    Ratiox_top: float
    Mx_top: float
    Asx_bot: float
    Ratiox_bot: float
    Mx_bot: float
    Asy_top: float
    Ratioy_top: float
    My_top: float
    Asy_bot: float
    Ratioy_bot: float
    My_bot: float
class Mdl_jcResult_rein_CTBeam:
    ID: int
    Method: int
    As_bot: float
    Rs_bot: float
    Asv: float
    Rsv: float
    Ash: float
    Rsh: float
    M: float
    V: float
class Mdl_jcResult_rein_CT_Tri:
    ID: int
    Style: int
    As1: float
    Rs1: float
    M1: float
    As2: float
    Rs2: float
    M2: float
class Mdl_jcResult_rein_DJ:
    ID: int
    Style: int
    Asx_top: float
    Ratiox_top: float
    Mx_top: float
    Asx_bot: float
    Ratiox_bot: float
    Mx_bot: float
    Asy_top: float
    Ratioy_top: float
    My_top: float
    Asy_bot: float
    Ratioy_bot: float
    My_bot: float
class Mdl_jcResult_rein_FBeam:
    ID: int
    Type: int
    Asu: list[float]
    Rsu: list[float]
    Mu: list[float]
    Asd: list[float]
    Rsd: list[float]
    Md: list[float]
    Asyy: list[float]
    Rsyy: list[float]
    Myy: list[float]
    Ashyy: list[float]
    Rshyy: list[float]
    Mhyy: list[float]
    Asv: list[float]
    Rsv: list[float]
    Vmax: list[float]
class Mdl_jcResult_rein_LL:
    ID: int
    Asu: list[float]
    Rsu: list[float]
    Mu: list[float]
    Asd: list[float]
    Rsd: list[float]
    Md: list[float]
    Asv: list[float]
    Rsv: list[float]
    Vmax: list[float]
class Mdl_jcResult_settle_CT:
    ID: int
    LayerID: int
    Es: float
    Thick: float
    Sigma: float
    si: float
class Mdl_jcResult_settle_DJ:
    ID: int
    LayerID: int
    Es: float
    Thick: float
    Sigma: float
    si: float
class Mdl_jcResult_settle_FBeam:
    ID: int
    LayerID: int
    Es: float
    Thick: float
    Sigma: float
    si: float
class Mdl_jcResult_settle_FeaElem:
    ID: int
    LayerID: int
    Es: float
    Thick: float
    Sigma: float
    si: float
class Mdl_jcResult_settle_Pile:
    ID: int
    LayerID: int
    Es: float
    Thick: float
    Sigma: float
    si: float
class Mdl_jcResult_settle_Raft:
    ID: int
    LayerID: int
    Es: float
    Thick: float
    Sigma: float
    si: float
class Mdl_jcResult_settle_total_CT:
    ID: int
    TotalLoad: float
    Area: float
    Pc: float
    P0: float
    fi: float
    fi_e: float
    ss: float
    s_final: float
class Mdl_jcResult_settle_total_DJ:
    ID: int
    TotalLoad: float
    Area: float
    Pc: float
    P0: float
    fi: float
    ss: float
    s_final: float
class Mdl_jcResult_settle_total_FBeam:
    ID: int
    SoilR: float
    Pc: float
    P0: float
    fi: float
    ss: float
    s_final: float
class Mdl_jcResult_settle_total_Pile:
    ID: int
    Qj: float
    kxi_e: float
    se: float
    fi: float
    ss: float
    s_final: float
class Mdl_jcResult_settle_total_Raft:
    ID: int
    TotalLoad: float
    Area: float
    Pc: float
    P0: float
    fi: float
    ss: float
    s_final: float
class Mdl_jcResult_shear_CT:
    ID: int
    SecID: int
    Type: int
    Angle: float
    Vs: float
    Comb: int
    RS: float
class Mdl_jcResult_shear_CTBeam:
    ID: int
    SecID: int
    Method: int
    Angle: float
    bVmax: int
    Vs: float
    Comb: int
    RS: float
class Mdl_jcResult_shear_DJ:
    ID: int
    SecID: int
    Step: int
    Direct: int
    IsNeed: int
    Vs: float
    Comb: int
    RS: float
class Mdl_jcResult_soilcap_DJ:
    ID: int
    fa: float
    faE: float
    faW: float
class Mdl_jcResult_soilcap_FBeam:
    ID: int
    fa: float
    faE: float
    faW: float
class Mdl_jcResult_soilcap_FeaElem:
    ID: int
    fa: float
    faE: float
    faW: float
class Mdl_jcResult_soilcap_Pile:
    ID: int
    Ra: float
    Rh: float
    Rt: float
class Mdl_jcResult_soilcap_Raft:
    ID: int
    fa: float
    faE: float
    faW: float
class Mdl_jcResult_totalload_CT:
    ID: int
    LoadCase: int
    N: float
    Mx: float
    My: float
    Qx: float
    Qy: float
class Mdl_jcResult_totalload_DJ:
    ID: int
    LoadCase: int
    N: float
    Mx: float
    My: float
    Qx: float
    Qy: float
class Mdl_jcResult_totalload_Raft:
    ID: int
    LoadCase: int
    N: float
    Mx: float
    My: float
    Qx: float
    Qy: float
class Mdl_jcResult_ver:
    ID: int
    version: str
class ENUM_DBMDL:
    TABLE_STDFLR = 0
    TABLE_STDFLRPARA = 1
    TABLE_FLOOR = 2
    TABLE_AXIS = 3
    TABLE_GRID = 4
    TABLE_JOINT = 5
    TABLE_WALLSECT = 6
    TABLE_WALLSEG = 7
    TABLE_WALLHOLEDEF = 8
    TABLE_WALLHOLE = 9
    TABLE_BEAMSECT = 10
    TABLE_BEAMSEG = 11
    TABLE_SUBBEAM = 12
    TABLE_SLAB = 13
    TABLE_SLABHOLEDEF = 14
    TABLE_SLABHOLE = 15
    TABLE_CANTISLABDEF = 16
    TABLE_CANTISLAB = 17
    TABLE_COLSECT = 18
    TABLE_COLSEG = 19
    TABLE_BRACESECT = 20
    TABLE_BRACESEG = 21
    TABLE_STAIRDEF = 22
    TABLE_STAIRSEG = 23
    TABLE_LOADSECT = 24
    TABLE_LOADSEG = 25
    TABLE_PROJECTPARA = 26
    TABLE_PROPERTY = 27
    TABLE_GROUP = 28
    TABLE_GKLOADDEF = 29
    TABLE_BEAMHOLESECT = 30
    TABLE_BEAMHOLESEG = 31
    TABLE_COLCAPSECT = 32
    TABLE_SKINLOADSECT = 33
    TABLE_SKINSEG = 34
    TABLE_CRANE = 35
    TABLE_CRANEDEF = 36
    TABLE_CRANELOAD = 37
    TABLE_BEAMJGSECT = 38
    TABLE_COLJGSECT = 39
    TABLE_JGSEG = 40
    TABLE_SUM = 41

class GjKind:
    IDK_LAYE = 0
    IDK_WALL = 1
    IDK_PLAT = 2
    IDK_PL3D = 3
    IDK_GLAS = 4
    IDK_COLM = 11
    IDK_BEAM = 12
    IDK_CL3D = 13
    IDK_CILG = 14
    IDK_QULI = 15
    IDK_WNDR = 21
    IDK_HOLE = 22
    IDK_BEAMHOLE = 23
    IDK_STAI = 41
    IDK_STLSTAI = 42
    IDK_PLAO = 62
    IDK_YUZB = 64
    IDK_SLAB = 65
    IDK_HOLLOWSLAB = 66
    IDK_COLCAP = 67
    IDK_LOAD = 71
    IDK_XNQ = 72
    IDK_GLOBALDATA = 80
    IDK_CRANE = 81
    IDK_SKIN = 82
    IDK_LOADSELF = 83
    IDK_SKINLOAD = 84
    IDK_SKINTEXT = 85
    IDK_MATHERIALSELF = 86
    IDK_PETRODEVICE = 87
    IDK_COLUMNJG = 88
    IDK_BEAMJG = 89
    IDK_JG = 90
    IDK_YZGJ = 91
    IDK_SLABJY = 92
    IDK_PRECASTSLAB = 93
    IDK_PROFILINGSTEELSLAB = 94
    IDK_MIDSLAB = 95
    IDK_YMJ = 96
    IDK_PRECASTDTSLAB = 97
    IDK_PRESTRESS = 98
    IDK_WALLYMJ = 99
    IDK_GROUP = 100
    IDK_WALLDEF = 101
    IDK_COLMDEF = 102
    IDK_BEAMDEF = 103
    IDK_CL3DDEF = 104
    IDK_STEELJG = 902
    IDK_AXIS3D = -6
    IDK_ZRC = -5
    IDK_BZC = -4
    IDK_AXIS = -3
    IDK_GRID = -2
    IDK_NODE = -1

class Hi_DbModelData_Py:
    m_StdFlr: list
    m_StdFlrPara: list
    m_Floor: list
    m_Axis: list
    m_Grid: list
    m_Group: list
    m_Joint: list
    m_WallSect: list
    m_WallSeg: list
    m_WallHoleDef: list
    m_WallHole: list
    m_BeamSect: list
    m_BeamHoleSect: list
    m_BeamSeg: list
    m_BeamHoleSeg: list
    m_SubBeam: list
    m_Slab: list
    m_MidSlab: list
    m_SlabJYDef: list
    m_SlabHoleDef: list
    m_SlabHole: list
    m_CantiSlabDef: list
    m_CantiSlab: list
    m_ColSect: list
    m_ColSeg: list
    m_ColCapSect: list
    m_BeamJYSect: list
    m_BeamJYSeg: list
    m_ColCapSeg: list
    m_BraceSect: list
    m_BraceSeg: list
    m_StairDef: list
    m_Stair40: list
    m_StairSeg: list
    m_LoadSect: list
    m_LoadSeg: list
    m_ProjectPara: list
    m_Property: list
    m_GKLoadDef: list
    m_SkinLoadSect: list
    m_SkinSeg: list
    m_Crane: list
    m_CraneDef: list
    m_BeamJGSect: list
    m_ColJGSect: list
    m_SteelJGSect: list
    m_JGSeg: list
    m_XNQSeg: list
    m_XNQSegSect: list
    m_FillWallSect: list
    m_FillWallSeg: list
    unionID: int
class Hi_DbModelData:
    m_StdFlr: list[Mdl_StdFlr]
    m_StdFlrPara: list[Mdl_StdFlrPara]
    m_Floor: list[Mdl_Floor]
    m_Axis: list[Mdl_Axis]
    m_Grid: list[Mdl_Grid]
    m_Group: list[Mdl_Group]
    m_Joint: list[Mdl_Joint]
    m_WallSect: list[Mdl_WallSect]
    m_WallSeg: list[Mdl_WallSeg]
    m_WallHoleDef: list[Mdl_WallHoleDef]
    m_WallHole: list[Mdl_WallHole]
    m_BeamSect: list[Mdl_BeamSect]
    m_BeamHoleSect: list[Mdl_BeamHoleSect]
    m_BeamSeg: list[Mdl_BeamSeg]
    m_BeamHoleSeg: list[Mdl_BeamHoleSeg]
    m_SubBeam: list[Mdl_SubBeam]
    m_Slab: list[Mdl_Slab]
    m_MidSlab: list[Mdl_MidSlab]
    m_SlabJYDef: list[Mdl_SlabJYDef]
    m_SlabHoleDef: list[Mdl_SlabHoleDef]
    m_SlabHole: list[Mdl_SlabHole]
    m_CantiSlabDef: list[Mdl_CantiSlabDef]
    m_CantiSlab: list[Mdl_CantiSlab]
    m_ColSect: list[Mdl_ColSect]
    m_ColSeg: list[Mdl_ColSeg]
    m_ColCapSect: list[Mdl_ColCapSect]
    m_BeamJYSect: list[Mdl_BeamJY]
    m_BeamJYSeg: list[Mdl_BeamYSeg]
    m_ColCapSeg: list[Mdl_ColcapSeg]
    m_BraceSect: list[Mdl_BraceSect]
    m_BraceSeg: list[Mdl_BraceSeg]
    m_StairDef: list[Mdl_StairDef]
    m_Stair40: list[Mdl_StairSeg40]
    m_StairSeg: list[Mdl_StairSeg]
    m_LoadSect: list[Mdl_LoadSect]
    m_LoadSeg: list[Mdl_LoadSeg]
    m_ProjectPara: list[Mdl_ProjectPara]
    m_Property: list[Mdl_Property]
    m_GKLoadDef: list[Mdl_GKLoadDef]
    m_SkinLoadSect: list[Mdl_SkinLoadSect]
    m_SkinSeg: list[Mdl_SkinSeg]
    m_Crane: list[Mdl_Crane]
    m_CraneDef: list[Mdl_CraneDef]
    m_BeamJGSect: list[Mdl_BeamJGSect]
    m_ColJGSect: list[Mdl_ColJGSect]
    m_SteelJGSect: list[Mdl_SteelJGSect]
    m_JGSeg: list[Mdl_JGSeg]
    m_XNQSeg: list[Mdl_XNQSeg]
    m_XNQSegSect: list[Mdl_XNQSect]
    m_FillWallSect: list[Mdl_FillWallDef]
    m_FillWallSeg: list[Mdl_FillWall]
    unionID: int
    def ToPyList(self) -> Hi_DbModelData_Py: ...
    def ConvertCSharpListToPythonList(self, csharpList: Any) -> list: ...
class Hi_UpdateInfo:
    DeleteIdList: list[int]
    DeletePropertyIdList: list[Mdl_Property]
    AddIdSet: None[int]
    AddIdSet_Property: None[int]
    AddIdSet_Grp: None[str]
    ModifyIdSet: None[int]
    ModifyIdSet_Property: None[int]
    m_gjlist: list[Any]
    unionID: int
    def Clear(self) -> None: ...
    def AddObj(self, obj: Any) -> None: ...
    def AddGrpObj(self, obj: Any) -> None: ...
    def ModifyObj(self, obj: Any) -> None: ...
    def DeleteObj(self, obj: Any) -> None: ...
    def DeleteProerty(self, property: Mdl_Property) -> None: ...
class Mdl_StdFlr:
    ID: int
    No: int
    Height: int
    Name: str
    Para: str
    LiveLoad: float
    DeadLoad: float
class Mdl_StdFlrPara:
    nStdFlrID: int
    nKind: int
    dParas: float
class Mdl_Floor:
    ID: int
    No: int
    Name: str
    StdFlrID: int
    LevelB: int
    Height: int
class Mdl_Axis:
    ID: int
    No: int
    StdFlrID: int
    Jt1ID: int
    Jt2ID: int
    Name: str
class Mdl_Grid:
    ID: int
    No: int
    StdFlrID: int
    Jt1ID: int
    Jt2ID: int
    AxisID: int
class Mdl_Group:
    No_: int
    nCnt: int
    nID: list[int]
    Name: str
    idNewZRC: list[int]
class Mdl_Joint:
    ID: int
    No: int
    StdFlrID: int
    X: float
    Y: float
    HDiff: float
class Mdl_WallSect:
    ID: int
    No: int
    Mat: int
    Kind: int
    B: int
    H: int
    T2: int
    Dis: int
    colsect1: str
    colShapeVal1: str
    colsect2: str
    colShapeVal2: str
    Name: str
class Mdl_WallSeg:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    GridID: int
    Ecc: int
    HDiff1: int
    HDiff2: int
    HDiffB: int
    sloping: int
    EccDown: int
    offset1: int
    offset2: int
    HDiffB2: int
class Mdl_WallHoleDef:
    ID: int
    No: int
    B: int
    H: int
    K: int
    Name: str
    OutLT: int
    OutLB: int
    BWT: int
    BWB: int
    HW: int
    LZW: int
    LYW: int
    LZSW: int
    LYSW: int
    HSW: int
    BSW: int
    T1SW: int
    T2SW: int
    HXW: int
    BXW: int
    T1XW: int
    T2XW: int
    Special: str
class Mdl_WallHole:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    GridID: int
    Ecc: float
    HDiff: float
    FillWallId: int
    DR: int
class Mdl_Section:
    ID: int
    No: int
    Name: str
    Mat: int
    Kind: int
    ShapeVal: str
    ShapeVal1: str
class Mdl_BeamSect:
    idNew: int
    StateFlag: int
    b: int
    h: int
    u: int
    t: int
    d: int
    f: int
    l: int
    p: int
    ID: int
    No: int
    Name: str
    Mat: int
    Kind: int
    ShapeVal: str
    ShapeVal1: str
class Mdl_BeamHoleSect:
    ID: int
    No_: int
    B: int
    H: int
    K: int
    Name: str
class Mdl_BraceSect:
    ropekind: int
    ropelevel: int
    ropetxml: int
    b: int
    h: int
    u: int
    t: int
    d: int
    f: int
    l: int
    p: int
    ID: int
    No: int
    Name: str
    Mat: int
    Kind: int
    ShapeVal: str
    ShapeVal1: str
class Mdl_ColSect:
    idNew: int
    StateFlag: int
    b: int
    h: int
    u: int
    t: int
    d: int
    f: int
    l: int
    p: int
    ID: int
    No: int
    Name: str
    Mat: int
    Kind: int
    ShapeVal: str
    ShapeVal1: str
class Mdl_ColCapSect:
    ID: int
    No: int
    Kind: int
    W: int
    L: int
    H: int
    SW: int
    SL: int
    SH: int
    Name: str
class Mdl_BeamSeg:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    GridID: int
    Ecc: int
    HDiff1: int
    HDiff2: int
    Rotation: float
    JYDef: str
    RevitID: int
    Ecc2: int
class Mdl_BeamHoleSeg:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    ElementID: int
    Ec: int
    Ez: int
class Mdl_SubBeam:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    X1: float
    Y1: float
    Z1: float
    X2: float
    Y2: float
    Z2: float
    Grid1ID: int
    Grid2ID: int
class Mdl_Slab:
    ID: int
    No: int
    StdFlrID: int
    GridsID: str
    VertexX: str
    VertexY: str
    VertexZ: str
    RoomIsHole: int
    Thickness: int
    cc: int
    dead: float
    live: float
    TransWay: int
    Ang1: float
    Ang2: float
    nEdge: int
    EdgeSupport: str
    Shape: int
    xc: float
    yc: float
    HollowSlabID: float
    PrecastSlabID: str
    PrecastSlabRebarPara: str
    SingleSeamB: int
    SingleSeamBMax: int
    PairSeamB: int
    PairSeamBMax: int
    TwoWaySlab: int
    PrecastSlabLastL: float
    PrecastSlabRotate: int
    PrecastSlabStyle_PK: int
    PrecastSlabOffsetX: int
    PrecastSlabOffsetY: int
    PrecastSlabX: str
    PrecastSlabY: str
    PrecastSlabIndex: int
    PrecastSlabCount: int
    PrecastSlabArrangeNo: str
    PrecastSlabArrangeWidth: str
    precastSlabSpace: str
    PrecastSlabParaArr: str
    ProfilSlabDefId: int
    ProfilSlabAng: float
    ProfilSlabConcertW: float
    ProfilSlabWorkLoad: float
    ProfilSlabbhou: float
    HollowBoxPtNum: int
    HollowBoxPtX: str
    HollowBoxPtY: str
    HollowBoxPtZ: str
    HollowPtOrig: str
    HollowVX: str
    HollowVY: str
    HollowOhterData: str
    PcSlabStPt: str
    PcSlabEdPt: str
class Mdl_MidSlab:
    numsPt: str
    MidPt: str
    FloorH: int
    ID: int
    No: int
    StdFlrID: int
    GridsID: str
    VertexX: str
    VertexY: str
    VertexZ: str
    RoomIsHole: int
    Thickness: int
    cc: int
    dead: float
    live: float
    TransWay: int
    Ang1: float
    Ang2: float
    nEdge: int
    EdgeSupport: str
    Shape: int
    xc: float
    yc: float
    HollowSlabID: float
    PrecastSlabID: str
    PrecastSlabRebarPara: str
    SingleSeamB: int
    SingleSeamBMax: int
    PairSeamB: int
    PairSeamBMax: int
    TwoWaySlab: int
    PrecastSlabLastL: float
    PrecastSlabRotate: int
    PrecastSlabStyle_PK: int
    PrecastSlabOffsetX: int
    PrecastSlabOffsetY: int
    PrecastSlabX: str
    PrecastSlabY: str
    PrecastSlabIndex: int
    PrecastSlabCount: int
    PrecastSlabArrangeNo: str
    PrecastSlabArrangeWidth: str
    precastSlabSpace: str
    PrecastSlabParaArr: str
    ProfilSlabDefId: int
    ProfilSlabAng: float
    ProfilSlabConcertW: float
    ProfilSlabWorkLoad: float
    ProfilSlabbhou: float
    HollowBoxPtNum: int
    HollowBoxPtX: str
    HollowBoxPtY: str
    HollowBoxPtZ: str
    HollowPtOrig: str
    HollowVX: str
    HollowVY: str
    HollowOhterData: str
    PcSlabStPt: str
    PcSlabEdPt: str
class Mdl_SlabJYDef:
    ID: int
    No: int
    Kind: int
    Para: str
    name: str
class Mdl_SlabHoleDef:
    ID: int
    No: int
    Kind: int
    ShapeVal: str
    name: str
class Mdl_SlabHole:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    JtID: int
    SlabID: int
    EccX: int
    EccY: int
    Rotation: float
class Mdl_CantiSlabDef:
    ID: int
    No: int
    Kind: int
    Length: int
    Width: int
    Thick: int
    nSubKind: int
    Para: str
    name: str
class Mdl_CantiSlab:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    GridID: int
    Thick: int
    ez: int
    ec: int
    dr: int
class Mdl_ColSeg:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    JtID: int
    EccX: int
    EccY: int
    Rotation: float
    HDiffB: int
    ColcapId: int
    Cut_Col: str
    Cut_Cap: str
    Cut_Slab: str
    RevitID: int
class Mdl_ColcapSect:
    HostID: int
    type: int
    ID: int
    No: int
    dW: int
    dH: int
    dSlabH: int
    dSlabW: int
    dSlabL: int
    dlabEW: int
    dSlabEL: int
    dcapH: int
    dcapW: int
    dcapL: int
    BRT: bool
    BRD: bool
    BLT: bool
    BLD: bool
    TRT: bool
    TRD: bool
    TLT: bool
    TLD: bool
class Mdl_ColcapSeg:
    ID: int
    HostID: int
class Mdl_BeamYSeg:
    IntanceID: int
    SymbolID: int
    HostID: int
class Mdl_BeamJY:
    type: int
    ID: int
    No: int
    dL: float
    dH1: float
    dH2: float
    dLL: float
    dLW1: float
    dLW2: float
    dRL: float
    dRW1: float
    dRW2: float
    DownVisiabe: bool
    upVisiabe: bool
    leftVisiabe: bool
    name: str
class Mdl_BraceSeg:
    ID: int
    No: int
    StdFlrID: int
    SectID: int
    Jt1ID: int
    Jt2ID: int
    EccX1: int
    EccY1: int
    HDiff1: int
    EccX2: int
    EccY2: int
    HDiff2: int
    Rotation: float
    Ex: int
    Ey: int
class Mdl_StairDef:
    ID: int
    No: int
    Col2: int
    Col3: int
    Col4: int
    Col5: int
    Col6: int
    Col7: int
    Col8: int
    Col9: int
    Col10: int
    Col11: int
    Col12: int
    Col13: int
    Col14: int
    Col15: int
    Col16: int
    Col17: int
    Col18: int
    Col19: int
    Col20: int
    Col21: int
    Col22: int
    Col23: int
    Col24: int
    Col25: int
    Col26: int
    Col27: int
    Col28: int
    Col29: int
    Col30: int
    Col31: int
    Col32: int
    Col33: int
    Col34: int
    Col35: int
    Col36: int
    Col37: int
    Col38: int
    Col39: int
    Col40: int
    Col41: int
    Col42: int
    Col43: int
    Col44: int
    Col45: int
    Col46: int
    Col47: int
    Col48: int
    Col49: int
    Col50: int
    Col51: int
    Col52: int
    Col53: int
    Col54: int
    Col55: int
    Col56: int
    Col57: int
    Col58: int
    Col59: int
    Col60: int
    Col61: int
    Col62: int
    Col63: int
    Col64: int
    Col65: int
    Col66: int
    Col67: int
    Col68: int
    Col69: int
    Col70: int
    Col71: int
    gangh: int
    TZdef: str
    TLdef: str
    LCLdef: str
    def GetDef(self) -> list[str]: ...
    def GetNData(self) -> list[int]: ...
class Mdl_StairSeg:
    ID: int
    No: int
    StdFlrID: int
    SectionID: int
    SlabID: int
    StartNode: int
    AntiClockwise: int
class Mdl_StairSeg40:
    ID: int
    No: int
    StdFlrID: int
    SectionID: int
    SlabID: int
    StartNode: int
    AntiClockwise: int
    BoxPt1x: float
    BoxPtly: float
    BoxPt1z: float
    BoxPt2x: float
    BoxPt2y: float
    BoxPt2z: float
    BoxPt3x: float
    BoxPt3y: float
    BoxPt3z: float
    BoxPt4x: float
    BoxPt4y: float
    BoxPt4z: float
class Mdl_LoadSect:
    ID: int
    No: int
    ElementKind: int
    ShapeVal: str
    strName: str
class Mdl_LoadSeg:
    ID: int
    No: int
    SectID: int
    Type: int
    ElementID: int
    strParas1: str
    nPtCnt: int
    strParasX: str
    strParasY: str
    strParasZ: str
    stdFlrID: int
class Mdl_ProjectPara:
    ID: int
    ParaVal: str
class Mdl_Property:
    ID: int
    Name: str
    Type: int
    ShapeVal: str
class Mdl_GKLoadDef:
    ID: int
    No_: int
    kind: int
    dDead: float
    nLive: int
    dLive1: float
    dLive2: float
    dLive3: float
    strName: str
    Data: str
    StateFlag: int
class Mdl_SkinLoadSect:
    ID: int
    No: int
    Kind: int
    Style: int
    Val: float
    Direction: int
class Mdl_XNQSect:
    ID: int
    No: int
    Name: str
    Mat: int
    Kind: int
    BrcidDef: int
    d1: int
    L1: int
    H1: int
    H: int
    T: int
    BrcLel: int
    BrcMar: int
    WallLel: int
    WallMar: int
    ShuBrcidDef: int
    CalPara: str
    Quality: float
class Mdl_XNQSeg:
    ID: int
    No: int
    StdFlrId: int
    SectID: int
    idNode1: int
    idNode2: int
    idGrid: int
    nd1: int
    nd2: int
    ntop: int
    nbottom: int
class Mdl_SkinSeg:
    ID: int
    No: int
    StdFlrID: int
    Dead: float
    Live: float
    Thick: int
    TotalStress: float
    MaterialStyle: int
    ConcreteLevel: float
    CustomMaterialID: int
    Direction: str
    vecPtX: str
    vecPtY: str
    vecPtZ: str
    vecNodeID: str
    vecVal: str
    vecLoadID: str
    vecInx: str
    vecNodeIDNew: str
    listLoad: str
    nDirection: str
class Mdl_Crane:
    ID: int
    No: int
    StdFlrID: int
    Jan1: int
    IDX11: int
    IDX12: int
    Jan2: int
    IDX21: int
    IDX22: int
    Ex1: float
    Ex2: float
    Hx: float
    F1: float
    F2: float
    Ez: float
    DchNum: int
    DchNo1: int
    DchNo2: int
class Mdl_CraneDef:
    ID: int
    No: int
    CraneLoadData: str
    Name: str
class Mdl_CraneLoad:
    StdFlrID: int
    Num: int
    CraneLoadData: str
    Name: str
    DchLoadInfo: list[list[float]]
class Mdl_ColJGSect:
    k: int
    ID: int
    No: int
    name: str
class Mdl_ColJG_MagnifySect:
    b_l: int
    b_r: int
    h_t: int
    h_b: int
    hnt: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_ColJG_WrapSteel:
    gangh: int
    b: int
    h: float
    s: int
    pos: int
    _def: _kColumInt
    k: int
    ID: int
    No: int
    name: str
class Mdl_ColJG_Convert:
    b: int
    h: int
    hnt: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_ColJG_StickPlate:
    b: int
    h: int
    t: float
    gangh: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_ColJG_StickFibre:
    _k: int
    kk: int
    bw: int
    hw: int
    cw: int
    cs: int
    n: int
    t: float
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJGSect:
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_MagnifySect:
    b: int
    hb: int
    ht: int
    hnt: int
    steelB: str
    steelT: str
    steelH: str
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_Convert:
    hb: int
    ht: int
    hnt: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_WrapSteel:
    cw: int
    ct: float
    cs: int
    gangh: int
    defb: _kColumInt
    deft: _kColumInt
    bw: int
    bt: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_StickPlate:
    bw: int
    bt: float
    tw: int
    tt: float
    cw: int
    ct: float
    cs: int
    gangh: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_StickFibre:
    _k: int
    kk: int
    bn: int
    bw: int
    tn: int
    tw: int
    cn: int
    cs: int
    cw: int
    t: float
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_ReinForceSteelStrand:
    r: float
    cs: int
    Hrl: int
    Srw: int
    Szj: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_BeamJG_StickPlateAndMagnifySect:
    tw: int
    tt: float
    gangh: int
    b: int
    hb: int
    hnt: int
    k: int
    ID: int
    No: int
    name: str
class Mdl_SteelJGSect:
    ID: int
    No_: int
    idNew: int
    Name: str
    k: int
    SteelLevel: int
    SHFS: float
    HJCC: float
    HDCD: float
    HDJG: float
    B1: float
    B2: float
    T1: float
    T2: float
    SubK: int
    TSecK: int
    IsXY: int
    IsInter: int
    Dmid: int
    SectionSteelName: str
class Mdl_JGSeg:
    ID: int
    No_: int
    StdFlrID: int
    ElementKind: int
    SectID: int
    ElementID: int
class Mdl_FillWall:
    ID: int
    StdFlrID: int
    SectID: int
    x1: float
    y1: float
    dR: float
    x2: float
    y2: float
    Ea: int
    Ez: int
    Ez1: int
    Ez2: int
    GridId: int
    EccDown: int
    Height: int
    Ez3: int
class Mdl_FillWallDef:
    ID: int
    FireProtectClass: int
    Name: str
    RongZhong: int
    FillMainMat: int
    Thick: int
    Height: int
    K: int
    FuncType: int
    KZJ: int
    E: float
    U: float
    tFillWallType: int
class PostGjKind:
    COM_BEAM = 1
    COM_MAINBEAM = 2
    COM_COLUMN = 3
    COM_MAINCOLUMN = 4
    COM_BRACE = 5
    COM_WALLBEAM = 6
    COM_WALLCOLUMN = 7
    COM_WALLASSEMBLY = 8
    COM_EDGEELEMENT = 9
    COM_SUBBEAM = 10
    COM_MAINSUBBEAM = 11
    COM_RIBBEAM = 12
    COM_MAINRIBBEAM = 13
    COM_SLAB = 14
    COM_MAINWALLBEAM = 15
    COM_STAIR = 16
    COM_SLABHOLLOW = 17
    COM_SKIN = 18
    COM_LINK = 19
    COM_ELINK = 20
    COM_PLANAR = 21
    COM_WALLBODY = 22
    COM_GRADEBEAM = 23
    COM_MAINGRADEBEAM = 24
    COM_NODE = 101
    COM_NET = 102
    COM_MESH = 103
    COM_MESH3D = 104

class PostModelKind:
    MODULE_M0 = 1
    MODULE_M0F = 2
    MODULE_MR = 3
    MODULE_MRF = 4
    MODULE_MWR = 5
    MODULE_MWRF = 6
    MODULE_MFS = 7
    MODULE_MRCRP = 8
    MODULE_MRZ = 9
    MODULE_M0CB = 10
    MODULE_MRESB = 11
    MODULE_MRESBV = 12

class PostAnalysisKind:
    ANALYSIS_GENDATA_CAL_DESIGN = 1
    ANALYSIS_CAL_DESIGN = 2
    ANALYSIS_CALONLY = 3
    ANALYSIS_DESIGNONLY = 4

class PostForceKind:
    FORCE_MOMENT = 1
    FORCE_MOMENTX = 2
    FORCE_MOMENTY = 3
    FORCE_MOMENTOTHER = 4
    FORCE_SHEAR = 5
    FORCE_SHEARX = 6
    FORCE_SHEARY = 7
    FORCE_AXIS = 8
    FORCE_TORSION = 9

class PostStressKind:
    STRESS_FXX = 101
    STRESS_FYY = 102
    STRESS_FXY = 103
    STRESS_FMAX = 104
    STRESS_FMIN = 105
    STRESS_MXX = 106
    STRESS_MYY = 107
    STRESS_MXY = 108
    STRESS_MMAX = 109
    STRESS_MMIN = 110
    STRESS_VXZ = 111
    STRESS_VYZ = 112

class PostSigKind:
    SIG_XX = 201
    SIG_YY = 202
    SIG_ZZ = 203
    SIG_XY = 204
    SIG_YZ = 205
    SIG_XZ = 206
    SIG_MAX = 207
    SIG_MIN = 208
    SIG_EFF = 209
    SIG_SHEAR_MAX = 210

class PostLDComb:
    LDCOMB_NULL = 0
    LDCOMB_NORMAL = 1
    LDCOMB_HORSEIS = 2
    LDCOMB_VERSEIS = 3
    LDCOMB_VERSEISONLY = 4
    LDCOMB_AIR = 5

class PostLDCombType:
    LDCOMBTYPE_LDCASE = 1
    LDCOMBTYPE_FUNDATION = 2
    LDCOMBTYPE_NORMINAL = 3
    LDCOMBTYPE_FREQUENT = 4
    LDCOMBTYPE_QUASI = 5
    LDCOMBTYPE_PRC = 10
    LDCOMBTYPE_Construction = 11

class PostDir:
    DIR_X = 1
    DIR_Y = 2

class PostLDKind:
    LDKIND_HORSEISX = 1
    LDKIND_HORSEISXAPPOINT = 2
    LDKIND_HORSEISXP5 = 3
    LDKIND_HORSEISXP5APPOINT = 4
    LDKIND_HORSEISXN5 = 5
    LDKIND_HORSEISXN5APPOINT = 6
    LDKIND_HORSEISXD = 7
    LDKIND_HORSEISXMAX = 8
    LDKIND_HORSEISXFYWYP = 9
    LDKIND_HORSEISXFYWYN = 10
    LDKIND_HORSEISXMS = 11
    LDKIND_HORSEISY = 21
    LDKIND_HORSEISYAPPOINT = 22
    LDKIND_HORSEISYP5 = 23
    LDKIND_HORSEISYP5APPOINT = 24
    LDKIND_HORSEISYN5 = 25
    LDKIND_HORSEISYN5APPOINT = 26
    LDKIND_HORSEISYD = 27
    LDKIND_HORSEISYMAX = 28
    LDKIND_HORSEISYFYWYP = 29
    LDKIND_HORSEISYFYWYN = 30
    LDKIND_HORSEISYMS = 31
    LDKIND_WINDXP = 41
    LDKIND_WINDXPH = 42
    LDKIND_WINDXPT = 43
    LDKIND_WINDXN = 44
    LDKIND_WINDXNH = 45
    LDKIND_WINDXNT = 46
    LDKIND_WINDXPP5 = 47
    LDKIND_WINDXPN5 = 48
    LDKIND_WINDXNP5 = 49
    LDKIND_WINDXNN5 = 50
    LDKIND_WINDYP = 51
    LDKIND_WINDYPH = 52
    LDKIND_WINDYPT = 53
    LDKIND_WINDYN = 54
    LDKIND_WINDYNH = 55
    LDKIND_WINDYNT = 56
    LDKIND_WINDYPP5 = 57
    LDKIND_WINDYPN5 = 58
    LDKIND_WINDYNP5 = 59
    LDKIND_WINDYNN5 = 60
    LDKIND_WINDXPDYP = 61
    LDKIND_WINDXPDYPP5 = 62
    LDKIND_WINDXPDYPN5 = 63
    LDKIND_WINDXNDYP = 64
    LDKIND_WINDXNDYPP5 = 65
    LDKIND_WINDXNDYPN5 = 66
    LDKIND_WINDYPDXN = 67
    LDKIND_WINDYPDXNP5 = 68
    LDKIND_WINDYPDXNN5 = 69
    LDKIND_WINDYNDXN = 70
    LDKIND_WINDYNDXNP5 = 71
    LDKIND_WINDYNDXNN5 = 72
    LDKIND_WINDXPDYN = 73
    LDKIND_WINDXPDYNP5 = 74
    LDKIND_WINDXPDYNN5 = 75
    LDKIND_WINDXNDYN = 76
    LDKIND_WINDXNDYNP5 = 77
    LDKIND_WINDXNDYNN5 = 78
    LDKIND_WINDYPDXP = 79
    LDKIND_WINDYPDXPP5 = 80
    LDKIND_WINDYPDXPN5 = 81
    LDKIND_WINDYNDXP = 82
    LDKIND_WINDYNDXPP5 = 83
    LDKIND_WINDYNDXPN5 = 84
    LDKIND_DEAD = 100
    LDKIND_LIVE = 101
    LDKIND_LIVE1 = 102
    LDKIND_LIVE2 = 103
    LDKIND_VERSEIS = 104
    LDKIND_AIRDEFENCE = 105
    LDKIND_TEMP = 106
    LDKIND_TEMPUP = 107
    LDKIND_TEMPDOWN = 108
    LDKIND_SOIL = 109
    LDKIND_WATER = 110
    LDKIND_PRES = 111
    LDKIND_TEMPFHUP = 112
    LDKIND_CRANE = 120
    LDKIND_CRN_BRAKE_BEAMMN = 121
    LDKIND_CRN_BRAKE_BEAMVN = 122
    LDKIND_CRN_BRAKE_BEAMMP = 123
    LDKIND_CRN_BRAKE_BEAMVP = 124
    LDKIND_CRN_BRAKE_COL_VX = 125
    LDKIND_CRN_BRAKE_COL_VY = 126
    LDKIND_CRN_BRAKE_COL_MXP = 127
    LDKIND_CRN_BRAKE_COL_MXN = 128
    LDKIND_CRN_BRAKE_COL_MYP = 129
    LDKIND_CRN_BRAKE_COL_MYN = 130
    LDKIND_CRN_BRAKE_COL_NMAX_MXP = 131
    LDKIND_CRN_BRAKE_COL_NMAX_MXN = 132
    LDKIND_CRN_BRAKE_COL_NMAX_MYP = 133
    LDKIND_CRN_BRAKE_COL_NMAX_MYN = 134
    LDKIND_CRN_BRAKE_COL_NMIN_MXP = 135
    LDKIND_CRN_BRAKE_COL_NMIN_MXN = 136
    LDKIND_CRN_BRAKE_COL_NMIN_MYP = 137
    LDKIND_CRN_BRAKE_COL_NMIN_MYN = 138
    LDKIND_CRN_BRAKE_DIS_TRUSS = 139
    LDKIND_CRN_BRAKE_DIS_TRUSSPERP = 140
    LDKIND_CRN_BEAMMN = 141
    LDKIND_CRN_BEAMVN = 142
    LDKIND_CRN_BEAMMP = 143
    LDKIND_CRN_BEAMVP = 144
    LDKIND_CRN_COL_VX = 145
    LDKIND_CRN_COL_VY = 146
    LDKIND_CRN_COL_MXP = 147
    LDKIND_CRN_COL_MXN = 148
    LDKIND_CRN_COL_MYP = 149
    LDKIND_CRN_COL_MYN = 150
    LDKIND_CRN_COL_NMAX_MXP = 151
    LDKIND_CRN_COL_NMAX_MXN = 152
    LDKIND_CRN_COL_NMAX_MYP = 153
    LDKIND_CRN_COL_NMAX_MYN = 154
    LDKIND_CRN_COL_NMIN_MXP = 155
    LDKIND_CRN_COL_NMIN_MXN = 156
    LDKIND_CRN_COL_NMIN_MYP = 157
    LDKIND_CRN_COL_NMIN_MYN = 158
    LDKIND_WINDMS = 161
    LDKIND_WINDMSH = 211
    LDKIND_WINDMST = 261
    LDKIND_WINDXPI = 311
    LDKIND_WINDXPII = 312
    LDKIND_WINDXNI = 313
    LDKIND_WINDXNII = 314
    LDKIND_WINDYPI = 315
    LDKIND_WINDYPII = 316
    LDKIND_WINDYNI = 317
    LDKIND_WINDYNII = 318
    LDKIND_DEADZTQXXP = 319
    LDKIND_DEADZTQXXN = 320
    LDKIND_DEADZTQXYP = 321
    LDKIND_DEADZTQXYN = 322
    LDKIND_LIVEZTQXXP = 323
    LDKIND_LIVEZTQXXN = 324
    LDKIND_LIVEZTQXYP = 325
    LDKIND_LIVEZTQXYN = 326
    LDKIND_HORSEISXGZP = 327
    LDKIND_HORSEISXGZN = 328
    LDKIND_HORSEISYGZP = 329
    LDKIND_HORSEISYGZN = 330
    LDKIND_MAX = 340

class PostLDK:
    LDK_DEAD = 1
    LDK_LIVE = 2
    LDK_WIND = 3
    LDK_HORSEIS = 4
    LDK_VERSEIS = 5
    LDK_AIR = 6
    LDK_CRANE = 7
    LDK_TEMP = 8
    LDK_SOIL = 9
    LDK_WATER = 10
    LDK_LDCOMB_FUNDATION_NORMAL = 21
    LDK_LDCOMB_FUNDATION_HORSEIS = 22
    LDK_LDCOMB_FUNDATION_VERSEIS = 23
    LDK_LDCOMB_FUNDATION_VERSEISONLY = 24
    LDK_LDCOMB_FUNDATION_AIR = 25
    LDK_LDCOMB_NORMINAL_NORMAL = 31
    LDK_LDCOMB_NORMINAL_HORSEIS = 32
    LDK_LDCOMB_NORMINAL_VERSEIS = 33
    LDK_LDCOMB_NORMINAL_VERSEISONLY = 34
    LDK_LDCOMB_NORMINAL_AIR = 35
    LDK_LDCOMB_FREQUENT_NORMAL = 41
    LDK_LDCOMB_FREQUENT_HORSEIS = 42
    LDK_LDCOMB_FREQUENT_VERSEIS = 43
    LDK_LDCOMB_FREQUENT_VERSEISONLY = 44
    LDK_LDCOMB_FREQUENT_AIR = 45
    LDK_LDCOMB_QUASI_NORMAL = 51
    LDK_LDCOMB_QUASI_HORSEIS = 52
    LDK_LDCOMB_QUASI_VERSEIS = 53
    LDK_LDCOMB_QUASI_VERSEISONLY = 54
    LDK_LDCOMB_QUASI_AIR = 55

class PostLDType:
    LDTYPE_HORIZONX = 1
    LDTYPE_HORIZONY = 2
    LDTYPE_VERTICAL = 3
    LDTYPE_OTHER = 4

class PostPRCCombType:
    PRCCOMBTYPE_NL = 1
    PRCCOMBTYPE_YL = 2
    PRCCOMBTYPE_DIS = 3

class PostPRCComb:
    PRCCOMB_VX = 201
    PRCCOMB_VY = 202
    PRCCOMB_MXP = 203
    PRCCOMB_MXN = 204
    PRCCOMB_MYP = 205
    PRCCOMB_MYN = 206
    PRCCOMB_NMAX_MXP = 207
    PRCCOMB_NMAX_MXN = 208
    PRCCOMB_NMAX_MYP = 209
    PRCCOMB_NMAX_MYN = 210
    PRCCOMB_NMIN_MXP = 211
    PRCCOMB_NMIN_MXN = 212
    PRCCOMB_NMIN_MYP = 213
    PRCCOMB_NMIN_MYN = 214
    PRCCOMB_12D_14L = 215
    PRCCOMB_D_L = 216
    PRCCOMB_GRAVITY = 217
    PRCCOMB_13D_15L = 218

class PostPRCCombYL:
    PRCCOMBYL_MAX = 251
    PRCCOMBYL_MIN = 252

class PostPRCCombDis:
    PRCCOMBDIS_MAX = 301
    PRCCOMBDIS_MIN = 302

class PostSectDsnType:
    SECTDSNTYPE_M = 1
    SECTDSNTYPE_V = 2

class PostMaterialKind:
    MATERIAL_NULL = 0
    MATERIAL_CONCRETE = 1
    MATERIAL_STEEL = 2
    MATERIAL_SRC = 3
    MATERIAL_RECTTUBE = 4
    MATERIAL_CIRCLETUBE = 5
    MATERIAL_COMPOSITION = 6
    MATERIAL_BRICK = 7
    MATERIAL_BLOCK = 8
    MATERIAL_RCBLOCK = 9
    MATERIAL_TUBEREIN = 10
    MATERIAL_CONCRETEBRICK = 11
    MATERIAL_RECTTUBE_DBLSTEEL = 12
    MATERIAL_BBXG = 13
    MATERIAL_URCB = 14
    MATERIAL_AMCS = 15
    MATERIAL_YJSCC = 16
    MATERIAL_BAR = 51
    MATERIAL_USER = 101

class PostJGColKind:
    JGCOL_ZDJM = 1
    JGCOL_ZHHNT = 2
    JGCOL_WBXG = 3
    JGCOL_WZGB = 4
    JGCOL_WTXWFHCL = 5
    JGBEAM_ZDJM = 21
    JGBEAM_ZHHNT = 22
    JGBEAM_WBXG = 23
    JGBEAM_WZGB = 24
    JGBEAM_WTXWFHCL = 25
    JGBEAM_GJXW = 26
    JGBEAM_ZDJM_WZGB = 27

class PostBeamSupKind:
    BEAMSUP_NONE = 1
    BEAMSUP_BEAM = 2
    BEAMSUP_COL = 3
    BEAMSUP_COL_BK = 4
    BEAMSUP_COL_KZZ = 5
    BEAMSUP_BRACE = 6
    BEAMSUP_BRACE_COL = 7
    BEAMSUP_BRACE_HOR = 8
    BEAMSUP_WALL = 9

class PostBeamXJKind:
    BEAMXJ_NONE = 0
    BEAMXJ_JC = 1
    BEAMXJ_DJ = 2
    BEAMXJ_AC = 3

class PostBeamKind:
    BEAM_FRAME = 3
    BEAM_FRAME_NONE = 4
    BEAM_WALL = 5
    BEAM_TRAN_WALL = 6
    BEAM_TRAN_COL = 7
    BEAM_PORTALFRAME = 8
    BEAM_DISSIPATIVE = 9
    BEAM_COMPOSITE = 10
    BEAM_SUB = 11
    BEAM_RIB = 12
    BEAM_GRADE = 13
    BEAM_CRANE = 14

class PostColKind:
    COLPOS_MID = 1
    COLPOS_SIDE = 2
    COLPOS_CORNER = 3
    COLKIND_FRAME = 4
    COLKIND_KZZ = 5
    COLKIND_WALL = 6
    COLKIND_WALL_KZZ = 7
    COLKIND_PORTALFRAME = 8
    COLKIND_STRUCT = 9
    COLKIND_FACTORYZC = 10
    COLKIND_KFZ = 11

class PostBraceKind:
    BRACEKIND_NOBRACE = 1
    BRACEKIND_COL = 2
    BRACEKIND_BRACE = 3
    BRACEKIND_HORBRACE = 4
    BRACETYPE_Y = 11
    BRACETYPE_V = 12
    BRACETYPE_X = 13
    BRACETYPE_L = 14
    LINKTYPE_NULL = 100
    LINKTYPE_LINEAR = 101
    LINKTYPE_DAMPER = 102
    LINKTYPE_ISOLATOR = 103
    LINKTYPE_WEN = 106
    LINKTYPE_GAP = 107

class PostWallKind:
    WALL_NORMAL = 1
    WALL_SHORTLEG = 2
    WALL_STLBUCKLING = 3
    WALL_TUSQGGJGM = 11
    WALL_TUSYZKXM = 12
    WALL_TUSJMPTJX = 13
    WALL_TUSJMPTBW = 14

class PostWallSta:
    WALLSTA_FLANGE = 1
    WALLSTA_WEBPLATE = 2

class PostWallStrength:
    WALL_NONSTRENGTHFLR = 0
    WALL_STRENGTHFLR = 1
    WALL_STRENGTHFLRUP = 2

class PostWallPos:
    WALLPOS_PMLEFT = 1
    WALLPOS_PMMID = 2
    WALLPOS_PMRIGHT = 3

class PostWallSteelPos:
    WALLSTEELPOS_INSIDE = 1
    WALLSTEELPOS_OUTSIDE = 2

class PostBaseWall:
    BASEWALL_NONE = 0
    BASEWALL_NORMAL = 1
    BASEWALL_AIRDEFENCE = 2
    BASEWALL_BLASTPROOF = 3

class PostWallZYBSect:
    WALLZYBSECT_LINE = 1
    WALLZYBSECT_OTHER = 2

class PostEdgeType:
    EDGETYPE_1 = 1
    EDGETYPE_L = 2
    EDGETYPE_T = 3
    EDGETYPE_CROSS = 4
    EDGETYPE_1_COL = 5
    EDGETYPE_L_COL = 6
    EDGETYPE_T_COL = 7
    EDGETYPE_CROSS_COL = 8
    EDGETYPE_1_MIDCOL = 9
    EDGETYPE_Y = 10
    EDGETYPE_Y_COL = 11
    EDGETYPE_H = 12
    EDGETYPE_H_COL = 13
    EDGETYPE_Z = 14
    EDGETYPE_Z_COL = 15

class PostEdgeKind:
    EDGEKIND_RESTRAINT = 1
    EDGEKIND_CONSTRUCTIONAL = 2

class PostWJType:
    WJTYPE_WJ = 1
    WJTYPE_WQ_DC = 2
    WJTYPE_WQ_SC = 3
    WJTYPE_HJ = 4
    WJTYPE_ZX = 5
    WJTYPE_PX = 6
    WJTYPE_NORMAL = 7
    WJTYPE_PORTALFRAME = 8
    WJTYPE_GREENHOUSE = 9

class PostTrussKind:
    TRUSSKIND_CHORDUP = 1
    TRUSSKIND_WEB = 2
    TRUSSKIND_CHORDMID = 3
    TRUSSKIND_CHORDDW = 4
    TRUSSKIND_WEBSUP = 5
    GREENHOUSE_MAIN = 6
    GREENHOUSE_ARCH = 7
    GREENHOUSE_OTHER = 8

class PostNonlProp:
    NONLPROP_NONE = 0
    NONLPROP_TENSE = 1
    NONLPROP_COMP = 2

class PostPres:
    PRES_BONDTYPE_UNBONDED = 1
    PRES_BONDTYPE_BONDED = 2

class PostLimitKind:
    LIMIT_NULL = 0
    LIMIT_BEAM_V = 1
    LIMIT_BEAM_T = 2
    LIMIT_BEAM_VT = 3
    LIMIT_BEAM_ASMAXUP = 4
    LIMIT_BEAM_ASMAXDOWN = 5
    LIMIT_BEAM_XI = 6
    LIMIT_SRCBEAM_RATIO = 7
    LIMIT_SRCBEAM_BT = 8
    LIMIT_SRCBEAM_HT = 9
    LIMIT_SRCBEAM_VCON = 10
    LIMIT_STLBEAM_STREN = 11
    LIMIT_STLBEAM_STA = 12
    LIMIT_STLBEAM_V = 13
    LIMIT_STLBEAM_BT = 14
    LIMIT_STLBEAM_BTREG = 15
    LIMIT_STLBEAM_HT = 16
    LIMIT_STLBEAM_SPANOUTLENGTH = 17
    LIMIT_STLBEAM_NXN = 18
    LIMIT_STLZHBEAM_STREN = 19
    LIMIT_STLZHBEAM_V = 20
    LIMIT_STLZHBEAM_BT = 21
    LIMIT_STLZHBEAM_BTREG = 22
    LIMIT_STLZHBEAM_HT = 23
    LIMIT_STLZHBEAM_NUTNUM = 24
    LIMIT_PORTALBEAM_SLOPE = 25
    LIMIT_BEAMJDJG_ZDJMAS = 26
    LIMIT_BEAMJDJG_ZDJMASC = 27
    LIMIT_BEAMJDJG_ZHHNTHN = 28
    LIMIT_BEAMJDJG_WBXGAREA = 29
    LIMIT_BEAMJDJG_WZGBAREA = 30
    LIMIT_BEAMJDJG_WTXWFHCLAREA = 31
    LIMIT_COL_VX = 32
    LIMIT_COL_VY = 33
    LIMIT_COL_ASMAX = 34
    LIMIT_COL_ASMAX_SIDE = 35
    LIMIT_COL_ZYB = 36
    LIMIT_SRCCOL_RATIO = 37
    LIMIT_SRCCOL_CXB = 38
    LIMIT_SRCCOL_BT = 39
    LIMIT_SRCCOL_HT = 40
    LIMIT_SRCCOL_VCON = 41
    LIMIT_COLJOINT_VX = 42
    LIMIT_COLJOINT_VY = 43
    LIMIT_COLCAP = 44
    LIMIT_STLCOL_STREN = 45
    LIMIT_STLCOL_XSTA = 46
    LIMIT_STLCOL_YSTA = 47
    LIMIT_STLCOL_BT = 48
    LIMIT_STLCOL_HT = 49
    LIMIT_STLCOL_CXB = 50
    LIMIT_STLCOLJOINT_VX = 51
    LIMIT_STLCOLJOINT_VY = 52
    LIMIT_RECTTUBECOL_STREN = 53
    LIMIT_RECTTUBECOL_XSTA = 54
    LIMIT_RECTTUBECOL_YSTA = 55
    LIMIT_RECTTUBECOL_VXSTREN = 56
    LIMIT_RECTTUBECOL_VYSTREN = 57
    LIMIT_RECTTUBECOL_BT = 58
    LIMIT_RECTTUBECOL_HT = 59
    LIMIT_RECTTUBECOL_CXB = 60
    LIMIT_RECTTUBECOL_ALFAC = 61
    LIMIT_CIRCLETUBECOL_NSTREN = 62
    LIMIT_CIRCLETUBECOL_MSTREN = 63
    LIMIT_CIRCLETUBECOL_VSTREN = 64
    LIMIT_CIRCLETUBECOL_HT = 65
    LIMIT_CIRCLETUBECOL_CXB = 66
    LIMIT_CIRCLETUBECOL_SITA = 67
    LIMIT_TUBEREINCOL_HT = 68
    LIMIT_TUBEREINCOL_HGL = 69
    LIMIT_TUBEREINCOL_SITA = 70
    LIMIT_COLJDJG_ZHHNTHN = 71
    LIMIT_COLJDJG_WBXGAREA = 72
    LIMIT_COLJDJG_WZGBAREA = 73
    LIMIT_COLJDJG_WTXWFHCLAREA = 74
    LIMIT_WALLCOL_ASMAX = 75
    LIMIT_WALLCOL_V = 76
    LIMIT_WALLCOL_ZYB = 77
    LIMIT_WALLCOLSTA = 78
    LIMIT_WALLCOLSTA_ENT = 79
    LIMIT_WALLCOLSEAM = 80
    LIMIT_WALLCOLTUSPL = 81
    LIMIT_WALLCOLRECTTUBEM = 82
    LIMIT_WALLCOLRECTTUBEV = 83
    LIMIT_WALLCOLTHRATIO = 84
    LIMIT_STLWALL_V = 85
    LIMIT_STLWALL_CXB = 86
    LIMIT_STLWALL_KGB = 87
    LIMIT_WALLCOL_PRES_STRESS = 88
    LIMIT_WALLCOL_YSTA = 89
    LIMIT_RECTTUBECOL_FH_BHC = 90
    LIMIT_CIRCLETUBECOL_FH_BHC = 91
    LIMIT_STLBEAM_XNXS = 92
    LIMIT_STLCOL_XNXS = 93
    LIMIT_BEAMJDJG_WZGBTG = 94
    LIMIT_BEAMJDJG_WTXWFHCLTG = 95
    LIMIT_WALLCOL_V30 = 96
    LIMIT_URCBBEAM_RATIO = 97
    LIMIT_URCBBEAM_V = 98
    LIMIT_URCBBEAM_VCON = 99
    LIMIT_URCBCOL_RATIO = 100
    LIMIT_URCBCOL_VCON = 101
    LIMIT_URCBCOL_ZBAREA = 102
    LIMIT_URCBCOL_STREN = 103
    LIMIT_URCBCOL_XSTA = 104
    LIMIT_URCBCOL_YSTA = 105
    LIMIT_URCBCOL_VXSTREN = 106
    LIMIT_URCBCOL_VYSTREN = 107
    LIMIT_AMCSCOL_STREN = 108
    LIMIT_AMCSCOL_XSTA = 109
    LIMIT_AMCSCOL_YSTA = 110
    LIMIT_AMCSCOL_VXSTREN = 111
    LIMIT_AMCSCOL_VYSTREN = 112
    LIMIT_AMCSCOL_BT = 113
    LIMIT_AMCSCOL_HT = 114
    LIMIT_AMCSCOL_CXB = 115
    LIMIT_YJSCCBEAM_V = 116
    LIMIT_YJSCCBEAM_BUT = 117
    LIMIT_YJSCCBEAM_BDT = 118
    LIMIT_YJSCCBEAM_HT = 119
    LIMIT_YJSCCBEAM_ASMAXUP = 120
    LIMIT_YJSCCBEAM_NUTNUM = 121
    LIMIT_STLZHBEAM_LONGSHEARAS = 122
    LIMIT_WALLCOL_ASMINGD = 123

class Mdl_FlrTHInfo:
    m_LoadCaseName: str
    m_LoadCaseName_Short: str
    m_Angle: float
    m_Force: list[float]
class Mdl_ghShowOption_ComProperty:
    m_nBeamMat: int
    m_nBeamKind: int
    m_nBeamSectType: int
    m_nBeamBTGrade: int
    m_nBeamSupLink: int
    m_nBeamXJ: int
    m_nBeamTran: int
    m_nBeamXNSJ: int
    m_nBeamCrane: int
    m_nBeamRF: int
    m_nBeamWJType: int
    m_nBeamYZ: int
    m_nBeamYYL: int
    m_nBeamKZDJ: int
    m_nBeamPortal: int
    m_nBeamSect: int
    m_nColMat: int
    m_nColKind: int
    m_nColJZ: int
    m_nColSectType: int
    m_nColBTGrade: int
    m_nColLink: int
    m_nColTran: int
    m_nColXNSJ: int
    m_nColRF: int
    m_nColWJType: int
    m_nColYZ: int
    m_nColKZDJ: int
    m_nColPortal: int
    m_nColSect: int
    m_nBraceMat: int
    m_nBraceKind: int
    m_nBraceJZ: int
    m_nBraceSectType: int
    m_nBraceBTGrade: int
    m_nBraceLink: int
    m_nBraceTran: int
    m_nBraceXNSJ: int
    m_nBraceRF: int
    m_nBraceWJType: int
    m_nBraceYZ: int
    m_nBraceNonLProp: int
    m_nBraceBRB: int
    m_nBraceKZDJ: int
    m_nBracePortal: int
    m_nBraceSect: int
    m_nWallColMat: int
    m_nWallColKind: int
    m_nWallColBase: int
    m_nWallColShortLeg: int
    m_nWallColSZQ: int
    m_nWallColJQ: int
    m_nWallColTran: int
    m_nWallColXNSJ: int
    m_nWallColRF: int
    m_nWallColYZ: int
    m_nWallColKZDJ: int
    m_nWallColSect: int
    m_nWallBeamMat: int
    m_nWallBeamKind: int
    m_nWallBeamXJ: int
    m_nWallBeamTran: int
    m_nWallBeamXNSJ: int
    m_nWallBeamRF: int
    m_nWallBeamYZ: int
    m_nWallBeamKZDJ: int
    m_nWallBeamSect: int
    m_nSlabThick: int
    m_nSlabKind: int
class Mdl_ghComAdjustCoe:
    m_fjzx: float
    m_fjzy: float
    m_fjzz: float
    m_fbrc: float
    m_f02vx: float
    m_f02vy: float
    m_fzh: float
    m_fxfc: float
    m_fzps: float
    m_fzpseam: float
    m_fstlomigamin: float
    m_fstlbeta: float
    m_flivec: float
    m_fRoofCoe: float
    m_fwindxp: float
    m_fwindxn: float
    m_fwindyp: float
    m_fwindyn: float
    m_fkzzx: float
    m_fkzzy: float
    m_fkzzn: float
    m_fzcn: float
    m_fvcoex: float
    m_fvcoey: float
    m_fcq: float
    m_fdsnm: float
    m_fdsnv: float
    m_fnj: float
    m_ftf: float
class Mdl_dsnEPPara:
    m_nXNSJM: int
    m_nXNSJV: int
    m_nXNSJSeisLevel: int
class Mdl_dsnEPReportPara:
    nOutputSect: int
    nOutputM: int
    nOutputUpOrX: int
    nOutputDsnInfo: int
class Mdl_ExistBarData:
    fAsX: float
    fAsY: float
    fAsVX: float
    fAsVY: float
class Mdl_ExistWallBarData:
    fVertReinRatio: float
    fAsS: float
    fAsE: float
class Mdl_ExistBeamBarData:
    fAsUp: float
    fAsDw: float
class Mdl_STowExp:
    cCL: float
    cBE: float
    cWA: float
    cSB: float
    cBR: float
    stl: int
    h: int
    q: float
    JQC: str
    DBJQQ: str
    GDC: str
    YBZ: str
    XTL: str
    ROOF: str
    sCLMain: int
    sBEMain: int
    sWAMain: int
    sCLHoop: int
    sBEHoop: int
    sWAHoop: int
    sWAHStl: int
    sWAVStl: int
    rohWAVStl: float
    rohWAHStl: float
    kzdjCL: int
    kzdjBEMain: int
    kzdjBESub: int
    kzdjWA: int
    kzdjBR: int
    gzkzdjCL: int
    gzkzdjBEMain: int
    gzkzdjBESub: int
    gzkzdjWA: int
    gzkzdjBR: int
    kzdjSCL: int
    kzdjSBEMain: int
    kzdjSBESub: int
    kzdjSBR: int
    gzkzdjSCL: int
    gzkzdjSBEMain: int
    gzkzdjSBESub: int
    gzkzdjSBR: int
    cpxsCL: float
    cpxsBE: float
    cpxsWC: float
    cpxsWB: float
    cpxsBR: float
    calcIdx: int
    gama: float
    stlCl: int
    stlBe: int
    stlWa: int
    stlBr: int
    fz: int
    no: int
    orino: int
    poly: list[None[float, float]]
    up: list[None[int, int]]
    dw: list[None[int, int]]
    _poly: list
    _up: list
    _dw: list
    def ConvertCSharpList(self) -> None: ...
    def ConvertPyList(self) -> None: ...
class LinkType:
    ISOLATOR = 1
    DAMPER = 2
    PLASTIC = 3
